# Usage

## Installation

Clone the repository and install dependencies:

```bash
uv sync
```

## Capturing a Thought

```bash
uv run second_brain new "My brilliant idea about caching"
```

This creates a markdown file like `~/second_brain/2026-03-22-my-brilliant-idea-about-caching.md`:

```markdown
# My brilliant idea about caching

2026-03-22T14:30:00
```

The file path is printed to stdout on success.

## Listing Notes

```bash
uv run second_brain list
```

Prints the notes directory path followed by a numbered list of filenames,
sorted newest-first:

```
Notes: /Users/rp/second_brain

1. 2026-03-22-my-idea.md
2. 2026-03-21-another-note.md
3. 2026-03-20-hello-world.md
```

If no notes exist yet or the directory hasn't been created, a helpful message
is shown instead.

## Showing a Note

```bash
uv run second_brain show 1
```

Prints the raw markdown content of note #1 (matching the numbered output from
`list`).

If the number is out of range:

```
$ second_brain show 99
Error: Note 99 not found. Only 2 notes available.
```

## Duplicate Titles

If a note with the same title already exists for the same day, a numeric suffix
is appended automatically (`-1`, `-2`, …) to prevent overwriting:

```bash
uv run second_brain new "My idea"   # → 2026-03-22-my-idea.md
uv run second_brain new "My idea"   # → 2026-03-22-my-idea-1.md
```

With dev environment variables:

```bash
uv run --env-file .env second_brain new "Some thought"
```

Or as a Python module:

```bash
uv run python -m second_brain new "Some thought"
```

## Environment Variables

| Variable           | Default            | Description                          |
|--------------------|--------------------|--------------------------------------|
| `SECOND_BRAIN_DIR` | `~/second_brain/`  | Directory where notes are stored. Created automatically. |
| `LOG_LEVEL`        | `INFO`             | Console log level (DEBUG, INFO, …)   |
| `LOG_FILE`         | `app.log`          | Path to the log file                 |

Copy `.env.example` to `.env` for development defaults, then run with `uv run --env-file .env`.

## Log Output

### Console

The console (stderr) uses a compact format:

```
2026-03-21 20:34:28 | INF | second_brain.app:main:29 | Hello from second_brain!
```

Level names are shortened to 3 letters: TRC, DBG, INF, SUC, WRN, ERR, CRT.

### File

The file handler (`LOG_FILE`, default `app.log`) uses loguru's default verbose
format with millisecond timestamps, full level names, and automatic rotation.
