import pathlib
import klm_menu
import art
import repo_manager
import git_ops

_current_repo = None


# -------------------------
# Helpers
# -------------------------

def _pause(msg=""):
    if msg:
        print(f"\n{msg}")
    input("\nPress Enter to continue...")


def _pick_repo(repos, prompt="Select a repository"):
    art.clear()
    print(f"\n{prompt}:\n")
    for i, r in enumerate(repos, 1):
        print(f"  {i:>2})  {r}")
    print(f"\n       b)  Back\n")
    while True:
        choice = input("Select >> ").strip().lower()
        if choice == "b":
            return None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(repos):
                return repos[idx]
        print("  Invalid selection.")


def _parse_filename(status_line):
    """Extract filename from a 'git status --short' line (format: XY FILENAME)."""
    rest = status_line[3:].strip()
    if " -> " in rest:
        return rest.split(" -> ", 1)[1].strip()
    return rest


# -------------------------
# Command handlers
# -------------------------

def open_repo():
    global _current_repo
    repos = repo_manager.load_repos()
    if not repos:
        _pause("No repos saved. Use 'a' to add one.")
        return None
    path = _pick_repo(repos)
    if path is None:
        return None
    _current_repo = path
    repo_manager._log_event("opened", path)
    return "repo"


def open_repo_by_path():
    global _current_repo
    art.clear()
    path_str = input("Enter repo path: ").strip()
    p = pathlib.Path(path_str).resolve()
    if not p.exists():
        _pause(f"Path does not exist: {p}")
        return None
    if not (p / ".git").exists():
        _pause(f"Not a git repository (no .git): {p}")
        return None
    _current_repo = str(p)
    repo_manager._log_event("opened", str(p))
    return "repo"


def clone_repo_ssh():
    art.clear()
    url = input("Enter SSH URL: ").strip()
    dest_str = input("Enter destination directory: ").strip()
    dest = pathlib.Path(dest_str).resolve()
    if not dest.exists():
        _pause(f"Destination directory does not exist: {dest}")
        return
    ok, err = git_ops.git_clone(url, dest)
    if ok:
        _pause("Clone successful.")
    else:
        _pause(f"Clone failed: {err}")


def add_repo():
    art.clear()
    path_str = input("Enter repo path to add: ").strip()
    ok, err = repo_manager.add_repo(path_str)
    if ok:
        _pause(f"Added: {pathlib.Path(path_str).resolve()}")
    else:
        _pause(f"Error: {err}")


def remove_repo():
    repos = repo_manager.load_repos()
    if not repos:
        _pause("No repos saved.")
        return
    path = _pick_repo(repos, "Select repo to remove")
    if path is None:
        return
    ok, err = repo_manager.remove_repo(path)
    if ok:
        _pause(f"Removed: {path}")
    else:
        _pause(f"Error: {err}")


def validate_repo_list():
    results = repo_manager.validate_repos()
    art.clear()
    print()
    if not results:
        print("  No repos in list.")
    for rpath, status in results:
        tag = art.green("[ OK ]") if status == "ok" else art.red("[ERR]")
        print(f"  {tag}  {rpath}  ({status})")
    input("\nPress Enter to continue...")


def repo_status():
    art.clear()
    out, err = git_ops.git_status_long(_current_repo)
    if err:
        print(f"\nError: {err}")
    else:
        print(out)
    _pause()


def stage_changes():
    lines, err = git_ops.git_status(_current_repo)
    if err:
        _pause(f"Error: {err}")
        return
    if not lines:
        _pause("Nothing to stage (working tree clean).")
        return
    art.clear()
    print("\nChanged files:\n")
    for i, line in enumerate(lines, 1):
        print(f"  {i:>2})  {line}")
    print()
    choice = input("Stage files (numbers, space-separated) or 'all': ").strip().lower()
    if choice == "all":
        ok, err2 = git_ops.git_add_files(_current_repo, ["."])
        if ok:
            _pause("All changes staged.")
        else:
            _pause(f"Error: {err2}")
    else:
        parts = choice.split()
        filenames = []
        for part in parts:
            if part.isdigit():
                idx = int(part) - 1
                if 0 <= idx < len(lines):
                    filenames.append(_parse_filename(lines[idx]))
        if not filenames:
            _pause("No valid files selected.")
            return
        ok, err2 = git_ops.git_add_files(_current_repo, filenames)
        if ok:
            _pause(f"Staged: {', '.join(filenames)}")
        else:
            _pause(f"Error: {err2}")


def commit_changes():
    art.clear()
    message = input("Commit message: ").strip()
    if not message:
        _pause("Commit aborted (empty message).")
        return
    ok, result = git_ops.git_commit(_current_repo, message)
    if ok:
        _pause(f"Committed: {result}")
    else:
        _pause(f"Commit failed: {result}")


def pull_repo():
    print("\nPulling from remote...")
    ok, result = git_ops.git_pull(_current_repo)
    if ok:
        _pause(result)
    else:
        _pause(f"Pull failed: {result}")


def push_repo():
    print("\nPushing to remote...")
    ok, result = git_ops.git_push(_current_repo)
    if ok:
        _pause(result)
    else:
        _pause(f"Push failed: {result}")


def branch_list():
    lines, err = git_ops.git_branch_list(_current_repo)
    art.clear()
    if err:
        _pause(f"Error: {err}")
        return
    print("\nBranches:\n")
    for line in lines:
        print(f"  {line}")
    input("\nPress Enter to continue...")


def branch_switch():
    art.clear()
    name = input("Branch name to switch to: ").strip()
    if not name: return
    ok, out = git_ops.git_branch_switch(_current_repo, name)
    _pause(out)


def branch_create():
    art.clear()
    name = input("New branch name: ").strip()
    if not name: return
    ok, out = git_ops.git_branch_create(_current_repo, name)
    _pause(out if ok else f"Failed: {out}")


def branch_delete():
    lines, err = git_ops.git_branch_list(_current_repo)
    if err:
        _pause(f"Error: {err}")
        return
    local = [l.strip().lstrip("* ") for l in lines if not l.strip().startswith("remotes/")]
    if not local:
        _pause("No local branches found.")
        return
    art.clear()
    print("\nLocal branches:\n")
    for i, b in enumerate(local, 1):
        print(f"  {i:>2})  {b}")
    print("\n       b)  Back\n")
    while True:
        choice = input("Select branch to delete >> ").strip().lower()
        if choice == "b": return
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(local):
                name = local[idx]
                confirm = input(f"  Delete '{name}'? (y/N): ").strip().lower()
                if confirm == "y":
                    ok, out = git_ops.git_branch_delete(_current_repo, name)
                    _pause(out if ok else f"Failed: {out}")
                else:
                    _pause("Cancelled.")
                return
        print("  Invalid selection.")


def stash_save():
    art.clear()
    msg = input("Stash message (optional): ").strip()
    ok, out = git_ops.git_stash_save(_current_repo, msg)
    _pause(out if ok else f"Failed: {out}")


def stash_list():
    entries, err = git_ops.git_stash_list(_current_repo)
    art.clear()
    if err:
        _pause(f"Error: {err}")
        return
    if not entries:
        _pause("No stashes saved.")
        return
    print("\nStash list:\n")
    for e in entries:
        print(f"  {e}")
    input("\nPress Enter to continue...")


def stash_pop():
    ok, out = git_ops.git_stash_pop(_current_repo)
    _pause(out)


def stash_apply():
    entries, err = git_ops.git_stash_list(_current_repo)
    if not entries:
        _pause("No stashes saved.")
        return
    art.clear()
    print("\nStash list:\n")
    for i, e in enumerate(entries):
        print(f"  {i})  {e}")
    idx_str = input("\nApply stash index (default 0): ").strip()
    idx = int(idx_str) if idx_str.isdigit() else 0
    ok, out = git_ops.git_stash_apply(_current_repo, idx)
    _pause(out)


def stash_drop():
    entries, err = git_ops.git_stash_list(_current_repo)
    if not entries:
        _pause("No stashes saved.")
        return
    art.clear()
    print("\nStash list:\n")
    for i, e in enumerate(entries):
        print(f"  {i})  {e}")
    idx_str = input("\nDrop stash index (default 0): ").strip()
    idx = int(idx_str) if idx_str.isdigit() else 0
    confirm = input(f"  Drop stash@{{{idx}}}? (y/N): ").strip().lower()
    if confirm == "y":
        ok, out = git_ops.git_stash_drop(_current_repo, idx)
        _pause(out if ok else f"Failed: {out}")
    else:
        _pause("Cancelled.")


def log_view():
    out, err = git_ops.git_log(_current_repo)
    art.clear()
    if err:
        _pause(f"Error: {err}")
        return
    print("\nCommit log (last 20):\n")
    print(out)
    input("\nPress Enter to continue...")


def undo_soft():
    confirm = input("Undo last commit (keep staged)? (y/N): ").strip().lower()
    if confirm == "y":
        ok, out = git_ops.git_reset_soft(_current_repo)
        _pause(out if ok else f"Failed: {out}")
    else:
        _pause("Cancelled.")


def undo_mixed():
    confirm = input("Undo last commit (unstage changes)? (y/N): ").strip().lower()
    if confirm == "y":
        ok, out = git_ops.git_reset_mixed(_current_repo)
        _pause(out if ok else f"Failed: {out}")
    else:
        _pause("Cancelled.")


def unstage_all():
    confirm = input("Unstage all staged files? (y/N): ").strip().lower()
    if confirm == "y":
        ok, out = git_ops.git_unstage_all(_current_repo)
        _pause("Done." if ok else f"Failed: {out}")
    else:
        _pause("Cancelled.")


def discard_all():
    art.clear()
    print(art.red("\n  WARNING: This will permanently discard ALL unstaged changes."))
    print("  This cannot be undone.\n")
    confirm1 = input("  Type 'discard' to confirm: ").strip().lower()
    if confirm1 == "discard":
        ok, out = git_ops.git_discard_all(_current_repo)
        _pause("Done." if ok else f"Failed: {out}")
    else:
        _pause("Cancelled.")


# -------------------------
# Menus
# -------------------------

workspace_menu = {
    "menu": "Workspace Menu",
    "name": "workspace",
    "width": 90,
    "options": [
        ["open_repo", "Open repo (from saved list)", "o", "Open a saved Git repository from your persistent list. Use (a) to add repos."],
        ["open_repo_by_path", "Open repo by path (one-time)", "p", "Enter any path to a local Git repo. Useful for one-off access without saving."],
        ["clone_repo_ssh", "Clone new repo (SSH)", "c", "Clone a remote repository using an SSH URL (git@github.com:user/repo.git)."],
        ["add_repo", "Add repo to saved list", "a", "Add a local Git repository path to your saved list."],
        ["remove_repo", "Remove repo from saved list", "r", "Remove a repository from your saved list. Does not delete files on disk."],
        ["validate_repo_list", "Validate saved repo list", "v", "Check every saved repo: flags missing directories and missing .git folders."],
        ["exit", "Exit", "x", "Exit MGitPi and return to the shell."],
    ],
    "back_option": False,
    "back_to": None
}

repo_menu = {
    "menu": "Repo Menu",
    "name": "repo",
    "width": 90,
    "options": [
        ["repo_status", "Status", "s", "Show the current working tree status: staged, unstaged, and untracked files."],
        ["stage_changes", "Stage changes", "a", "Interactively stage files for commit. Type numbers or 'all' to select."],
        ["commit_changes", "Commit", "c", "Commit staged changes with a message."],
        ["pull_repo", "Pull", "l", "Fetch and merge changes from the remote branch (git pull)."],
        ["push_repo", "Push", "p", "Upload local commits to the remote repository (git push)."],
        ["menu:rebase", "Rebase tools", "r", "Rebase tools: replay commits on top of another branch."],
        ["menu:branch", "Branch tools", "b", "Branch tools: list, create, switch, and delete branches."],
        ["menu:stash", "Stash tools", "t", "Stash tools: save and restore uncommitted work temporarily."],
        ["log_view", "Log", "g", "View the recent commit history (last 20 commits)."],
        ["menu:undo", "Undo / Cleanup", "u", "Undo and cleanup: reverse commits or discard changes."],
    ],
    "back_option": True,
    "back_to": "workspace"
}

rebase_menu = {
    "menu": "Rebase Tools",
    "name": "rebase",
    "width": 90,
    "options": [
        ["rebase_onto_main", "Rebase onto origin/main", "m", "Replay your current branch's commits on top of origin/main."],
        ["rebase_continue", "Rebase continue", "c", "Continue an in-progress rebase after resolving conflicts."],
        ["rebase_abort", "Rebase abort", "a", "Abort the current rebase and restore the original branch state."],
    ],
    "back_option": True,
    "back_to": "repo"
}

branch_menu = {
    "menu": "Branch Tools",
    "name": "branch",
    "width": 90,
    "options": [
        ["branch_list", "List branches", "l", "List all local and remote branches. Your current branch is marked with *."],
        ["branch_switch", "Switch branch", "s", "Switch to an existing branch (git checkout)."],
        ["branch_create", "Create branch", "c", "Create a new branch and switch to it immediately (git checkout -b)."],
        ["branch_delete", "Delete branch", "d", "Delete a local branch. Prompts for confirmation."],
    ],
    "back_option": True,
    "back_to": "repo"
}

stash_menu = {
    "menu": "Stash Tools",
    "name": "stash",
    "width": 90,
    "options": [
        ["stash_save", "Stash save", "s", "Save your current uncommitted changes to the stash stack."],
        ["stash_list", "Stash list", "l", "Show all stashed changesets with their index numbers."],
        ["stash_apply", "Stash apply", "a", "Apply a stash by index without removing it from the stack."],
        ["stash_pop", "Stash pop", "p", "Apply the most recent stash and remove it from the stack."],
        ["stash_drop", "Stash drop", "d", "Delete a stash entry by index."],
    ],
    "back_option": True,
    "back_to": "repo"
}

undo_menu = {
    "menu": "Undo / Cleanup",
    "name": "undo",
    "width": 90,
    "options": [
        ["undo_soft", "Undo last commit (soft)", "s", "Undo the last commit but keep changes staged. Safe — nothing is lost."],
        ["undo_mixed", "Undo last commit (mixed)", "m", "Undo the last commit and unstage the changes. Files stay modified on disk."],
        ["unstage_all", "Unstage all", "u", "Unstage all staged files (moves them back to 'modified' without losing changes)."],
        ["discard_all", "Discard ALL changes", "x", "DANGER: discard ALL unstaged changes permanently. Cannot be undone."],
    ],
    "back_option": True,
    "back_to": "repo"
}

menu_system = {
    "workspace": workspace_menu,
    "repo": repo_menu,
    "rebase": rebase_menu,
    "branch": branch_menu,
    "stash": stash_menu,
    "undo": undo_menu,
}


# -------------------------
# Router loop
# -------------------------

def show_menu(m):
    ex = False
    menu_name = "workspace"
    while not ex:
        cmd, menu_name = klm_menu.present_menu(menu_name, m)
        if cmd == "exit":
            ex = True
        elif cmd == "open_repo":
            next_menu = open_repo()
            if next_menu:
                menu_name = next_menu
        elif cmd == "open_repo_by_path":
            next_menu = open_repo_by_path()
            if next_menu:
                menu_name = next_menu
        elif cmd == "clone_repo_ssh":
            clone_repo_ssh()
        elif cmd == "add_repo":
            add_repo()
        elif cmd == "remove_repo":
            remove_repo()
        elif cmd == "validate_repo_list":
            validate_repo_list()
        elif cmd == "repo_status":
            repo_status()
        elif cmd == "stage_changes":
            stage_changes()
        elif cmd == "commit_changes":
            commit_changes()
        elif cmd == "pull_repo":
            pull_repo()
        elif cmd == "push_repo":
            push_repo()
        elif cmd == "branch_list":    branch_list()
        elif cmd == "branch_switch":  branch_switch()
        elif cmd == "branch_create":  branch_create()
        elif cmd == "branch_delete":  branch_delete()
        elif cmd == "stash_save":     stash_save()
        elif cmd == "stash_list":     stash_list()
        elif cmd == "stash_pop":      stash_pop()
        elif cmd == "stash_apply":    stash_apply()
        elif cmd == "stash_drop":     stash_drop()
        elif cmd == "log_view":       log_view()
        elif cmd == "undo_soft":      undo_soft()
        elif cmd == "undo_mixed":     undo_mixed()
        elif cmd == "unstage_all":    unstage_all()
        elif cmd == "discard_all":    discard_all()
        elif cmd in ("rebase_onto_main", "rebase_continue", "rebase_abort"):
            _pause(f"Rebase tools not yet implemented.")


if __name__ == "__main__":
    art.splash(wait_sec=5)
    repos = repo_manager.load_repos()
    if repos:
        snapshots = [git_ops.git_repo_summary(p) for p in repos]
        repo_manager.save_status_snapshot(snapshots)
    show_menu(menu_system)
