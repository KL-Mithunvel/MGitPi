# MGitPi

A modular, menu-driven, cyber-styled Git Control Interface for Raspberry Pi.

Built for streamlined Git workflows on embedded Linux systems, MGitPi wraps common
Git operations in a clean keyboard-driven terminal UI — inspired by tools like
[KIAUH](https://github.com/dw-0/kiauh) — so you can manage repositories on a
headless Raspberry Pi without needing a browser or GUI.

---

## Quick Start

**Requirements:** Python 3.10+, Git installed, any Linux terminal (60+ columns wide)

```bash
git clone <this-repo>
cd MGitPi
python3 main.py
```

No `pip install` required. The project uses the Python standard library only.

---

## Project Overview

MGitPi provides:

- A clean TUI/CLI interface with hotkey navigation
- Persistent repository list stored in `~/.mgitpi/repos.json`
- SSH-based repo cloning
- A modular menu framework (`klm_menu.py`) that keeps UI separate from logic
- Custom UTF-8 box-drawing UI components
- A cyber-styled ASCII splash screen (`art.py`)

---

## Architecture

### Module Responsibilities

| File              | Status      | Role                                                                      |
|-------------------|-------------|---------------------------------------------------------------------------|
| `main.py`         | Active      | Entry point — defines all menus and routes user choices to handlers       |
| `klm_menu.py`     | Active      | Menu engine — renders menus, reads hotkeys, drives navigation             |
| `art.py`          | Active      | Splash screen, ASCII logo, ANSI color helpers, terminal utilities         |
| `repo_manager.py` | Planned     | Persistent repo list at `~/.mgitpi/repos.json`                           |
| `git_ops.py`      | Planned     | Subprocess wrappers for every Git command                                 |
| `ui_box.py`       | Planned     | Reusable UTF-8 box-drawing components                                     |

### Data Flow

```
python3 main.py
  └─► art.splash()                 # Animated welcome screen (5 sec)
  └─► show_menu(menu_system)       # Main routing loop
        └─► klm_menu.present_menu()      # Render + read input
        └─► handler_function()           # Stub or real implementation
                └─► git_ops.*()          # Subprocess Git calls (planned)
                └─► repo_manager.*()     # Persistence (planned)
```

### Persistence

All user data lives in `~/.mgitpi/` (never in the project directory):

```
~/.mgitpi/
└── repos.json    # { "repos": ["/path/to/repo", ...] }
```

---

## Current Status

### Working

- Splash screen with ASCII art logo and ANSI color theming
- Full menu engine: hotkey navigation, back navigation, input validation
- All menu structures defined (workspace, repo, branch, stash, rebase, undo)
- Responsive layout via terminal width detection

### Stubs (defined but not yet implemented)

Every handler in `main.py` currently prints a `TODO` message. These need
implementing in `git_ops.py` and `repo_manager.py`, then wiring into `main.py`:

- Repository: open / clone / add / remove / validate
- Git: status, stage, commit, pull, push
- Branch management: create, switch, delete, merge
- Stash, rebase, and undo operations
- Commit log viewer

---

## UI Design

MGitPi uses:

- UTF-8 box-drawing characters for all borders
- Cyan-themed cyber aesthetic (configurable via `ACCENT_COLOR` in `art.py`)
- A large ASCII splash screen rendered with a built-in block font
- Responsive width — adapts to any terminal ≥ 60 columns

**Splash screen example:**

```
  __  __   ____   _   _  _______  ____   ___
 |  \/  | / ___| | | | ||__   __||  _ \ |_ _|
 | |\/| || |  _  | | | |   | |   | |_) | | |
 | |  | || |_| | | |_| |   | |   |  __/  | |
 |_|  |_| \____|  \___/    |_|   |_|    |___|
```

**Menu example:**

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│════════════════════════════════════════════════════════════════════════════════════════│
│─────────────────────────────── [ MGITPI ] ─────────────────────────────────────────────│
│                        Git Control Interface for Raspberry Pi                          │
│════════════════════════════════════════════════════════════════════════════════════════│
└────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────[ Workspace Menu ]────────────────────────┐
│ Select an option:                                                                      │
│                                                                                        │
│  1) Open repo (from saved list)                                                    (o) │
│  2) Open repo by path (one-time)                                                   (p) │
│  3) Clone new repo (SSH)                                                           (c) │
│  4) Add repo to saved list                                                         (a) │
│  5) Remove repo from saved list                                                    (r) │
│  6) Validate saved repo list                                                       (v) │
│  7) Exit                                                                           (x) │
└────────────────────────────────────────────────────────────────────────────────────────┘

Perform action >>
```

---

## Menu Navigation

MGitPi has six menus organized in a tree:

```
Splash Screen
  └─► Workspace Menu          (main menu)
        ├─► Saved Repo List   (pick from JSON)
        ├─► Open by Path      (one-time entry)
        ├─► Clone SSH         (git clone workflow)
        ├─► Add / Remove Repo (manage JSON list)
        ├─► Validate Repos    (check list health)
        └─► Repo Menu         (per-repo actions)
              ├─► Rebase Tools
              ├─► Branch Tools
              ├─► Stash Tools
              └─► Undo / Cleanup
```

Every menu supports:
- Hotkey input (single character) or number selection
- `b` to go back, `x` to exit (top-level only)
- Re-prompt on invalid input (no error message, just loops)

For the full screen-by-screen specification including all hotkeys and action
mappings, see [`CLAUDE/project.md`](CLAUDE/project.md).

---

## Git Operations

Implemented (target) via `git_ops.py`:

| Action              | Git command              | Handler                          |
|---------------------|--------------------------|----------------------------------|
| Status              | `git status`             | `git_ops.git_status()`           |
| Stage (interactive) | `git add <files>`        | `git_ops.git_add_interactive()`  |
| Commit              | `git commit -m "..."`    | `git_ops.git_commit()`           |
| Push                | `git push`               | `git_ops.git_push()`             |
| Pull                | `git pull`               | `git_ops.git_pull()`             |
| Clone (SSH)         | `git clone`              | `git_ops.git_clone()`            |
| List branches       | `git branch -a`          | `git_ops.git_list_branches()`    |
| Checkout            | `git checkout <branch>`  | `git_ops.git_checkout()`         |

All calls use `subprocess.run()` with `capture_output=True` and explicit
return-code checking. Errors are returned to the caller, not printed directly.

---

## Adding New Features

### New Git action

1. Add a handler stub in `main.py`:
   ```python
   def my_action():
       pass  # TODO
   ```
2. Add the entry to the relevant menu dict in `main.py`:
   ```python
   ["my_action", "My Action Label", "m"],
   ```
3. Implement the logic in `git_ops.py`.
4. Call `git_ops.my_function()` from the stub in `main.py`.

### New menu

1. Define a menu dict in `menu_system` in `main.py`.
2. Add a `"menu:new_menu_name"` navigation entry in the parent menu.
3. Set `"back_to"` to the correct parent menu name.
4. Verify all hotkeys in the new menu are unique within that menu.

### New Git action — subprocess pattern

```python
# in git_ops.py
def git_fetch(path):
    result = subprocess.run(
        ["git", "fetch"],
        capture_output=True, text=True, cwd=path
    )
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None
```

---

## Roadmap

Planned additions for future contributors:

- Branch creation / merge / delete UI
- Interactive rebase workflow
- Stash save / apply / drop
- Remote viewer
- Repo-wide file search
- Built-in SSH key wizard
- Commit diff viewer (inline)
- ANSI loading animations

---

## Developer Reference

Full coding conventions, rules, and architecture decisions are documented in
[`CLAUDE/CLAUDE.md`](CLAUDE/CLAUDE.md). Key principles:

| Principle       | Rule                                                              |
|-----------------|-------------------------------------------------------------------|
| **Simple**      | One screen at a time, one action per keypress                     |
| **Lightweight** | Zero runtime dependencies beyond Python and system Git            |
| **Readable**    | Clear module boundaries, short functions, obvious names           |
| **Resilient**   | Never crash on missing files, bad input, or Git errors            |
| **Expandable**  | Every new feature fits cleanly into the existing pattern          |

**Separation of concerns (strict):**

| Layer            | File(s)                        |
|------------------|--------------------------------|
| UI rendering     | `art.py`, `klm_menu.py`, `ui_box.py` |
| Git logic        | `git_ops.py` only              |
| Persistence      | `repo_manager.py` only         |
| Routing          | `main.py` only                 |

---

## License

MIT © 2026 KL Mithunvel (`mithunvel-kl`)
