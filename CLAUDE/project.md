# MGitPi – Full Menu Flow Specification

This document describes the full navigation architecture, all menu screens, all hotkeys, and the action flow of MGitPi.

It is the authoritative reference for integrating new features or expanding the CLI.

---

## 1. System Overview

MGitPi has 3 main components:

| Component | Source |
|-----------|--------|
| Splash Screen | `art.py` |
| Main Menu System | `klm_menu.py` |
| Action Handlers | Git ops, repo manager |

The core loop is:

```
splash()
  → main_menu
  → submenu (optional)
  → action function
  → return to menu
```

---

## 2. Menu Architecture (Tree Structure)

### 2.1 Top-Level Flow

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

## 3. Workspace Menu (MAIN MENU)

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

### Options → Results

| Hotkey | Action | Goes to |
|--------|--------|---------|
| `o` | Open repo from saved list | → Saved Repo List Menu |
| `p` | Open a repo by entering path | → Repo Actions Menu |
| `c` | Clone new repo (SSH) | → Clone Workflow |
| `a` | Add repo to saved list | → Path Input |
| `r` | Remove repo from saved list | → Removal Menu |
| `v` | Validate saved repo list | → Validation Output |
| `x` | Exit to shell | Terminates program |

---

## 4. Saved Repo List Menu

Only appears when choosing **Open repo (from saved list)**.

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

### Options → Results

| Input | Action |
|-------|--------|
| number | Opens repo → Repo Actions Menu |
| `b` | Returns to Workspace Menu |

---

## 5. Repo Actions Menu (per repo)

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

### Actions → Functions

| Option | Description | Calls |
|--------|-------------|-------|
| Status | `git status` | `git_ops.git_status()` |
| Add files interactively | Shows changed files → user selects | `git_ops.git_add_interactive()` |
| Commit | Prompts for message | `git_ops.git_commit()` |
| Push | `git push` | `git_ops.git_push()` |
| Pull | `git pull` | `git_ops.git_pull()` |
| List branches | `git branch -a` | `git_ops.git_list_branches()` |
| Checkout branch | Input branch name | `git_ops.git_checkout()` |
| Back | → back to previous menu | returns |

---

## 6. Add Repo to Saved List

**Workflow:**

```
User enters a path
  → repo_manager.add_repo()
  → Repo saved in repos.json
  → return to Workspace Menu
```

**Validation rules:**

- Path must exist
- Must contain a `.git` folder
- Normalized to absolute path

---

## 7. Remove Repo

Menu generated dynamically:

```
1) /path/A
2) /path/B
3) /path/C
b) Back
```

Selecting a number removes the entry from the JSON file.

---

## 8. Validate Repo List

Runs through `repos.json` and flags:

- Missing directories
- Missing `.git` folder
- Broken symlinks

**Output example:**

```
[ OK ] /home/pi/project1
[ERR] /home/pi/old_project (missing)
```

User returns to Workspace Menu after review.

---

## 9. Clone New Repo (SSH)

**Workflow:**

```
Ask for SSH URL
  → Ask for folder to clone into
  → Run git clone
  → Return to Workspace Menu
```

**Supported URL format:**

```
git@github.com:user/repo.git
```

---

## 10. Repo Manager Behavior

**Location:**

```
~/.mgitpi/repos.json
```

**Structure:**

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

## 11. Full Navigation Map

```
                ┌──────────────────────┐
                │      Splash Screen   │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │   Workspace Menu     │
                └──────┬───────────────┘
       ┌───────────────┼─────────────────────┬────────────────────────────┐
       ↓               ↓                     ↓                            ↓
Saved Repo Menu   Open Path Menu       Clone SSH        Add Repo         Remove Repo
       │               │                    │               │                 │
       └─────→ Repo Actions Menu  ←─────────┘               │                 │
                       │                                     │                 │
                       └──────────────→ Back ───────────────┘                 │
                                                                               │
                                                             Validate → Back ←─┘
```

---

## 12. Developer Integration Checklist

### Add new Git features

1. Edit `git_ops.py`
2. Add option to Repo Actions Menu
3. Map command in `main.py`

### Add new top-level features

1. Extend `workspace_menu` in `main.py`
2. Add supporting submenu in `menu_system`

### Modify splash

- Edit `art.py` → `splash()`

### Modify UI rendering

- Edit `ui_box.py`

### Add persistent data

1. Add to `repo_manager.py`
2. Store in `~/.mgitpi/`

---

## 13. Known UX Rules

- Backtracking is always possible via ← Back menus
- Only Workspace Menu has Exit
- Input prompt always ends with:

```
Perform action >>
```

---

## 14. Developer Notes

- All box drawing must use UTF-8
- Width auto-scales using terminal width
- Do not write Git logic in `main.py`
- Keep UI independent so MGitPi can run with different skins later
- Avoid blocking loops inside Git functions