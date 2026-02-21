
# MGitPi

A modular, menu-driven, cyber-styled Git Control Interface for Raspberry Pi.
Built for streamlined Git workflows on embedded Linux systems, especially Raspberry Pi.

MGitPi provides a clean, structured CLI menu system with a fully customizable ASCII-art splash screen, persistent repository management, and safe wrappers for Git operations — all using a modular Python architecture.

⸻

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

⸻

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


⸻

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


⸻

🛠 Core Features

✔ Persistent repository list

Stored in JSON:

~/.mgitpi/repos.json

Developers can:
	•	Add repo paths
	•	Remove repo paths
	•	Validate missing/moved repos

⸻

✔ Git operations (through git_ops.py)

Current supported actions:
	•	git status
	•	git add (interactive choose-files mode)
	•	git commit -m “”
	•	git push
	•	git pull
	•	git clone (PAT)

All operations use subprocess.run() with error handling.

⸻

✔ Open Repo Workflows

There are two ways to open a repo:
	1.	Open from saved list
— Menu shows numbered repositories stored in JSON.
	2.	Open by path (one-time)
— User enters a path, not added to saved list.

⸻

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

⸻

⚙ Installation / Setup

Prerequisites
	•	Python 3.10+
	•	Git installed
	•	Raspberry Pi OS or any Linux

Install

git clone <this repo>
cd MGitPi
python3 main.py


⸻

🧪 How to Add New Git Actions

All Git logic lives in:

git_ops.py

Example: Adding a “git fetch” function

def git_fetch(path):
    return run_git(["fetch"], path)

Then map it inside the menu in main.py.

⸻

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

⸻

📁 Repo Storage Format

repo_manager.py writes JSON like:

{
  "repos": [
    "/home/pi/project1",
    "/home/pi/project2"
  ]
}

Missing repos automatically flagged during validation.

⸻

🔧 Developer Notes
	•	Always keep UI logic in ui_box.py or art.py
	•	Avoid mixing Git logic with menus
	•	Git subprocess outputs must be captured and colorized carefully
	•	Add new menus by extending menu_system dict

⸻

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

