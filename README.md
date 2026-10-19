# prosango-project
Repository with Python and TypeScript prosango directory structure

Run the Django and Rsbuild development servers together with `python run.py parallel`.
They use ports 8000 and 3000 respectively. Override them independently with
`DJANGO_PORT` and `RSBUILD_PORT`, for example:

```sh
python run.py parallel DJANGO_PORT=8001 RSBUILD_PORT=3001
```

The ports must be different. In parallel mode, use these variables instead of
passing shared `--port` or `--addrport` arguments.
