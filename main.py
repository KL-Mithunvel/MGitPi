import klm_menu
import art
import git_ops
import repo_manager
from pathlib import Path

current_repo = None  # active repo path, set when user opens/clones a repo


def _pause():
    input("\n  Press Enter to continue...")


# -------------------------
# Workspace handlers
# -------------------------

def open_repo():
    global current_repo
    repos = repo_manager.load_repos()
    if not repos:
        print("\n  No saved repos yet. Use 'Add repo' (a) first.")
        _pause()
        return None
    print("\n  Saved repositories:\n")
    for i, r in enumerate(repos, 1):
        print(f"    {i}) {r}")
    print(f"\n    0) Cancel")
    while True:
        try:
            choice = int(input("\n  Select number >> ").strip())
        except ValueError:
            continue
        if choice == 0:
            return None
        if 1 <= choice <= len(repos):
            current_repo = repos[choice - 1]
            print(f"\n  Opened: {current_repo}")
            return "repo"


def open_repo_by_path():
    global current_repo
    path = input("\n  Enter repo path >> ").strip()
    if not path:
        return None
    p = Path(path).expanduser().resolve()
    if not p.exists():
        print(f"\n  [ERR] Path not found: {p}")
        _pause()
        return None
    if not (p / ".git").exists():
        print(f"\n  [ERR] No .git folder at: {p}")
        _pause()
        return None
    current_repo = str(p)
    print(f"\n  Opened: {current_repo}")
    return "repo"


def clone_repo_ssh():
    global current_repo
    print()
    url = input("  Enter SSH or HTTPS URL >> ").strip()
    if not url:
        return None
    default_dest = str(Path.home())
    prompt = f"  Clone into (Enter for {default_dest}) >> "
    dest = input(prompt).strip() or default_dest
    print(f"\n  Cloning into {dest} ...")
    cloned_path, err = git_ops.git_clone(url, dest)
    if err:
        print(f"\n  [ERR] {err}")
        _pause()
        return None
    print(f"\n  [ OK ] Cloned to: {cloned_path}")
    add = input("\n  Add to saved list? (y/n) >> ").strip().lower()
    if add == "y":
        ok, msg = repo_manager.add_repo(cloned_path)
        print(f"  {'[ OK ]' if ok else '[ERR]'} {msg}")
    current_repo = cloned_path
    _pause()
    return "repo"


def add_repo():
    path = input("\n  Enter path to repo >> ").strip()
    if not path:
        return
    ok, msg = repo_manager.add_repo(path)
    print(f"\n  {'[ OK ]' if ok else '[ERR]'} {msg}")
    _pause()


def remove_repo():
    repos = repo_manager.load_repos()
    if not repos:
        print("\n  No saved repos.")
        _pause()
        return
    print("\n  Saved repositories:\n")
    for i, r in enumerate(repos, 1):
        print(f"    {i}) {r}")
    print(f"\n    0) Cancel")
    while True:
        try:
            choice = int(input("\n  Select number to remove >> ").strip())
        except ValueError:
            continue
        if choice == 0:
            return
        if 1 <= choice <= len(repos):
            ok, msg = repo_manager.remove_repo(choice - 1)
            print(f"\n  {'[ OK ] Removed:' if ok else '[ERR]'} {msg}")
            _pause()
            return


def validate_repo_list():
    results = repo_manager.validate_repos()
    if not results:
        print("\n  No saved repos to validate.")
    else:
        print()
        for path, status in results:
            tag = "[ OK ]" if status == "ok" else f"[ERR] ({status})"
            print(f"  {tag} {path}")
    _pause()


# -------------------------
# Repo action handlers
# -------------------------

def _check_repo():
    if not current_repo:
        print("\n  No repo open. Go back and open or clone a repo first.")
        _pause()
        return False
    return True


def repo_status():
    if not _check_repo():
        return
    print(f"\n  Repo: {current_repo}\n")
    out, err = git_ops.git_status(current_repo)
    print(err if err else out)
    _pause()


def stage_changes():
    if not _check_repo():
        return
    ok, err = git_ops.git_add_all(current_repo)
    print(f"\n  {'[ OK ] All changes staged.' if ok else '[ERR] ' + err}")
    _pause()


def commit_changes():
    if not _check_repo():
        return
    msg = input("\n  Commit message >> ").strip()
    if not msg:
        print("\n  Cancelled — empty message.")
        _pause()
        return
    ok, result = git_ops.git_commit(current_repo, msg)
    print(f"\n  {'[ OK ]' if ok else '[ERR]'} {result}")
    _pause()


def pull_repo():
    if not _check_repo():
        return
    print(f"\n  Pulling {current_repo} ...")
    ok, result = git_ops.git_pull(current_repo)
    print(f"\n  {'[ OK ]' if ok else '[ERR]'} {result}")
    _pause()


def push_repo():
    if not _check_repo():
        return
    print(f"\n  Pushing {current_repo} ...")
    ok, result = git_ops.git_push(current_repo)
    print(f"\n  {'[ OK ]' if ok else '[ERR]'} {result}")
    _pause()


def log_view():
    if not _check_repo():
        return
    out, err = git_ops.git_log(current_repo)
    print(f"\n  Repo: {current_repo}\n")
    print(err if err else out)
    _pause()


def branch_tools():
    if not _check_repo():
        return
    out, err = git_ops.git_list_branches(current_repo)
    print(f"\n  Branches in {current_repo}:\n")
    print(err if err else out)
    _pause()


def rebase_tools():
    print("\n  Rebase tools — coming soon.")
    _pause()


def stash_tools():
    print("\n  Stash tools — coming soon.")
    _pause()


def undo_tools():
    print("\n  Undo tools — coming soon.")
    _pause()


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
        ["clone_repo_ssh", "Clone new repo (SSH / HTTPS)", "c"],
        ["add_repo", "Add repo to saved list", "a"],
        ["remove_repo", "Remove repo from saved list", "r"],
        ["validate_repo_list", "Validate saved repo list", "v"],
        ["exit", "Exit", "x"],
    ],
    "back_option": False,
    "back_to": None,
}

repo_menu = {
    "menu": "Repo Menu",
    "name": "repo",
    "width": 90,
    "options": [
        ["repo_status", "Status", "s"],
        ["stage_changes", "Stage all changes", "a"],
        ["commit_changes", "Commit", "c"],
        ["pull_repo", "Pull", "l"],
        ["push_repo", "Push", "p"],
        ["menu:branch", "Branch tools", "b"],
        ["menu:rebase", "Rebase tools", "r"],
        ["menu:stash", "Stash tools", "t"],
        ["log_view", "Log", "g"],
        ["menu:undo", "Undo / Cleanup", "u"],
    ],
    "back_option": True,
    "back_to": "workspace",
}

rebase_menu = {
    "menu": "Rebase Tools",
    "name": "rebase",
    "width": 90,
    "options": [
        ["rebase_tools", "Rebase onto origin/main", "m"],
        ["rebase_tools", "Rebase continue", "c"],
        ["rebase_tools", "Rebase abort", "a"],
    ],
    "back_option": True,
    "back_to": "repo",
}

branch_menu = {
    "menu": "Branch Tools",
    "name": "branch",
    "width": 90,
    "options": [
        ["branch_tools", "List branches", "l"],
        ["branch_tools", "Switch branch (coming soon)", "s"],
        ["branch_tools", "Create branch (coming soon)", "c"],
        ["branch_tools", "Delete branch (coming soon)", "d"],
    ],
    "back_option": True,
    "back_to": "repo",
}

stash_menu = {
    "menu": "Stash Tools",
    "name": "stash",
    "width": 90,
    "options": [
        ["stash_tools", "Stash save", "s"],
        ["stash_tools", "Stash list", "l"],
        ["stash_tools", "Stash apply", "a"],
        ["stash_tools", "Stash pop", "p"],
        ["stash_tools", "Stash drop", "d"],
    ],
    "back_option": True,
    "back_to": "repo",
}

undo_menu = {
    "menu": "Undo / Cleanup",
    "name": "undo",
    "width": 90,
    "options": [
        ["undo_tools", "Undo last commit (soft)", "s"],
        ["undo_tools", "Undo last commit (mixed)", "m"],
        ["undo_tools", "Unstage all", "u"],
        ["undo_tools", "Discard ALL changes", "x"],
    ],
    "back_option": True,
    "back_to": "repo",
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
        ex = (cmd == "exit")
        nav = None

        if cmd == "open_repo":
            nav = open_repo()
        elif cmd == "open_repo_by_path":
            nav = open_repo_by_path()
        elif cmd == "clone_repo_ssh":
            nav = clone_repo_ssh()
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
        elif cmd == "branch_tools":
            branch_tools()
        elif cmd == "rebase_tools":
            rebase_tools()
        elif cmd == "stash_tools":
            stash_tools()
        elif cmd == "log_view":
            log_view()
        elif cmd == "undo_tools":
            undo_tools()

        if nav:
            menu_name = nav


if __name__ == "__main__":
    art.splash(wait_sec=5)
    show_menu(menu_system)
