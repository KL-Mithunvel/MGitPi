# main.py (MGitPi) - menu setup using your klm_menu.py engine
# NOTE: This is only menu setup + routing skeleton (no git logic yet)

import klm_menu
import art
# -------------------------
# Command handlers (stubs)
# -------------------------

def open_repo():
    print("open_repo (TODO)")

def open_repo_by_path():
    print("open_repo_by_path (TODO)")

def clone_repo_ssh():
    print("clone_repo_ssh (TODO)")

def add_repo():
    print("add_repo (TODO)")

def remove_repo():
    print("remove_repo (TODO)")

def validate_repo_list():
    print("validate_repo_list (TODO)")

def repo_status():
    print("repo_status (TODO)")

def stage_changes():
    print("stage_changes (TODO)")

def commit_changes():
    print("commit_changes (TODO)")

def pull_repo():
    print("pull_repo (TODO)")

def push_repo():
    print("push_repo (TODO)")

def rebase_tools():
    print("rebase_tools (TODO)")

def branch_tools():
    print("branch_tools (TODO)")

def stash_tools():
    print("stash_tools (TODO)")

def log_view():
    print("log_view (TODO)")

def undo_tools():
    print("undo_tools (TODO)")


# -------------------------
# Menus
# -------------------------

workspace_menu = {
    "menu": "Workspace Menu",
    "name": "workspace",
    "width": 90,   # optional, used by klm_menu.display_menu
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
# Router loop (same style as your furnace main.py)
# -------------------------

def show_menu(m):
    ex = False
    menu_name = "workspace"

    while not ex:
        cmd, menu_name = klm_menu.present_menu(menu_name, m)
        ex = (cmd == "exit")

        if cmd == "open_repo":
            open_repo()

        elif cmd == "open_repo_by_path":
            open_repo_by_path()

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

        elif cmd == "rebase_tools":
            rebase_tools()

        elif cmd == "branch_tools":
            branch_tools()

        elif cmd == "stash_tools":
            stash_tools()

        elif cmd == "log_view":
            log_view()

        elif cmd == "undo_tools":
            undo_tools()


if __name__ == "__main__":
    art.splash(wait_sec=5)  # <-- separate function call as you wanted
    show_menu(menu_system)