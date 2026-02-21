
# MGitPi

A modular, menu-driven, cyber-styled Git Control Interface for Raspberry Pi.
Built for streamlined Git workflows on embedded Linux systems, especially Raspberry Pi.

MGitPi provides a clean, structured CLI menu system with a fully customizable ASCII-art splash screen, persistent repository management, and safe wrappers for Git operations — all using a modular Python architecture.



📌 Project Overview

MGitPi aims to simplify Git operations on Raspberry Pi by providing:
	•	A clean TUI/CLI interface inspired by tools like KIAUH
	•	Easy navigation across Git repositories
	•	Persistent management of repo paths
	•	SSH-based cloning support
	•	A consistent menu framework (klm_menu.py)
	•	Custom UI rendering with box-drawing characters
	•	A cyber-styled ASCII splash screen (art.py)

Designed to be extensible, with all UI logic isolated from core Git operations.


🧩 Architecture

The project is divided into the following modules:

MGitPi/
│
├── main.py            # Main entry point, loads splash + menu system
├── klm_menu.py        # Core menu engine (rendering + navigation)
├── art.py             # Splash screen + branding banners
├── repo_manager.py    # Load/save repo list, validate repo paths
├── git_ops.py         # Wrapper around git commands
├── ui_box.py          # Box-drawing utilities for UI components
└── README.md

Descriptions

File	Responsibility
main.py	Starts the app, displays splash, loads main menu, maps actions.
klm_menu.py	Custom menu engine (hotkeys, back navigation, looping).
art.py	Splash screen generation, cyber ASCII art, branding.
ui_box.py	Builds borders, menus, input boxes using UTF-8 line art.
repo_manager.py	Handles persistent repo list storage + validation.
git_ops.py	Executes Git commands safely with subprocess.



🎨 UI / UX Design

MGitPi uses:
	•	UTF-8 box-drawing characters
	•	Cyan-themed cyber aesthetic
	•	A large custom ASCII splash (“MGitPi”)
	•	Animated intro (optional delay)

Example of the UI layout:

┌───────────────────────────────────────────────────────┐
│                     [ Menu ]                          │
│ 1) Open repo from saved list                      (o) │
│ 2) Clone new repo (SSH)                           (c) │
│ 3) Add repo to saved list                         (a) │
│ 4) Remove repo from list                          (r) │
│ 5) Validate repo list                              (v) │
│ 6) Exit                                            (x) │
└───────────────────────────────────────────────────────┘
Perform action >>


🛠 Core Features

✔ Persistent repository list

Stored in JSON:

~/.mgitpi/repos.json

Developers can:
	•	Add repo paths
	•	Remove repo paths
	•	Validate missing/moved repos


✔ Git operations (through git_ops.py)

Current supported actions:
	•	git status
	•	git add (interactive choose-files mode)
	•	git commit -m “”
	•	git push
	•	git pull
	•	git clone (PAT)

All operations use subprocess.run() with error handling.



✔ Open Repo Workflows

There are two ways to open a repo:
	1.	Open from saved list
— Menu shows numbered repositories stored in JSON.
	2.	Open by path (one-time)
— User enters a path, not added to saved list.



✔ Cyber Splash Screen

Stored in art.py.
Shows something like:

███╗   ███╗ ██████╗ ██╗████████╗
████╗ ████║██╔════╝ ██║╚══██╔══╝
██╔████╔██║██║  ███╗██║   ██║
██║╚██╔╝██║██║   ██║██║   ██║
██║ ╚═╝ ██║╚██████╔╝██║   ██║
╚═╝     ╚═╝ ╚═════╝ ╚═╝   ╚═╝
               

With:
	•	“WELCOME KLM 🎶”
	•	“Project: MGitPi”
	•	“Made by: mithunvel-kl”

Then auto-clears after a delay.



⚙ Installation / Setup

Prerequisites
	•	Python 3.10+
	•	Git installed
	•	Raspberry Pi OS or any Linux

Install

git clone <this repo>
cd MGitPi
python3 main.py




🧪 How to Add New Git Actions

All Git logic lives in:

git_ops.py

Example: Adding a “git fetch” function

def git_fetch(path):
    return run_git(["fetch"], path)

Then map it inside the menu in main.py.



🧱 How the Menu System Works

klm_menu.py defines structured dictionary menus.

Example:

main_menu = {
    "menu": "Workspace Menu",
    "name": "workspace",
    "options": [
        ["open_saved", "Open repo (saved list)", "o"],
        ["clone_repo", "Clone new repo (SSH)", "c"],
        ["add_repo", "Add repo to list", "a"],
        ["exit", "Exit", "x"]
    ],
    "back_option": False
}

Menu navigation flow:

cmd, menu_name = klm_menu.present_menu("workspace", menu_system)

Returned command triggers functions in main.py.



📁 Repo Storage Format

repo_manager.py writes JSON like:

{
  "repos": [
    "/home/pi/project1",
    "/home/pi/project2"
  ]
}

Missing repos automatically flagged during validation.



🔧 Developer Notes
	•	Always keep UI logic in ui_box.py or art.py
	•	Avoid mixing Git logic with menus
	•	Git subprocess outputs must be captured and colorized carefully
	•	Add new menus by extending menu_system dict



📌 Future Expansion

Your next developers can implement:

Planned Additions:
	•	Branch management
	•	Rebase + merge UI
	•	Stash & stash-pop
	•	Remote viewer
	•	Repo-wide search
	•	Built-in SSH key wizard
	•	Commit diff viewer
	•	Real ANSI animations for loading

Below is a clear, complete, developer-ready “Menu Flow Specification” for MGitPi.
This documents EVERY menu discussed so far, how they connect, and what each option triggers.
This is meant for another developer to take over instantly and continue integration.

You can paste this into README.md (as an extension section) or save as MENU_FLOW.md.

⸻

MGitPi – Full Menu Flow Specification

This document describes the full navigation architecture, all menu screens, all hotkeys, and the action flow of MGitPi.

It is the authoritative reference for integrating new features or expanding the CLI.

⸻

1. System Overview

MGitPi has 3 main components:
	1.	Splash Screen (from art.py)
	2.	Main Menu System (driven by klm_menu.py)
	3.	Action Handlers (Git ops, repo manager)

The core loop is:

splash()  
→ main_menu  
→ submenu (optional)  
→ action function  
→ return to menu  


⸻

2. Menu Architecture (Tree Structure)

2.1 Top-Level Flow

Splash Screen
      ↓
Workspace Menu  (MAIN MENU)
      ↓
Repo Selection Menu (if opened)
      ↓
Repo Actions Menu (status/add/commit/push/etc.)


⸻

3. Workspace Menu (MAIN MENU)

Displayed immediately after splash.

┌───────────────────────────────────────────────────────────────┐
│ [ Menu ]                                                      │
│ 1) Open repo (from saved list)                     (o)        │
│ 2) Open repo by path (one-time)                    (p)        │
│ 3) Clone new repo (SSH)                            (c)        │
│ 4) Add repo to saved list                          (a)        │
│ 5) Remove repo from saved list                     (r)        │
│ 6) Validate saved repo list                        (v)        │
│ 7) Exit                                             (x)        │
└───────────────────────────────────────────────────────────────┘
Perform action >>

Options → Results

Hotkey	Action	Goes to
o	Open repo from saved list	→ Saved Repo List Menu
p	Open a repo by entering path	→ Repo Actions Menu
c	Clone new repo (SSH)	→ Clone Workflow
a	Add repo to saved list	→ Path Input
r	Remove repo from saved list	→ Removal Menu
v	Validate saved repo list	→ Validation Output
x	Exit to shell	Terminates program


⸻

4. Saved Repo List Menu

Only appears when choosing Open repo (from saved list).

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

Options → Results

Input	Action
number	Opens repo → Repo Actions Menu
b	Returns to Workspace Menu


⸻

5. Repo Actions Menu (per repo)

Displayed after selecting or entering a repo path.

┌──────────────────────────────────────────────────┐
│ Repo: /path/to/repo                               │
│--------------------------------------------------│
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

Actions → Functions

Option	Description	Calls
Status	git status	git_ops.git_status()
Add files interactively	Shows changed files → user selects	git_ops.git_add_interactive()
Commit	Prompts for message	git_ops.git_commit()
Push	git push	git_ops.git_push()
Pull	git pull	git_ops.git_pull()
List branches	git branch -a	git_ops.git_list_branches()
Checkout branch	Input branch name	git_ops.git_checkout()
Back	→ back to previous menu	returns


⸻

6. Add Repo to Saved List

Workflow:

User enters a path → repo_manager.add_repo() →
Repo saved in repos.json → return to Workspace Menu

Validation rules:
	•	Path must exist
	•	Must contain a .git folder
	•	Normalized to absolute path

⸻

7. Remove Repo

Menu generated dynamically:

1) /path/A
2) /path/B
3) /path/C
b) Back

Selecting number removes entry from JSON.

⸻

8. Validate Repo List

Runs through repos.json:
	•	Missing directories flagged
	•	Missing .git folder flagged
	•	Broken symlinks flagged

Output example:

[ OK ] /home/pi/project1
[ERR] /home/pi/old_project (missing)

User returns to Workspace Menu.

⸻

9. Clone New Repo (SSH)

Workflow:

Ask for SSH URL →
Ask for folder to clone into →
Run git clone →
Return to Workspace Menu

Supports:

git@github.com:user/repo.git


⸻

10. Repo Manager Behavior

Location:

~/.mgitpi/repos.json

Structure:

{
  "repos": [
    "/home/pi/project1",
    "/home/pi/project2"
  ]
}

All repo-related menus depend on this file.

⸻

11. Full Navigation Map (Graph Form)

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
       │               │                    │               │                 │
       └─────→ Repo Actions Menu  ←─────────┘               │                 │
                       │                                     │                 │
                       └──────────────→ Back ───────────────┘                 │
                                                                               │
                                                                               └→ Validate → Back


⸻

12. Developer Integration Checklist

To extend the system:

✔ Add new Git features

→ edit git_ops.py
→ add option to Repo Actions Menu
→ map command in main.py

✔ Add new top-level features

→ extend workspace_menu in main.py
→ add supporting submenu in menu_system

✔ Modify splash

→ edit art.py → splash()

✔ Modify UI rendering

→ edit ui_box.py

✔ Add persistent data

→ add to repo_manager.py
→ store in ~/.mgitpi/

⸻

13. Known UX Rules
	•	Backtracking is always possible via ← Back menus
	•	Only Workspace Menu has Exit
	•	Input prompt always ends with:

Perform action >>



⸻

14. Developer Notes
	•	All box drawing must use UTF-8
	•	Width auto-scales using terminal width
	•	Do not write Git logic in main.py
	•	Keep UI independent so MGitPi can run with different skins later
	•	Avoid blocking loops inside Git functions

