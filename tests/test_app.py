import re

import pytest

from second_brain.app import console_format, main


class _Level:
    """Minimal stand-in for loguru's record level object."""

    def __init__(self, name):
        self.name = name


# -- Unit tests for console_format ------------------------------------------


def test_console_format_returns_compact_string():
    record = {"level": _Level("INFO")}
    result = console_format(record)

    assert "INF" in result
    assert " | " in result
    assert result.endswith("\n{exception}")
    assert "INFO" not in result


@pytest.mark.parametrize(
    "level_name,expected_short",
    [
        ("TRACE", "TRC"),
        ("DEBUG", "DBG"),
        ("INFO", "INF"),
        ("SUCCESS", "SUC"),
        ("WARNING", "WRN"),
        ("ERROR", "ERR"),
        ("CRITICAL", "CRT"),
    ],
)
def test_console_format_all_levels(level_name, expected_short):
    record = {"level": _Level(level_name)}
    result = console_format(record)
    assert expected_short in result


def test_console_format_unknown_level_falls_back_to_slice():
    record = {"level": _Level("CUSTOM_LEVEL")}
    result = console_format(record)
    assert "CUS" in result


# -- Integration tests -------------------------------------------------------


def test_main_logs_greeting(capfd):
    main()
    captured = capfd.readouterr()
    assert "Hello from second_brain!" in captured.err


def test_main_console_output_matches_compact_format(capfd):
    main()
    captured = capfd.readouterr()
    lines = [ln for ln in captured.err.strip().splitlines() if ln.strip()]
    assert lines, "Expected at least one log line on stderr"
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| \w{3} \| .+:.+:\d+ \| .+"
    for line in lines:
        assert re.match(pattern, line), f"Line does not match compact format: {line!r}"


def test_file_handler_uses_default_format(tmp_path, monkeypatch):
    log_file = tmp_path / "verify.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))
    main()
    content = log_file.read_text()
    assert "INFO" in content
    assert " - Hello from second_brain!" in content
