# MGitPi — User Guide

**MGitPi** is a keyboard-driven Git interface built for Raspberry Pi.
It lets you manage Git repositories from the terminal without typing raw Git
commands — just press a key and it does the work.

This guide covers everything from first launch to advanced workflows. It also
explains what each Git operation actually does, so you can understand what is
happening behind the scenes.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [The Interface](#2-the-interface)
3. [Workspace Menu](#3-workspace-menu)
4. [Repo Menu](#4-repo-menu)
5. [Branch Tools](#5-branch-tools)
6. [Stash Tools](#6-stash-tools)
7. [Log Viewer](#7-log-viewer)
8. [Undo and Cleanup](#8-undo-and-cleanup)
9. [Git Concepts Explained](#9-git-concepts-explained)
10. [Common Workflows](#10-common-workflows)
11. [SSH Setup Guide](#11-ssh-setup-guide)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Getting Started

### First-time setup

Run the setup script once before launching the app:

```bash
bash setup.sh
```

This will:
- Check that Python 3.10+ and Git are installed
- Create the data folder at `~/.mgitpi/`
- Walk you through SSH key generation and GitHub connection

If the script asks you to edit `secrets/credentials.env`, open it with a text
editor, fill in your GitHub username and SSH key details, then run
`bash setup.sh` again.

### Launching MGitPi

```bash
python3 main.py
```

A splash screen appears for a few seconds, then the main menu loads.

### Exiting

Press `x` from the main Workspace Menu, or press `Ctrl+C` at any time.

---

## 2. The Interface

### How menus work

Every screen shows a box like this:

```
┌─────────────────────────────────[ Workspace Menu ]──────────────────────────┐
│ Select an option:                                                            │
│                                                                              │
│   1)  Open repo (from saved list)                                       (o) │
│   2)  Open repo by path (one-time)                                      (p) │
│   3)  Clone new repo (SSH)                                              (c) │
│   ...                                                                        │
└──────────────────────────────────────────────────────────────────────────────┘

Perform action >>
```

You can answer the `Perform action >>` prompt in two ways:

| Method | Example | What it does |
|--------|---------|--------------|
| Type the hotkey letter | `o` | Selects "Open repo" |
| Type the number | `1` | Same — selects option 1 |

Either way works — use whichever feels natural.

### Going back

Every submenu has a `b) Back` option. Press `b` to return to the previous menu.
You can never get "stuck" — back always works.

### Getting help

Type `?` at any `Perform action >>` prompt to see a description of every
option on that screen. Press Enter to close help and return to the menu.

### Input prompt

The prompt always looks like:

```
Perform action >>
```

After you choose an action, the screen clears and the result is shown. Press
Enter to return to the menu.

---

## 3. Workspace Menu

This is the main menu — it appears right after the splash screen. Everything
in MGitPi starts from here.

```
┌────────────────────────────[ Workspace Menu ]───────────────────────────────┐
│   1)  Open repo (from saved list)                                      (o)  │
│   2)  Open repo by path (one-time)                                     (p)  │
│   3)  Clone new repo (SSH)                                             (c)  │
│   4)  Add repo to saved list                                           (a)  │
│   5)  Remove repo from saved list                                      (r)  │
│   6)  Validate saved repo list                                         (v)  │
│   7)  Exit                                                             (x)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### `o` — Open repo (from saved list)

Shows a numbered list of repositories you have previously saved. Pick one to
open it and enter the Repo Menu for that repository.

**When to use it:** Your day-to-day starting point. Add repositories once with
`a`, then open them quickly with `o` every time after that.

---

### `p` — Open repo by path

Lets you type in the full path to any repository on your Pi. The repo is opened
without being saved to your list.

**When to use it:** When you want to quickly check a repo you don't use often,
without cluttering your saved list.

**Example path:** `/home/pi/my-project`

---

### `c` — Clone new repo (SSH)

Downloads (clones) a repository from GitHub (or another server) to your Pi.
You will be asked for:

1. The **SSH URL** — looks like `git@github.com:username/repo-name.git`
   (find this on GitHub under the green "Code" button → SSH tab)
2. A **destination folder** on your Pi — the repo will be created inside it
   (e.g., type `/home/pi` and the repo appears at `/home/pi/repo-name`)

**What cloning does:** Creates a full local copy of the repository, including
all commits and branches. See [Git Concepts](#9-git-concepts-explained) for more.

**Requires:** SSH key configured and added to GitHub. See
[SSH Setup Guide](#11-ssh-setup-guide).

---

### `a` — Add repo to saved list

Saves a repository path to your permanent list so you can open it with `o`.

You will be asked for the path. MGitPi checks that:
- The path actually exists on disk
- It contains a `.git` folder (confirming it is a Git repository)

**When to use it:** The first time you work with a repository, or after cloning
a new one.

---

### `r` — Remove repo from saved list

Shows your saved list as a numbered menu. Select a number to remove that repo
from the list.

**Important:** This only removes it from MGitPi's list. It does **not** delete
any files from your Pi.

---

### `v` — Validate saved repo list

Checks every saved repository and reports its status:

| Result | Meaning |
|--------|---------|
| `[ OK ]` | Repository exists and has a `.git` folder |
| `[ERR]` | Directory is missing (deleted, moved, or unmounted) |

Use this when you notice something is wrong, or after moving repos around.

---

### `x` — Exit

Closes MGitPi and returns you to the terminal.

---

## 4. Repo Menu

Once you open a repository (via `o` or `p`), you enter the Repo Menu.
The repository's path is shown at the top so you always know which repo
you are working in.

```
┌─────────────────────────────────[ Repo Menu ]───────────────────────────────┐
│   1)  Status                                                           (s)  │
│   2)  Stage changes                                                    (a)  │
│   3)  Commit                                                           (c)  │
│   4)  Pull                                                             (l)  │
│   5)  Push                                                             (p)  │
│   6)  Rebase tools                                                     (r)  │
│   7)  Branch tools                                                     (b)  │
│   8)  Stash tools                                                      (t)  │
│   9)  Log                                                              (g)  │
│  10)  Undo / Cleanup                                                   (u)  │
│  11)  Back                                                             (b)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### `s` — Status

Shows the current state of your working directory.

**What it tells you:**
- Which files have been modified since the last commit
- Which files are staged (ready to be committed)
- Which files are new and untracked (Git hasn't seen them before)
- Which branch you are on
- Whether you are ahead or behind the remote

**Example output:**

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   config.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        notes.txt
```

**How to read it:**
- **"Changes to be committed"** — these files are staged. They will be included in your next commit.
- **"Changes not staged"** — you modified these files but haven't staged them yet.
- **"Untracked files"** — new files Git has never tracked. Use Stage to include them.

**Run this first** before staging or committing — it gives you a clear picture
of where things stand.

---

### `a` — Stage changes

Staging is the step between editing files and committing them. You choose
exactly which changes to include in the next commit.

**How it works in MGitPi:**

1. A numbered list of all changed files is shown:
   ```
   Changed files:

     1)  M  README.md
     2) ??  new-script.py
     3)  M  config.py

   Stage files (numbers, space-separated) or 'all':
   ```

2. Type numbers separated by spaces to stage specific files, or type `all` to
   stage everything:
   ```
   Stage >> 1 3        ← stages README.md and config.py
   Stage >> all        ← stages everything
   ```

**Understanding the status codes:**

| Code | Meaning |
|------|---------|
| `M ` | Modified and staged |
| ` M` | Modified, not yet staged |
| `??` | New untracked file |
| `D ` | Deleted (staged) |
| ` D` | Deleted (not staged) |
| `A ` | New file added to staging |

**Why stage instead of just committing everything?**

Staging lets you create focused, logical commits. For example, if you fixed a
bug and added a new feature at the same time, you can stage and commit the bug
fix first, then stage and commit the feature separately. This keeps your project
history clean and easy to understand.

---

### `c` — Commit

Saves your staged changes as a permanent snapshot in the repository's history.

You will be asked for a **commit message** — a short description of what
you changed and why.

**Good commit message examples:**

```
Fix login timeout not resetting on activity
Add temperature sensor reading to main loop
Update README with installation instructions
```

**What makes a good message:**
- Use the imperative mood ("Fix", "Add", "Update" — not "Fixed", "Added")
- Keep it under 72 characters
- Describe the *what* and *why*, not the *how*

**What committing does:**
Creates a permanent record in the repository history with your name, the date,
and the exact changes made. Commits are the building blocks of Git history.

**Note:** You must stage at least one file before committing. If nothing is
staged, commit will fail with a clear message.

---

### `l` — Pull

Downloads the latest changes from the remote repository (GitHub) and merges
them into your current branch.

**When to use it:**
- At the start of a work session to make sure you have the latest code
- Before pushing, to avoid conflicts

**What can happen:**
- `Already up to date.` — you already have the latest version
- A list of updated files — new changes were merged in
- A merge conflict message — your changes and the remote changes overlap
  (see [Troubleshooting](#12-troubleshooting))

**Requires:** A remote configured (set up when cloning). Uses your SSH key.

---

### `p` — Push

Uploads your local commits to the remote repository (GitHub), making them
visible to others.

**When to use it:** After committing, to share your work or back it up.

**What can happen:**
- Success output — commits uploaded
- `Everything up-to-date` — nothing new to push
- `rejected` error — someone else pushed first; run Pull first, then push again
- Permission error — your SSH key may not be added to the repo

**Rule of thumb:** Always Pull before you Push to avoid rejections.

---

## 5. Branch Tools

From the Repo Menu, press `b` to open Branch Tools.

```
┌──────────────────────────────[ Branch Tools ]───────────────────────────────┐
│   1)  List branches                                                    (l)  │
│   2)  Switch branch                                                    (s)  │
│   3)  Create branch                                                    (c)  │
│   4)  Delete branch                                                    (d)  │
│   5)  Back                                                             (b)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### What is a branch?

A branch is an independent line of development. Think of it like a parallel
version of your project where you can make changes without affecting the main
version.

The default branch is usually called `main` (or `master` on older repos).

**Example:** You have a working robot controller on `main`. You want to try
a new motor algorithm without risking the working version. You create a branch
called `motor-experiment`, make your changes there, test them, and only merge
them into `main` once they work.

---

### `l` — List branches

Shows all branches in the repository.

```
Branches:

  * main
    feature-sensors
    remotes/origin/main
    remotes/origin/feature-sensors
```

The `*` marks your current branch. Lines starting with `remotes/` are branches
on the remote server.

---

### `s` — Switch branch

Changes your working directory to a different branch. Your files update to
reflect that branch's state.

Enter the branch name exactly as it appears in the list.

**Note:** If you have uncommitted changes, Git may refuse to switch. Either
commit or stash your changes first.

---

### `c` — Create branch

Creates a new branch and switches to it immediately.

Enter a name for your new branch. Use lowercase with hyphens for clarity:

```
New branch name: fix-login-bug
New branch name: feature-sensor-readings
New branch name: experiment-new-ui
```

The new branch starts as an exact copy of your current branch.

---

### `d` — Delete branch

Shows a numbered list of local branches. Select one to delete it.

You will be asked to confirm before the deletion happens.

**Important:**
- You cannot delete the branch you are currently on. Switch to another branch first.
- This only deletes the local branch. The remote branch (on GitHub) is not affected.
- Deleted branches can be recovered if you know the commit hash, but it is tricky.
  Be sure before confirming.

---

## 6. Stash Tools

From the Repo Menu, press `t` to open Stash Tools.

```
┌───────────────────────────────[ Stash Tools ]───────────────────────────────┐
│   1)  Stash save                                                       (s)  │
│   2)  Stash list                                                       (l)  │
│   3)  Stash pop                                                        (p)  │
│   4)  Stash apply                                                      (a)  │
│   5)  Stash drop                                                       (d)  │
│   6)  Back                                                             (b)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### What is the stash?

The stash is a temporary storage area for work you are not ready to commit.
Think of it as a drawer where you can put your current changes aside to deal
with something else, and then pull them back out later.

**Common scenario:** You are halfway through a feature when you get asked to
fix an urgent bug. You stash your in-progress work, fix the bug on the main
branch, then return to your feature and pop the stash to continue where you
left off.

---

### `s` — Stash save

Saves all your current uncommitted changes to the stash and cleans your working
directory. You can optionally give it a message to remember what it contains:

```
Stash message (optional): half-done sensor calibration
```

---

### `l` — Stash list

Shows all saved stashes:

```
Stash list:

  stash@{0}: On main: half-done sensor calibration
  stash@{1}: On feature-x: quick experiment
```

Each stash has an index number in `{curly braces}`. The most recent is always
`stash@{0}`.

---

### `p` — Stash pop

Applies the most recent stash (`stash@{0}`) to your working directory and
removes it from the stash list. This is the most common way to restore your
work after stashing.

---

### `a` — Stash apply

Applies a stash by index but **keeps it in the list**. Useful if you want to
apply the same set of changes to multiple branches.

You will be asked for the index number (the number in `stash@{N}`). Default is `0`.

---

### `d` — Stash drop

Deletes a stash entry permanently without applying it.

You will be asked for the index. Confirm with `y`.

**Warning:** A dropped stash cannot be recovered. Only drop stashes you no
longer need.

---

## 7. Log Viewer

From the Repo Menu, press `g` to open the Log Viewer.

Shows the last 20 commits in a compact, visual format:

```
Commit log (last 20):

* a3f9d12 (HEAD -> main, origin/main) Add temperature sensor module
* 8c21b04 Fix divide-by-zero in calibration routine
* 5e7a3d8 Update README with wiring diagram
*   2b9c1f0 Merge branch 'feature-sensors'
|\
| * 7f4e2a1 Add DS18B20 sensor reading
| * 3c8d0b9 Add sensor module skeleton
|/
* 1a2e5f7 Initial commit
```

**Reading the log:**

| Part | Meaning |
|------|---------|
| `*` | A commit |
| `a3f9d12` | The short commit hash (unique ID) |
| `(HEAD -> main)` | Where you currently are |
| `(origin/main)` | Where the remote is |
| `|\` / `|/` | Branches merging |

The log is read **newest at top, oldest at bottom**.

---

## 8. Undo and Cleanup

From the Repo Menu, press `u` to open Undo / Cleanup.

```
┌──────────────────────────────[ Undo / Cleanup ]─────────────────────────────┐
│   1)  Undo last commit (keep staged)                                   (s)  │
│   2)  Undo last commit (unstage changes)                               (m)  │
│   3)  Unstage all                                                      (u)  │
│   4)  Discard ALL changes                                              (x)  │
│   5)  Back                                                             (b)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

All options require confirmation before doing anything.

---

### `s` — Undo last commit (keep staged) — Soft Reset

Undoes the most recent commit, but keeps all the changes staged and ready
to re-commit with a different message or after adding more changes.

**Nothing is lost.** Your files are unchanged. The commit is simply removed
from history and the changes returned to the staging area.

**When to use it:** You committed too soon, or with a typo in the message.

---

### `m` — Undo last commit (unstage changes) — Mixed Reset

Undoes the most recent commit and unstages all the changes. Your files on
disk are unchanged, but nothing is staged.

**Nothing is lost.** All your edited files are still modified on disk.
You can re-stage selectively and commit again more carefully.

**When to use it:** You committed the wrong files together and want to
re-organise into separate commits.

---

### `u` — Unstage all

Moves all staged files back to "modified but unstaged". Your files on disk
are not changed.

**When to use it:** You accidentally staged the wrong file and want to start
the staging step over.

---

### `x` — Discard ALL changes

**This is permanent.** It throws away every unstaged change in the working
directory and restores all files to the state of the last commit.

Because this cannot be undone, MGitPi asks you to type the word `discard`
in full to confirm. Typing `y` or `yes` is not enough.

**When to use it:** Your working directory is a mess and you want to start
fresh from the last commit. Only use this when you are certain you don't
need those changes.

---

### Quick comparison

| Option | Removes commit? | Changes staged? | Files changed on disk? | Reversible? |
|--------|----------------|-----------------|------------------------|-------------|
| Soft reset | Yes | Still staged | No | Yes (re-commit) |
| Mixed reset | Yes | Unstaged | No | Yes (re-stage) |
| Unstage all | No | Cleared | No | Yes (re-stage) |
| Discard all | No | No change | **Yes — permanent** | **No** |

---

## 9. Git Concepts Explained

This section explains the core ideas behind Git in plain language.

---

### Repository

A repository (repo) is a folder that Git is tracking. It contains your project
files plus a hidden `.git` folder where Git stores the entire history of changes.

---

### Working Tree

The working tree is simply the files you see in your project folder — the ones
you edit. When you modify a file, the change lives in the working tree until
you stage it.

---

### Staging Area (Index)

The staging area is a preparation zone between your working tree and a commit.
You explicitly move changes into the staging area using `a` (Stage changes)
before they are included in a commit.

```
[Working Tree] ──stage──► [Staging Area] ──commit──► [Commit History]
```

This two-step process lets you be intentional about what goes into each commit.

---

### Commit

A commit is a permanent snapshot of your staging area. Every commit has:
- A unique hash (like `a3f9d12`) — its permanent ID
- Your name and email
- A timestamp
- A message describing the change
- A reference to the previous commit (making a chain of history)

Commits are never deleted by normal operations — they form an immutable record
of your project's evolution.

---

### Branch

A branch is a named pointer to a specific commit. When you make new commits,
the branch pointer moves forward to point to the new commit.

Branches let multiple lines of development happen in parallel without affecting
each other.

```
main:     A → B → C → D
                   \
feature:            E → F
```

---

### Remote

A remote is a copy of the repository on another server (usually GitHub). The
default remote is called `origin`.

- **Push** sends your commits to the remote
- **Pull** brings commits from the remote to you
- **Clone** creates your local copy from the remote

---

### Push

Uploads your local commits to the remote repository. After pushing, others can
see your commits on GitHub.

---

### Pull

Downloads commits from the remote and merges them into your local branch. Pull
= Fetch + Merge in one step.

---

### Clone

Creates a complete local copy of a remote repository, including the full
history and all branches.

---

### Stash

A temporary storage area for uncommitted changes. Stashing saves your current
modifications and gives you a clean working tree without creating a commit.

---

### Merge

Combines the history of two branches. When you finish work on a feature branch,
you merge it into `main` so the changes become part of the main codebase.

---

### Rebase

An alternative to merging that rewrites your commits as if they were made on
top of another branch. Produces a cleaner, linear history.

*Rebase tools are not yet fully implemented in MGitPi.*

---

## 10. Common Workflows

### Daily workflow

The typical sequence when working on a project:

```
1. Pull              ← get the latest changes from GitHub first
2. Edit your files
3. Status            ← see what changed
4. Stage changes     ← select files to commit
5. Commit            ← save the snapshot with a message
6. Push              ← upload to GitHub
```

In MGitPi:

```
Workspace → o (open repo) → l (pull) → s (status) → a (stage) → c (commit) → p (push)
```

---

### Starting a new feature

When you want to work on something new without touching the stable code:

```
1. Make sure you are on main and it is up to date (pull)
2. Branch tools → c (Create branch): feature-my-feature
3. Edit your files
4. Stage → Commit (repeat as needed)
5. When done: switch back to main, merge the feature branch
```

---

### Saving work to resume later

When you need to stop in the middle of something:

```
1. Stash tools → s (Stash save) — give it a descriptive message
2. Later: Stash tools → p (Stash pop) to restore your work
```

---

### Fixing a mistake in the last commit

If you just committed but made an error:

```
Undo → s (Soft reset)     ← commit removed, changes still staged
Fix the file(s)
Stage changes → a
Commit → c                ← new commit with corrected message
```

---

### Recovering from a messy working tree

If your files are in a broken state and you want to go back to the last commit:

```
Undo → x (Discard all)    ← TYPE 'discard' to confirm
```

This wipes all unstaged changes and restores everything to the last committed state.

---

## 11. SSH Setup Guide

SSH is the secure way MGitPi talks to GitHub. Instead of typing a password
every time, your Pi uses a cryptographic key pair to prove its identity.

### How SSH keys work

SSH generates two files:
- **Private key** (`id_ed25519`) — stays on your Pi. Never share this.
- **Public key** (`id_ed25519.pub`) — uploaded to GitHub. GitHub uses it to
  verify that your Pi is who it claims to be.

### Automatic setup via MGitPi

Run `bash setup.sh`. If you don't have a key yet, the script will:
1. Generate a new ED25519 key pair in `~/.ssh/`
2. Display your public key
3. Ask you to add it to GitHub before continuing

### Manual key generation

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter to accept the default location (`~/.ssh/id_ed25519`).
Enter a passphrase (optional but recommended for security).

### Adding your public key to GitHub

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the output. Then:
1. Go to GitHub → click your profile picture → **Settings**
2. Click **SSH and GPG keys** → **New SSH key**
3. Give it a title (e.g., "Raspberry Pi 4")
4. Paste the public key
5. Click **Add SSH key**

### Testing the connection

```bash
ssh -T git@github.com
```

Expected response:

```
Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see `Permission denied`, double-check that the public key is added to
GitHub and that the correct private key is in `~/.ssh/`.

---

## 12. Troubleshooting

### Push rejected

```
error: failed to push some refs to 'git@github.com:...'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Cause:** Someone else (or you on another machine) pushed commits since your
last pull.

**Fix:** Pull first, then push:

```
Repo Menu → l (Pull) → then p (Push)
```

---

### Permission denied (publickey)

```
git@github.com: Permission denied (publickey).
```

**Cause:** Your SSH key is not added to GitHub, or the wrong key is being used.

**Fix:**
1. Check your public key is on GitHub (Settings → SSH keys).
2. Make sure the key is loaded: `ssh-add ~/.ssh/id_ed25519`
3. Test: `ssh -T git@github.com`

---

### Repo shows as `[ERR]` in validate

**Cause:** The repo has been moved, deleted, or is on an unmounted drive.

**Fix:** If you moved the repo, remove the old entry (`r`) and add the new
path (`a`). If on a USB drive, make sure it is mounted.

---

### Nothing to commit

```
nothing to commit, working tree clean
```

This is not an error — it means no files have been changed since the last
commit. You only commit when there are changes staged.

---

### Merge conflict after pull

```
CONFLICT (content): Merge conflict in main.py
Automatic merge failed; fix conflicts then commit the result.
```

**Cause:** Your changes and the remote changes modified the same part of the
same file.

**Fix:**
1. Open the conflicted file — look for lines like:
   ```
   <<<<<<< HEAD
   your version of the code
   =======
   remote version of the code
   >>>>>>> origin/main
   ```
2. Edit the file to keep the correct version and remove the `<<<<`, `====`,
   `>>>>` markers.
3. Stage the resolved file.
4. Commit.

*MGitPi does not yet have a built-in conflict resolver. Edit files directly
in a text editor for now.*

---

### App crashes or shows a Python traceback

Please report this at the project's issue tracker with:
- The full error message
- What you were doing when it happened
- Your Python version (`python3 --version`) and Pi model

---

*MGitPi — built for the Pi, not for the cloud.*
