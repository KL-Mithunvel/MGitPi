# CLAUDE.me — MGitPi Project Brief

This file describes the MGitPi project for AI-assisted development sessions.
It covers the project's purpose, architecture, conventions, and rules that must
be followed when contributing to this codebase.

---

## Project Overview

**MGitPi** is a modular, menu-driven, cyber-styled Git control interface built
specifically for Raspberry Pi and resource-constrained embedded Linux systems.

The goal is to provide a clean, keyboard-driven terminal UI that wraps common
Git operations in an intuitive, KIAUH-inspired interface — making Git accessible
on headless Raspberry Pi boards without needing a web browser or GUI.

**Author:** KL Mithunvel (mithunvel-kl)
**License:** MIT (2026)
**Entry point:** `python3 main.py`
**Minimum Python:** 3.10
**Runtime dependencies:** None (standard library only + system `git`)

---

## Architecture

### Module Responsibilities

| File | Role |
|------|------|
| `main.py` | Application entry point; defines all menus and routes user choices to handler functions |
| `klm_menu.py` | Menu engine — renders menus, reads input, validates hotkeys, drives navigation |
| `art.py` | Branding and UI chrome — splash screen, ASCII logo, ANSI color helpers, terminal utilities |
| `repo_manager.py` | *(planned)* Persistent list of repository paths at `~/.mgitpi/repos.json` |
| `git_ops.py` | *(planned)* Subprocess wrappers for every Git command; all output captured and returned |
| `ui_box.py` | *(planned)* Reusable UTF-8 box-drawing components shared across the UI |

### Data Flow

```
python3 main.py
    └─► art.splash()             # 5-second animated welcome screen
    └─► show_menu(menu_system)   # Main loop
            └─► klm_menu.present_menu()    # Render + read input
            └─► handler_function()         # Stub or real implementation
                    └─► git_ops.*()        # Subprocess Git calls (planned)
                    └─► repo_manager.*()   # Persistence (planned)
```

### Menu System

Menus are plain Python dicts:

```python
{
    "menu": "Display Name",
    "name": "internal_id",
    "width": 90,
    "options": [
        [command_string, "Label shown to user", "hotkey"],
    ],
    "back_option": True,
    "back_to": "parent_menu_name"
}
```

Navigation prefixes:
- `"menu:some_name"` — navigate to a sub-menu
- Any other string — calls the matching function in `main.py`

### Persistence

All persistent state lives in `~/.mgitpi/` (never in the project directory).

```
~/.mgitpi/
└── repos.json     # { "repos": ["/path/to/repo", ...] }
```

---

## Current Status

### Implemented and working
- Splash screen with ASCII art logo and ANSI color support
- Full menu engine with hotkey navigation, back navigation, and input validation
- All menu structures defined (workspace, repo, branch, stash, rebase, undo)
- Terminal width detection and responsive layout

### Stubs (defined, not yet implemented)
Every handler function in `main.py` is a `pass` or `print("TODO")` stub:

- Repository open / clone / add / remove / validate
- Git status, stage, commit, pull, push
- Branch management (create, switch, delete, merge)
- Stash, rebase, and undo operations
- Commit log viewer

These must be implemented in `git_ops.py` and `repo_manager.py`, then wired
into the stubs in `main.py`.

---

## Development Rules

The following rules apply to all contributions, human or AI-assisted.

### 1. Separation of Concerns

- **UI logic** belongs in `art.py`, `klm_menu.py`, or `ui_box.py`.
- **Git logic** belongs exclusively in `git_ops.py`.
- **Persistence logic** belongs exclusively in `repo_manager.py`.
- `main.py` is the router only — it calls into other modules, it does not
  contain Git commands, file I/O, or rendering code.

Never put `subprocess` calls in `main.py`. Never put menu definitions outside
`main.py`.

### 2. No External Dependencies

The project must run with Python 3.10+ standard library and a system `git`
install only. Do not add `requirements.txt`, `pip install` steps, or any third-
party packages. If something seems to need an external library, implement the
minimal needed subset from scratch.

### 3. Git Operations via Subprocess

All Git commands must go through `subprocess.run()` or `subprocess.Popen()`
with:
- `capture_output=True`
- `text=True`
- Explicit error checking (check `returncode`)
- Errors returned to the caller, not printed directly

Example pattern:
```python
result = subprocess.run(
    ["git", "status", "--short"],
    capture_output=True, text=True, cwd=repo_path
)
if result.returncode != 0:
    return None, result.stderr.strip()
return result.stdout.strip(), None
```

### 4. Persistent Data in `~/.mgitpi/`

Never write files into the project directory at runtime. All user data (saved
repo paths, settings) must go into `~/.mgitpi/`. Use `pathlib.Path.home()` to
resolve the path — never hardcode `/home/pi/` or any username.

### 5. ANSI Colors Are Optional

Both `art.py` and `klm_menu.py` expose an `ANSI = True` flag. Color output
must always be wrapped through the helper functions (`cyan()`, `bold()`,
`dim()`, `_c()`). Never write raw `\033[…m` escape codes inline in other
modules.

### 6. Menu Hotkeys Must Be Unique Per Menu

Within a single menu, every hotkey must be a distinct single character.
By convention:
- First letter of the action when possible (e.g., `s` → Status, `c` → Commit)
- `b` is always reserved for Back navigation
- `x` or `q` is reserved for Exit/Quit at the top-level menu

### 7. Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Functions | `snake_case` | `clone_repo_ssh` |
| Internal helpers | `_leading_underscore` | `_c` |
| Module-level constants | `UPPER_CASE` | `ANSI` |
| Menu `name` keys | lowercase, no spaces | `"branch_tools"` |

### 8. Terminal Width Awareness

Never hardcode a line width. Always use `art.term_width()` or the `width` key
from the menu dict. Respect terminals as narrow as 60 columns. Use
`art.center()` for centering; never manually count spaces.

### 9. Error Handling Principles

- Git command errors must be shown to the user in a clear, plain-English
  message. Do not dump raw stderr.
- Invalid menu input re-prompts silently — do not print an error, just loop.
- Missing config files (`repos.json`) must be created automatically on first
  run with safe defaults. Never crash on a missing file.
- Functions that can fail must return `(result, error)` tuples, not raise
  unhandled exceptions.

### 10. No Hardcoded Usernames or Paths

Never hardcode `/home/pi`, `/home/user`, a username, or any system-specific
path. Use `pathlib.Path.home()` for the home directory and `pathlib.Path.cwd()`
or the saved repo path for working directories.

### 11. Cross-Platform Awareness

The primary targets are Raspberry Pi OS and Debian-based Linux. Windows
support is secondary. The `art.clear()` function already handles `cls` vs
`clear`. Any new OS-specific code must follow the same pattern: check
`sys.platform` and branch, with Linux as the primary path.

### 12. Adding a New Menu Action

1. Add a handler stub in `main.py`:
   ```python
   def my_new_action():
       pass  # TODO: implement
   ```
2. Add an entry to the relevant menu dict in `main.py`:
   ```python
   ["my_new_action", "My New Action", "n"],
   ```
3. Implement the Git logic in `git_ops.py`.
4. Wire the implementation into the stub: call `git_ops.my_function()`.
5. Never skip step 3 — don't put Git logic in `main.py`.

### 13. Adding a New Menu

1. Define the menu dict in `menu_system` in `main.py`.
2. Add a navigation entry (`"menu:new_menu_name"`) in the parent menu.
3. Ensure `"back_to"` points to the correct parent menu name.
4. Verify every hotkey in the new menu is unique within that menu.

### 14. Commit Message Style

Use imperative mood, short subject line (≤ 72 chars), no trailing period:
```
Add branch creation handler in git_ops.py
Fix hotkey collision in stash menu
Implement repo_manager persistence layer
```

Do not use vague messages like "fix stuff", "update code", or "changes".

### 15. Testing

There is currently no test suite. Until one is added:
- Manually test every menu path before committing.
- Test on a real or emulated terminal (not just an IDE run configuration).
- Verify behavior on narrow terminals (≤ 80 columns).
- Verify graceful behavior when `git` is not on PATH.

When a test framework is added, the convention will be `pytest` with tests in
a `tests/` directory. Each `git_ops.py` function must have at least one test
using a temporary git repository created with `tempfile.mkdtemp()`.

---

## Quick Reference

```bash
# Run the application
python3 main.py

# Lint (if/when configured)
python3 -m py_compile main.py klm_menu.py art.py

# Project-wide text search (useful for finding TODOs)
grep -rn "TODO\|FIXME\|pass$" --include="*.py" .
```

---

## Philosophy

MGitPi is built for the Pi, not for the cloud. Keep it:

- **Simple** — one screen at a time, one action per keypress
- **Lightweight** — zero runtime dependencies beyond Python and Git
- **Readable** — clear module boundaries, short functions, obvious names
- **Resilient** — never crash on missing files, bad input, or Git errors
- **Expandable** — every new feature fits cleanly into the existing pattern
