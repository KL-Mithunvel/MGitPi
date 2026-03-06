# MGitPi

A modular, menu-driven, cyber-styled Git Control Interface for Raspberry Pi.
Built for streamlined Git workflows on embedded Linux systems, especially Raspberry Pi.

MGitPi provides a clean, structured CLI menu system with a fully customizable ASCII-art
splash screen, persistent repository management, and safe wrappers for Git operations —
all using a modular Python architecture.

---

## Project Overview

MGitPi aims to simplify Git operations on Raspberry Pi by providing:

- A clean TUI/CLI interface inspired by tools like KIAUH
- Easy navigation across Git repositories
- Persistent management of repo paths
- SSH-based cloning support
- A consistent menu framework (`klm_menu.py`)
- Custom UI rendering with box-drawing characters
- A cyber-styled ASCII splash screen (`art.py`)

Designed to be extensible, with all UI logic isolated from core Git operations.

---

## Architecture

The project is divided into the following modules:

```
MGitPi/
│
├── main.py            # Main entry point, loads splash + menu system
├── klm_menu.py        # Core menu engine (rendering + navigation)
├── art.py             # Splash screen + branding banners
├── repo_manager.py    # Load/save repo list, validate repo paths
├── git_ops.py         # Wrapper around git commands
├── ui_box.py          # Box-drawing utilities for UI components
└── README.md
```

### Module Descriptions

| File | Responsibility |
|------|---------------|
| `main.py` | Starts the app, displays splash, loads main menu, maps actions |
| `klm_menu.py` | Custom menu engine (hotkeys, back navigation, looping) |
| `art.py` | Splash screen generation, cyber ASCII art, branding |
| `ui_box.py` | Builds borders, menus, input boxes using UTF-8 line art |
| `repo_manager.py` | Handles persistent repo list storage + validation |
| `git_ops.py` | Executes Git commands safely with subprocess |

---

## UI / UX Design

MGitPi uses:

- UTF-8 box-drawing characters
- Cyan-themed cyber aesthetic
- A large custom ASCII splash ("MGitPi")
- Animated intro (optional delay)

Example of the UI layout:

```
┌───────────────────────────────────────────────────────┐
│                     [ Menu ]                          │
│ 1) Open repo from saved list                      (o) │
│ 2) Clone new repo (SSH)                           (c) │
│ 3) Add repo to saved list                         (a) │
│ 4) Remove repo from list                          (r) │
│ 5) Validate repo list                             (v) │
│ 6) Exit                                           (x) │
└───────────────────────────────────────────────────────┘
Perform action >>
```

---

## Core Features

### Persistent repository list

Stored in JSON at `~/.mgitpi/repos.json`. Developers can:

- Add repo paths
- Remove repo paths
- Validate missing/moved repos

### Git operations (via `git_ops.py`)

Supported actions:

- `git status`
- `git add` (interactive choose-files mode)
- `git commit -m ""`
- `git push`
- `git pull`
- `git clone` (SSH/PAT)

All operations use `subprocess.run()` with error handling.

### Open Repo Workflows

Two ways to open a repo:

1. **Open from saved list** — Menu shows numbered repositories stored in JSON.
2. **Open by path (one-time)** — User enters a path, not added to saved list.

### Cyber Splash Screen

Stored in `art.py`. Displays:

```
███╗   ███╗ ██████╗ ██╗████████╗
████╗ ████║██╔════╝ ██║╚══██╔══╝
██╔████╔██║██║  ███╗██║   ██║
██║╚██╔╝██║██║   ██║██║   ██║
██║ ╚═╝ ██║╚██████╔╝██║   ██║
╚═╝     ╚═╝ ╚═════╝ ╚═╝   ╚═╝
```

With "WELCOME KLM", "Project: MGitPi", and "Made by: mithunvel-kl". Auto-clears after a delay.

---

## Installation / Setup

### Prerequisites

- Python 3.10+
- Git installed
- Raspberry Pi OS or any Linux

### Install

```bash
git clone <this repo>
cd MGitPi
python3 main.py
```

---

## How to Add New Git Actions

All Git logic lives in `git_ops.py`. Example — adding a `git fetch` function:

```python
def git_fetch(path):
    return run_git(["fetch"], path)
```

Then map it inside the relevant menu in `main.py`.

---

## How the Menu System Works

`klm_menu.py` defines structured dictionary menus. Example:

```python
main_menu = {
    "menu": "Workspace Menu",
    "name": "workspace",
    "options": [
        ["open_saved", "Open repo (saved list)", "o"],
        ["clone_repo", "Clone new repo (SSH)", "c"],
        ["add_repo",   "Add repo to list",      "a"],
        ["exit",       "Exit",                  "x"]
    ],
    "back_option": False
}
```

Menu navigation:

```python
cmd, menu_name = klm_menu.present_menu("workspace", menu_system)
```

The returned command triggers the matching handler function in `main.py`.

---

## Repo Storage Format

`repo_manager.py` writes JSON:

```json
{
  "repos": [
    "/home/pi/project1",
    "/home/pi/project2"
  ]
}
```

Missing repos are automatically flagged during validation.

---

## Developer Notes

- Always keep UI logic in `ui_box.py` or `art.py`
- Avoid mixing Git logic with menus
- Git subprocess outputs must be captured and returned, not printed directly
- Add new menus by extending the `menu_system` dict in `main.py`

---

## Future Expansion

Planned additions:

- Branch management UI
- Rebase + merge UI
- Stash & stash-pop workflows
- Remote viewer
- Repo-wide search
- Built-in SSH key wizard
- Commit diff viewer
- Real ANSI animations for loading

---

## Menu Flow Specification

This section documents every menu, how they connect, and what each option triggers.
It is the authoritative reference for integrating new features or expanding the CLI.

---

### 1. System Overview

MGitPi has three main components:

1. **Splash Screen** (`art.py`)
2. **Main Menu System** (driven by `klm_menu.py`)
3. **Action Handlers** (Git ops, repo manager)

Core loop:

```
splash()
→ main_menu
→ submenu (optional)
→ action function
→ return to menu
```

---

### 2. Menu Architecture

```
Splash Screen
      ↓
Workspace Menu  (MAIN MENU)
      ↓
Repo Selection Menu (if opened)
      ↓
Repo Actions Menu (status/add/commit/push/etc.)
```

---

### 3. Workspace Menu (Main Menu)

Displayed immediately after splash.

```
┌───────────────────────────────────────────────────────────────┐
│ [ Menu ]                                                      │
│ 1) Open repo (from saved list)                     (o)        │
│ 2) Open repo by path (one-time)                    (p)        │
│ 3) Clone new repo (SSH)                            (c)        │
│ 4) Add repo to saved list                          (a)        │
│ 5) Remove repo from saved list                     (r)        │
│ 6) Validate saved repo list                        (v)        │
│ 7) Exit                                            (x)        │
└───────────────────────────────────────────────────────────────┘
Perform action >>
```

| Hotkey | Action | Goes to |
|--------|--------|---------|
| `o` | Open repo from saved list | Saved Repo List Menu |
| `p` | Open a repo by entering path | Repo Actions Menu |
| `c` | Clone new repo (SSH) | Clone Workflow |
| `a` | Add repo to saved list | Path Input |
| `r` | Remove repo from saved list | Removal Menu |
| `v` | Validate saved repo list | Validation Output |
| `x` | Exit to shell | Terminates program |

---

### 4. Saved Repo List Menu

Only appears when choosing "Open repo from saved list".

```
┌──────────────────────────────────────────────────┐
│ Saved Repositories                               │
│ Select a repository to open:                     │
│                                                  │
│ 1) /home/pi/project1                             │
│ 2) /home/pi/myrobot                              │
│ 3) /home/pi/HERC-26                              │
│                                                  │
│ b) Back                                          │
└──────────────────────────────────────────────────┘
Perform action >>
```

| Input | Action |
|-------|--------|
| number | Opens repo → Repo Actions Menu |
| `b` | Returns to Workspace Menu |

---

### 5. Repo Actions Menu

Displayed after selecting or entering a repo path.

```
┌──────────────────────────────────────────────────┐
│ Repo: /path/to/repo                              │
│──────────────────────────────────────────────────│
│ 1) Status                                     (s)│
│ 2) Add files (interactive)                    (a)│
│ 3) Commit                                     (c)│
│ 4) Push                                       (p)│
│ 5) Pull                                       (u)│
│ 6) List branches                              (b)│
│ 7) Checkout branch                            (h)│
│ 8) Go Back                                    (x)│
└──────────────────────────────────────────────────┘
Perform action >>
```

| Option | Description | Calls |
|--------|-------------|-------|
| Status | `git status` | `git_ops.git_status()` |
| Add files | Shows changed files, user selects | `git_ops.git_add_interactive()` |
| Commit | Prompts for message | `git_ops.git_commit()` |
| Push | `git push` | `git_ops.git_push()` |
| Pull | `git pull` | `git_ops.git_pull()` |
| List branches | `git branch -a` | `git_ops.git_list_branches()` |
| Checkout branch | Input branch name | `git_ops.git_checkout()` |
| Back | Return to previous menu | — |

---

### 6. Add Repo to Saved List

```
User enters a path
  → repo_manager.add_repo()
  → Repo saved in repos.json
  → Return to Workspace Menu
```

Validation rules:

- Path must exist
- Must contain a `.git` folder
- Normalized to absolute path

---

### 7. Remove Repo

Menu generated dynamically from `repos.json`:

```
1) /path/A
2) /path/B
3) /path/C
b) Back
```

Selecting a number removes that entry from JSON.

---

### 8. Validate Repo List

Scans every entry in `repos.json`:

- Missing directories are flagged
- Missing `.git` folder is flagged
- Broken symlinks are flagged

Output example:

```
[ OK ] /home/pi/project1
[ERR] /home/pi/old_project  (missing)
```

---

### 9. Clone New Repo (SSH)

```
Ask for SSH URL
  → Ask for destination folder
  → Run git clone
  → Return to Workspace Menu
```

Supports URLs in the form `git@github.com:user/repo.git`.

---

### 10. Repo Manager Behavior

Location: `~/.mgitpi/repos.json`

```json
{
  "repos": [
    "/home/pi/project1",
    "/home/pi/project2"
  ]
}
```

All repo-related menus depend on this file.

---

### 11. Full Navigation Map

```
                ┌──────────────────────┐
                │    Splash Screen     │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │   Workspace Menu     │
                └──────┬───────────────┘
       ┌───────────────┼──────────────────┬────────────┬──────────────┐
       ↓               ↓                  ↓            ↓              ↓
Saved Repo Menu  Open Path Menu     Clone SSH     Add Repo      Remove Repo
       │               │                 │
       └───────────────┴─────────────────┘
                       ↓
              Repo Actions Menu
                       │
                       └──→ Back → Workspace Menu
```

---

### 12. Developer Integration Checklist

**Add new Git features:**
1. Edit `git_ops.py`
2. Add option to the Repo Actions Menu in `main.py`
3. Map the command in `main.py`

**Add new top-level features:**
1. Extend `workspace_menu` in `main.py`
2. Add supporting submenu to `menu_system`

**Modify splash:**
- Edit `art.py` → `splash()`

**Modify UI rendering:**
- Edit `ui_box.py`

**Add persistent data:**
- Add to `repo_manager.py`
- Store under `~/.mgitpi/`

---

### 13. UX Rules

- Backtracking is always possible via Back menu options
- Only the Workspace Menu has Exit
- Input prompt always ends with `Perform action >>`
- All box drawing uses UTF-8 characters
- Width auto-scales to terminal width
- Git logic must never appear in `main.py`
