#!/usr/bin/env python3
import sys
import os
import subprocess
import threading
import time

# --- Helper Configuration ---
IS_WINDOWS = os.name == 'nt'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TS_DIR = os.path.join(ROOT_DIR, "typescript-frontend")
PY_DIR = os.path.join(ROOT_DIR, "django-project")

if IS_WINDOWS:
    VENV_PYTHON = os.path.join(PY_DIR, ".venv", "Scripts", "python.exe")
    VENV_PIP = os.path.join(PY_DIR, ".venv", "Scripts", "pip.exe")
else:
    VENV_PYTHON = os.path.join(PY_DIR, ".venv", "bin", "python")
    VENV_PIP = os.path.join(PY_DIR, ".venv", "bin", "pip")

# Keep track of active background processes for parallel shutdown
active_processes = []

def run_command(cmd, cwd, env_updates=None, wait=True):
    """Executes a command inheriting the system environment."""
    current_env = os.environ.copy()
    if env_updates:
        current_env.update(env_updates)
    
    try:
        command = subprocess.list2cmdline(cmd) if IS_WINDOWS else cmd
        proc = subprocess.Popen(command, cwd=cwd, env=current_env, shell=IS_WINDOWS)
        active_processes.append(proc)
        
        if wait:
            proc.wait()
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd)
    except Exception as e:
        print(f"\n❌ Execution error: {e}")
        sys.exit(1)

# --- Core Task Commands ---
def setup():
    print("📦 Installing TypeScript dependencies...")
    run_command(["npm", "install"], cwd=TS_DIR)
    
    print("\n🐍 Creating Python virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", os.path.join(PY_DIR, ".venv")], check=True)
    
    print("\n📦 Installing Python dependencies inside .venv...")
    run_command([VENV_PIP, "install", "-r", "requirements.txt"], cwd=PY_DIR)
    print("\n✅ Setup complete!")

def run_py(args, envs, wait=True):
    cmd = [VENV_PYTHON, "manage.py", "runserver", *args]
    run_command(cmd, cwd=PY_DIR, env_updates=envs, wait=wait)

def run_manage(args, envs, wait=True):
    cmd = [VENV_PYTHON, "manage.py", *args]
    run_command(cmd, cwd=PY_DIR, env_updates=envs, wait=wait)

def run_ts(args, envs, wait=True):
    cmd = ["npm", "run", "dev", *(["--", *args] if args else [])]
    run_command(cmd, cwd=TS_DIR, env_updates=envs, wait=wait)

def run_npm(args, envs, wait=True):
    cmd = ["npm", *args]
    run_command(cmd, cwd=TS_DIR, env_updates=envs, wait=wait)

def run_parallel(args, envs):
    print("🚀 Starting both Python and TypeScript services in parallel...")
    print("💡 Press Ctrl+C at any time to shut down both.\n")

    django_port = envs.get("DJANGO_PORT", "8000")
    rsbuild_port = envs.get("RSBUILD_PORT", "3000")
    try:
        django_port = int(django_port)
        rsbuild_port = int(rsbuild_port)
        if not 0 <= django_port <= 65535 or not 0 <= rsbuild_port <= 65535:
            raise ValueError
    except ValueError:
        raise SystemExit("❌ DJANGO_PORT and RSBUILD_PORT must be valid port numbers (0-65535).")

    if django_port == rsbuild_port:
        raise SystemExit("❌ DJANGO_PORT and RSBUILD_PORT must be different.")

    if any(
        arg in ("--port", "--addrport")
        or arg.startswith(("--port=", "--addrport="))
        for arg in args
    ):
        raise SystemExit(
            "❌ Shared --port/--addrport arguments are not supported in parallel mode. "
            "Use DJANGO_PORT=... and RSBUILD_PORT=... instead."
        )

    parallel_envs = envs.copy()
    parallel_envs.setdefault("RSBUILD_BASE_URL", f"http://localhost:{rsbuild_port}")
    
    # Target threads to execute tasks concurrently
    ts_thread = threading.Thread(
        target=run_ts,
        args=(["--port", str(rsbuild_port), *args], parallel_envs, False),
        daemon=True,
    )
    py_thread = threading.Thread(
        target=run_py,
        args=(["--port", str(django_port), *args], parallel_envs, False),
        daemon=True,
    )
    
    ts_thread.start()
    py_thread.start()
    
    # Keep the main process alive to intercept Ctrl+C signals cleanly
    try:
        while True:
            time.sleep(0.5)
            # If any process terminated prematurely on its own, stop the execution loop
            if any(p.poll() is not None for p in active_processes):
                break
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all services gracefully...")
    finally:
        # Loop through running instances and kill them down neatly
        for proc in active_processes:
            if proc.poll() is None:
                proc.terminate()
        print("👋 Extited all parallel tasks safely.")

# --- CLI Parser ---
def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [setup | py | manage | ts | npm | parallel] [KEY=VALUE ...] [--args...]")
        sys.exit(1)
        
    task = sys.argv[1]
    passed_args = sys.argv[2:]
    
    envs = {}
    forward_args = []
    
    for item in passed_args:
        if "=" in item and not item.startswith("-"):
            key, val = item.split("=", 1)
            envs[key] = val
        else:
            forward_args.append(item)

    if task in ("py", "manage", "parallel"):
        envs.setdefault("DJANGO_DEBUG", "true")
        envs.setdefault(
            "DJANGO_CORS_ALLOWED_ORIGINS",
            f"http://localhost:{envs.get('RSBUILD_PORT', '3000')}",
        )

    if task == "setup":
        setup()
    elif task == "py":
        run_py(forward_args, envs)
    elif task == "manage":
        run_manage(forward_args, envs)
    elif task == "ts":
        run_ts(forward_args, envs)
    elif task == "npm":
        run_npm(forward_args, envs)
    elif task == "parallel":
        run_parallel(forward_args, envs)
    else:
        print(f"Unknown task: {task}. Choose from setup, py, manage, ts, npm, parallel.")
        sys.exit(1)

if __name__ == "__main__":
    main()
