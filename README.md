# second-brain

## Installation

Clone the repository and install dependencies:

```bash
git clone <repo-url>
cd second-brain
uv sync
```

## Usage

Capture a quick thought:

```bash
uv run second_brain new "My brilliant idea about caching"
```

This creates `~/second_brain/2026-03-22-my-brilliant-idea-about-caching.md` with a heading and timestamp. Duplicate titles on the same day get a numeric suffix (`-1`, `-2`, …) to avoid overwriting.

List all notes:

```bash
uv run second_brain list
```

Show a note's content:

```bash
uv run second_brain show 1
```

With dev environment variables:

```bash
uv run --env-file .env second_brain new "Some thought"
```

Via Python module:

```bash
uv run python -m second_brain new "Some thought"
```

## Environment Variables

`.env.example` is the committed template — copy it to `.env` for development:

```bash
cp .env.example .env
```

| Variable           | Default            | Description                                         |
|--------------------|--------------------|-----------------------------------------------------|
| `SECOND_BRAIN_DIR` | `~/second_brain/`  | Directory where notes are stored. Created automatically. |
| `LOG_LEVEL`        | `INFO`             | Console log level. Set to `DEBUG` in `.env` for verbose output. |
| `LOG_FILE`         | `app.log`          | Path to the log file.                               |

Note: `uv run --env-file .env` loads the dev environment explicitly (no auto-loading).

## Log Format

Console output uses a compact format with 3-letter level codes (INF, DBG, WRN, etc.).
See the [Usage Guide](docs/usage.md) for details.

## Testing

Run tests:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov
```

## Documentation

Preview docs locally:

```bash
uv run python scripts/serve_docs.py
```

Build static docs:

```bash
uv run mkdocs build
```
