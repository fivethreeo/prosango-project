# Prosango repository instructions

## Setup and commands

- Bootstrap both projects from the repository root with `python run.py setup`. It installs frontend dependencies and creates `django-project/.venv` with the Python dependencies.
- Start Django and Rsbuild together with `python run.py parallel`. By default they bind to `127.0.0.1:8000` and `127.0.0.1:3000`. Configure them with assignments such as `python run.py parallel HOST=0.0.0.0 DJANGO_PORT=8001 RSBUILD_PORT=3001`; the two ports must differ. Do not pass shared `--host`, `--port`, or `--addrport` flags to `parallel`.
- Run Django management commands through the project wrapper, for example `python run.py manage migrate` or `python run.py manage test`. To run one Django test, use its dotted label: `python run.py manage test package.tests.TestCase.test_method`.
- Work on just the backend with `python run.py py` (forwarding Django `runserver` arguments), or just the frontend with `python run.py ts`. Run arbitrary frontend npm commands through `python run.py npm <args>`.
- Frontend commands run from `typescript-frontend/`: `npm run dev`, `npm run build`, and `npm run preview`. `npm run build` is the frontend’s available production build/type-checking validation. There is currently no separate lint script or frontend test runner.

## Architecture

- Django (`django-project/prosango`) owns HTTP routing, the admin, configuration, database access, and the HTML shell. The root URL is a `TemplateView` for `templates/index.html`; the browser application mounts into that template’s `#root` element from `typescript-frontend/src/index.ts`.
- Rsbuild produces the browser assets and `typescript-frontend/dist/manifest.json`. The `{% rsbuild_entry 'index' %}` tag in the Django template reads that manifest and emits its CSS and deferred JavaScript URLs. New frontend entry points must be represented both in Rsbuild’s manifest and in the consuming Django template tag.
- In development, Rsbuild writes the manifest to disk and Django loads its URLs from `RSBUILD_BASE_URL` (normally `http://localhost:3000`). Therefore start the frontend server or build the frontend before rendering Django pages; otherwise the template tag raises a clear manifest error.
- In production, run the frontend build before Django static-file collection. `STATICFILES_DIRS` includes the frontend `dist` directory, `collectstatic` copies the manifest/assets to `STATIC_ROOT`, and production configuration reads the manifest from there.

## Repository conventions

- Runtime configuration is environment-based in `prosango/local_settings.py`. Use the `DJANGO_*` variables for debug mode, secret key, hosts, database, static root, and CORS settings rather than editing committed settings for deployments. A non-debug process requires `DJANGO_SECRET_KEY`.
- The launcher defaults `DJANGO_DEBUG=true` and derives `DJANGO_CORS_ALLOWED_ORIGINS` from the Rsbuild host/port in `parallel` mode. If changing service-host behavior, keep `RSBUILD_BASE_URL` and CORS origin configuration aligned.
- TypeScript uses native ESM/bundler resolution and treats unused locals and parameters as errors. Keep frontend source under `typescript-frontend/src`; the generated `dist` contents are build output.
