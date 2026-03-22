# Module Dependency Map

> **No circular dependencies detected.** All internal modules form a clean acyclic graph.

```mermaid
flowchart LR
    subgraph Entry["Entry Point"]
        MAIN["__main__.py"]
    end

    subgraph CLI["CLI Layer"]
        cli["cli.py"]
    end

    subgraph Core["Core Modules"]
        app["app.py"]
        notes["notes.py"]
    end

    subgraph Tests["Tests"]
        conftest["conftest.py"]
        test_app["test_app.py"]
        test_cli["test_cli.py"]
        test_notes["test_notes.py"]
    end

    subgraph Scripts["Scripts"]
        serve_docs["serve_docs.py"]
    end

    subgraph Ext["External / stdlib"]
        lib_click["click"]
        lib_loguru["loguru"]
        lib_pytest["pytest"]
        lib_stdlib["sys · os · re · pathlib · datetime · subprocess"]
    end

    %% Internal wiring
    MAIN --> cli
    cli  --> app
    cli  --> notes

    %% Test → production
    test_app   --> app
    test_cli   --> cli
    test_notes --> notes

    %% Production → external
    app      --> lib_loguru
    app      --> lib_stdlib
    cli      --> lib_click
    cli      --> lib_stdlib
    notes    --> lib_stdlib

    %% Test → external
    conftest   --> lib_pytest
    test_app   --> lib_pytest
    test_cli   --> lib_pytest
    test_cli   --> lib_click
    test_notes --> lib_pytest

    %% Scripts → external
    serve_docs --> lib_stdlib
```

## Safe-change guide

| Module | Imports from | Imported by | Safe to change? |
|---|---|---|---|
| `app.py` | loguru, stdlib only | `cli.py`, `test_app.py` | Yes — leaf module, changes affect only its direct callers |
| `notes.py` | stdlib only | `cli.py`, `test_notes.py` | Yes — leaf module, same reasoning |
| `cli.py` | `app`, `notes`, click, stdlib | `__main__.py`, `test_cli.py` | Yes, but changes ripple to `__main__` and `test_cli` |
| `__main__.py` | `cli` only | *(entry point)* | Yes — nothing imports this |
| `conftest.py` | pytest only | *(pytest fixture scope)* | Yes — test infrastructure only |
| `serve_docs.py` | stdlib only | *(standalone script)* | Yes — fully isolated |

**Key insight:** `app.py` and `notes.py` are pure leaf modules with no internal imports.
Any refactor there stays local. The only module with fan-in risk is `cli.py`.
