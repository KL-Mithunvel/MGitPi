# CLAUDE.md — MGitPi Project Brief

> **IMPORTANT:** Read `CLAUDE-COMMON.md` first — it contains general must-follow instructions (companion files, deployment model, workflow, template structure). This file contains repo-specific instructions. Anything here overrides `CLAUDE-COMMON.md`.
>
> **Also read `PROJ_STARTER.md`** — it contains the owner's personal preferences (interaction rules, coding standards, tech stack choices, commit style). The **User Rules** section at the bottom already incorporates both — no need to re-read unless refreshing context.

---

## Project Overview

**MGitPi** is a modular, menu-driven, cyber-styled Git control interface built
specifically for Raspberry Pi and resource-constrained embedded Linux systems.

The goal is to provide a clean, keyboard-driven terminal UI that wraps common
Git operations in an intuitive, KIAUH-inspired interface — making Git accessible
on headless Raspberry Pi boards without needing a web browser or GUI.

| Field                    | Value                                          |
|--------------------------|------------------------------------------------|
| **Author**               | KL Mithunvel (`mithunvel-kl`)                  |
| **License**              | MIT (2026)                                     |
| **Entry point**          | `python3 main.py`                              |
| **Minimum Python**       | 3.10                                           |
| **Runtime dependencies** | None (standard library only + system `git`)    |

---

## Running the System

```bash
# No virtualenv needed — standard library only at runtime

# Run the application
python3 main.py

# Lint all source files before committing
python3 -m py_compile main.py klm_menu.py art.py git_ops.py repo_manager.py

# Project-wide TODO / stub scan
grep -rn "TODO\|FIXME\|pass$" --include="*.py" .

# Run tests (once test suite is added)
pytest tests/
```

---

## Architecture

### Module Responsibilities

| File              | Status       | Role                                                                                    |
|-------------------|--------------|-----------------------------------------------------------------------------------------|
| `main.py`         | ✔ Active     | Application entry point; defines all menus and routes user choices to handler functions |
| `klm_menu.py`     | ✔ Active     | Menu engine — renders menus, reads input, validates hotkeys, drives navigation          |
| `art.py`          | ✔ Active     | Branding and UI chrome — splash screen, ASCII logo, ANSI color helpers, terminal utils  |
| `repo_manager.py` | *(stub)*     | Persistent list of repository paths at `~/.mgitpi/repos.json`                          |
| `git_ops.py`      | *(stub)*     | Subprocess wrappers for every Git command; all output captured and returned             |
| `ui_box.py`       | *(planned)*  | Reusable UTF-8 box-drawing components shared across the UI                              |

### Data Flow

```
python3 main.py
    └─► art.splash()                   # 5-second animated welcome screen
    └─► show_menu(menu_system)         # Main loop
            └─► klm_menu.present_menu()        # Render + read input
            └─► handler_function()             # Stub or real implementation
                    └─► git_ops.*()            # Subprocess Git calls (stub)
                    └─► repo_manager.*()       # Persistence (stub)
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

| Prefix | Behaviour |
|--------|-----------|
| `"menu:some_name"` | Navigate to a sub-menu |
| Any other string | Calls the matching function in `main.py` |

### Persistence

All persistent state lives in `~/.mgitpi/` (never in the project directory).

```
~/.mgitpi/
└── repos.json     # { "repos": ["/path/to/repo", ...] }
```

---

## Key Modules

### `main.py`
- Entry point: calls `art.splash()` then enters menu loop via `show_menu(menu_system)`
- Defines all menu dicts in `menu_system` list
- Contains all action handler stubs — each must call into `git_ops` or `repo_manager` only
- Must not contain `subprocess` calls, file I/O, or menu rendering code

### `klm_menu.py`
- `present_menu(menu_dict)` — renders a menu and reads a hotkey; returns the selected command string
- `validate_hotkey(key, options)` — checks key is valid for the current menu
- All rendering is terminal-width-aware via `art.term_width()`

### `art.py`
- `splash()` — animated 5-second splash screen with ASCII logo
- `term_width()` — returns current terminal column count
- `center(text, width)` — centers text in a given width
- `clear()` — cross-platform terminal clear (`cls` / `clear`)
- `cyan(t)`, `bold(t)`, `dim(t)`, `_c(t)` — ANSI color helpers; respect the `ANSI` flag

### `git_ops.py` *(stub — not yet implemented)*
- All functions return `(result, error)` tuples — never raise unhandled exceptions
- Must use `subprocess.run()` with `capture_output=True, text=True, cwd=repo_path`
- Planned functions: `git_status()`, `git_add_interactive()`, `git_commit()`, `git_push()`, `git_pull()`, `git_list_branches()`, `git_checkout()`, `git_create_branch()`, `git_delete_branch()`, `git_stash()`, `git_stash_pop()`, `git_log()`, `git_diff()`, `git_reset()`

### `repo_manager.py` *(stub — not yet implemented)*
- Manages `~/.mgitpi/repos.json`
- Planned: `load_repos()`, `add_repo(path)`, `remove_repo(path)`, `validate_repos()`
- Always resolve home dir via `pathlib.Path.home()` — never hardcode `/home/pi` or any username
- Auto-creates `repos.json` with `{"repos": []}` on first run if missing

---

## Data Files

| File | Location | Git-tracked | Notes |
|------|----------|-------------|-------|
| `repos.json` | `~/.mgitpi/repos.json` | No | Runtime-generated; user's saved repo list |
| All source `.py` files | Project root | Yes | `main.py`, `klm_menu.py`, `art.py`, etc. |

Files that must **never** be committed: none currently (no credentials or large binaries in scope).

---

## Platform Constraints

- **Primary target:** Raspberry Pi OS (Debian Bookworm, 64-bit); headless terminal use
- **Secondary:** Windows 10/11 and Ubuntu LTS
- **Standard library only** — zero pip/runtime dependencies
- `art.clear()` already handles `cls` vs `clear` via `sys.platform`
- Any new OS-specific code must check `sys.platform`, with Linux as the primary path
- No hardware dependencies (GPIO, I2C, serial) — this is a pure software tool

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

## Known Technical Debt

1. All handler functions in `main.py` are `pass`/`print("TODO")` stubs — violates Rule 12 (new menu action must have implementation in `git_ops.py`)
2. No test suite exists — violates Rule 15 (testing)
3. `ui_box.py` not yet created — referenced in Architecture but absent from repo

---

## Development Rules

The following rules apply to all contributions, human or AI-assisted.

**Quick index:**
[1. Separation of Concerns](#1-separation-of-concerns) ·
[2. No External Dependencies](#2-no-external-dependencies) ·
[3. Git via Subprocess](#3-git-operations-via-subprocess) ·
[4. Persistent Data](#4-persistent-data-in-mgitpi) ·
[5. ANSI Colors](#5-ansi-colors-are-optional) ·
[6. Unique Hotkeys](#6-menu-hotkeys-must-be-unique-per-menu) ·
[7. Naming](#7-naming-conventions) ·
[8. Terminal Width](#8-terminal-width-awareness) ·
[9. Error Handling](#9-error-handling-principles) ·
[10. No Hardcoded Paths](#10-no-hardcoded-usernames-or-paths) ·
[11. Cross-Platform](#11-cross-platform-awareness) ·
[12. New Action](#12-adding-a-new-menu-action) ·
[13. New Menu](#13-adding-a-new-menu) ·
[14. Commit Style](#14-commit-message-style) ·
[15. Testing](#15-testing)

---

### 1. Separation of Concerns

| Layer | Belongs in |
|-------|------------|
| UI logic | `art.py`, `klm_menu.py`, `ui_box.py` |
| Git logic | `git_ops.py` only |
| Persistence logic | `repo_manager.py` only |
| Routing | `main.py` only |

`main.py` is the router only — it calls into other modules; it does not contain
Git commands, file I/O, or rendering code.

> Never put `subprocess` calls in `main.py`. Never put menu definitions outside `main.py`.

### 2. No External Dependencies

The project must run with Python 3.10+ standard library and a system `git`
install only. Do not add `requirements.txt`, `pip install` steps, or any
third-party packages. If something seems to need an external library, implement
the minimal needed subset from scratch.

### 3. Git Operations via Subprocess

All Git commands must go through `subprocess.run()` or `subprocess.Popen()`
with:

- `capture_output=True`
- `text=True`
- Explicit error checking (check `returncode`)
- Errors returned to the caller, not printed directly

**Example pattern:**

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

| Convention | Reserved for |
|------------|--------------|
| First letter of action | e.g. `s` → Status, `c` → Commit |
| `b` | Back navigation (always) |
| `x` or `q` | Exit/Quit at top-level menu |

### 7. Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Functions | `snake_case` | `clone_repo_ssh` |
| Internal helpers | `_leading_underscore` | `_c` |
| Module-level constants | `UPPER_CASE` | `ANSI` |
| Menu `name` keys | lowercase, no spaces | `"branch_tools"` |

### 8. Terminal Width Awareness

Never hardcode a line width. Always use `art.term_width()` or the `width` key
from the menu dict. Respect terminals as narrow as 60 columns. Use
`art.center()` for centering; never manually count spaces.

### 9. Error Handling Principles

- Git command errors must be shown to the user in a clear, plain-English message. Do not dump raw stderr.
- Invalid menu input re-prompts silently — do not print an error, just loop.
- Missing config files (`repos.json`) must be created automatically on first run with safe defaults. Never crash on a missing file.
- Functions that can fail must return `(result, error)` tuples, not raise unhandled exceptions.

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
5. **Never skip step 3** — don't put Git logic in `main.py`.

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

Do not use vague messages like `"fix stuff"`, `"update code"`, or `"changes"`.

Always add the co-author trailer:
```
Co-authored-by: kl mithunvel <klm@smtw.in>
```

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

## Project TODO List

Legend: 🔴 Bug / rule violation  |  🟡 Incomplete feature  |  🟢 Not started  |  ✅ Done

### CRITICAL
- 🔴 All `main.py` handler stubs are unimplemented (Rule 12 violation) — implement via `git_ops.py` / `repo_manager.py`
- 🔴 No test suite (Rule 15 violation)

### HIGH
- 🟡 `git_ops.py` — implement: `git_status`, `git_add_interactive`, `git_commit`, `git_push`, `git_pull`
- 🟡 `git_ops.py` — implement: `git_list_branches`, `git_checkout`, `git_create_branch`, `git_delete_branch`
- 🟡 `git_ops.py` — implement: `git_stash`, `git_stash_pop`, `git_log`, `git_diff`, `git_reset`
- 🟡 `repo_manager.py` — implement: `load_repos`, `add_repo`, `remove_repo`, `validate_repos`
- 🟡 Wire all `main.py` stubs to their `git_ops` / `repo_manager` implementations

### MEDIUM
- 🟢 Create `ui_box.py` with reusable UTF-8 box-drawing components
- 🟢 Add `tests/` directory with pytest suite covering all `git_ops.py` functions
- 🟢 Implement clone-SSH workflow with URL + target-path input

### NOT STARTED
- 🟢 Commit log viewer (formatted `git log` output in a scrollable box)
- 🟢 Interactive `git diff` viewer

### DONE
- ✅ Splash screen with animated ASCII art and ANSI colors
- ✅ Menu engine (`klm_menu.py`) — hotkey nav, back nav, input validation
- ✅ All menu structure definitions in `main.py`
- ✅ Terminal width detection and responsive layout
- ✅ `art.py` — ANSI helpers, `clear()`, `center()`, `term_width()`

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

| Principle | Meaning |
|-----------|---------|
| **Simple** | One screen at a time, one action per keypress |
| **Lightweight** | Zero runtime dependencies beyond Python and Git |
| **Readable** | Clear module boundaries, short functions, obvious names |
| **Resilient** | Never crash on missing files, bad input, or Git errors |
| **Expandable** | Every new feature fits cleanly into the existing pattern |

---

## User Rules

### Standard User Rules

#### Companion Files

Claude must maintain two files in every project root alongside `CLAUDE.md`. Create them on the first session if they do not exist.

**`TODO.md` — Task Tracker**

Tracks what has been done and what still needs doing. Update it whenever a task is started, completed, or discovered.

Rules:
- Move items from **Not Started → In Progress → Done** as work progresses. Never delete entries; they are the audit trail.
- Add newly discovered tasks immediately — do not hold them until the end of a session.
- Link to the relevant commit hash next to Done items where possible.

**`CLAUDE-LOG.md` — Session Log**

Records what was actually done, session by session. Append a new entry at the start of every session and fill it in as work proceeds.

Format:
```
## YYYY-MM-DD — <one-line session summary>
- <action taken and outcome>
- <files changed and why>
- <decisions made and rationale>
- <anything left incomplete and why>
```

Rules:
- One dated entry per session.
- Keep entries factual and concise — focus on *what changed* and *why*.
- Both files must be committed alongside any code changes they describe.

#### Deployment Model

**The hard rule: write and test on the development machine first. Hardware comes last.**

Stages — always in this order:
1. **Code on dev machine** — write all logic on the laptop/desktop (no GPIO, no I2C, no serial).
2. **Test on dev machine** — run the full test suite. Fix all failures before moving on.
3. **Review for hardware impact** — state which parts touch real hardware vs pure logic.
4. **Deploy to hardware** — only after steps 1–3 are complete.
5. **Verify on hardware** — run the hardware-specific test. If discrepancy, fix on dev machine (step 1) and repeat.

Rules:
- Never hardcode hardware addresses, port names, or pin numbers in driver files — they go in `config.yaml`.
- When proposing a change, always separate: (a) logic verifiable on dev machine, (b) hardware-specific parts.
- Never instruct the user to "just run it on the device" as a substitute for a dev-machine test.

#### Commands & Workflow

- No virtualenv needed for MGitPi (standard library only).
- Run `python3 -m py_compile` on all changed files before every commit.
- Run `pytest tests/` before every commit once the test suite exists.

---

### Personal Preferences (from PROJ_STARTER.md)

#### Interaction Rules

- **Every git commit must include a co-author trailer** for `kl mithunvel <klm@smtw.in>`. Add the following line at the end of every commit message body (after a blank line):
  ```
  Co-authored-by: kl mithunvel <klm@smtw.in>
  ```

- **Always explain before acting.** Before making any code changes, edits, or file writes, describe exactly what you are going to do and wait for explicit confirmation from the user. List every file that will be changed and what will change in each. Do not proceed until the user says to go ahead.

#### Software Engineering Preferences

- **DRY:** Extract shared logic into reusable functions.
- **Testing is important:** Write tests for new functionality. Use `pytest`; tests live in `tests/`.
- **Explicit over implicit:** Clear, readable code. No magic numbers, obscure one-liners, or hidden side effects.
- **Proper error handling:** Handle errors at the right level. Return meaningful messages. Don't swallow exceptions.
- **No deprecated APIs:** Never use deprecated APIs, functions, or modules. Rewrite to avoid after consulting the user.

#### General Principles

- **Simplicity first:** Minimal, straightforward code. No over-engineering.
- **Explain always:** Document decisions and how things work.
- **Backend-heavy:** Prefer logic in the backend; keep frontends thin.

#### Tech Stack Preferences

| Layer | Choice | Notes |
|-------|--------|-------|
| Languages | Python (latest stable) | |
| Python GUI | Tkinter | When a desktop UI is needed |
| Database | SQLite | For any future data needs |
| Configuration | YAML | For all settings and config files |
| Infrastructure | Raspberry Pi OS, Debian, Ubuntu LTS, Windows | Guard OS-specific code |

#### Commit Message Style

Use imperative mood, short subject line (≤ 72 chars), no trailing period. Always include co-author trailer (see Interaction Rules above).

---

### Project-Specific Overrides

- Consult `CLAUDE/project.md` before adding or changing any menu structure — it is the authoritative full menu flow specification.
- No virtualenv is needed (standard library only); skip any virtualenv activation steps from Standard User Rules.
- All persistent state goes in `~/.mgitpi/` — never write into the project directory at runtime.
