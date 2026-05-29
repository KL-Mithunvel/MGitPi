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


def rebase_tools():
    _pause("'rebase_tools' is not yet implemented.")


def branch_tools():
    _pause("'branch_tools' is not yet implemented.")


def stash_tools():
    _pause("'stash_tools' is not yet implemented.")


def log_view():
    _pause("'log_view' is not yet implemented.")


def undo_tools():
    _pause("'undo_tools' is not yet implemented.")


# -------------------------
# Menus
# -------------------------

workspace_menu = {
    "menu": "Workspace Menu",
    "name": "workspace",
    "width": 90,
    "options": [
        ["open_repo", "Open repo (from saved list)", "o"],
        ["open_repo_by_path", "Open repo by path (one-time)", "p"],
        ["clone_repo_ssh", "Clone new repo (SSH)", "c"],
        ["add_repo", "Add repo to saved list", "a"],
        ["remove_repo", "Remove repo from saved list", "r"],
        ["validate_repo_list", "Validate saved repo list", "v"],
        ["exit", "Exit", "x"],
    ],
    "back_option": False,
    "back_to": None
}

repo_menu = {
    "menu": "Repo Menu",
    "name": "repo",
    "width": 90,
    "options": [
        ["repo_status", "Status", "s"],
        ["stage_changes", "Stage changes", "a"],
        ["commit_changes", "Commit", "c"],
        ["pull_repo", "Pull", "l"],
        ["push_repo", "Push", "p"],
        ["menu:rebase", "Rebase tools", "r"],
        ["menu:branch", "Branch tools", "b"],
        ["menu:stash", "Stash tools", "t"],
        ["log_view", "Log", "g"],
        ["menu:undo", "Undo / Cleanup", "u"],
    ],
    "back_option": True,
    "back_to": "workspace"
}

rebase_menu = {
    "menu": "Rebase Tools",
    "name": "rebase",
    "width": 90,
    "options": [
        ["rebase_tools", "Rebase onto origin/main (TODO)", "m"],
        ["rebase_tools", "Rebase continue (TODO)", "c"],
        ["rebase_tools", "Rebase abort (TODO)", "a"],
    ],
    "back_option": True,
    "back_to": "repo"
}

branch_menu = {
    "menu": "Branch Tools",
    "name": "branch",
    "width": 90,
    "options": [
        ["branch_tools", "List branches (TODO)", "l"],
        ["branch_tools", "Switch branch (TODO)", "s"],
        ["branch_tools", "Create branch (TODO)", "c"],
        ["branch_tools", "Delete branch (TODO)", "d"],
    ],
    "back_option": True,
    "back_to": "repo"
}

stash_menu = {
    "menu": "Stash Tools",
    "name": "stash",
    "width": 90,
    "options": [
        ["stash_tools", "Stash save (TODO)", "s"],
        ["stash_tools", "Stash list (TODO)", "l"],
        ["stash_tools", "Stash apply (TODO)", "a"],
        ["stash_tools", "Stash pop (TODO)", "p"],
        ["stash_tools", "Stash drop (TODO)", "d"],
    ],
    "back_option": True,
    "back_to": "repo"
}

undo_menu = {
    "menu": "Undo / Cleanup",
    "name": "undo",
    "width": 90,
    "options": [
        ["undo_tools", "Undo last commit (soft) (TODO)", "s"],
        ["undo_tools", "Undo last commit (mixed) (TODO)", "m"],
        ["undo_tools", "Unstage all (TODO)", "u"],
        ["undo_tools", "Discard ALL changes (TODO)", "x"],
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
        elif cmd in ("rebase_tools", "branch_tools", "stash_tools", "log_view", "undo_tools"):
            _pause(f"'{cmd}' is not yet implemented.")


if __name__ == "__main__":
    art.splash(wait_sec=5)
    repos = repo_manager.load_repos()
    if repos:
        snapshots = [git_ops.git_repo_summary(p) for p in repos]
        repo_manager.save_status_snapshot(snapshots)
    show_menu(menu_system)
