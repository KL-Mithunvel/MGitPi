import subprocess
import pathlib


def _run(args: list, path) -> tuple:
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=str(path),
    )
    return result.stdout, result.stderr, result.returncode


def git_status(path) -> tuple:
    out, err, rc = _run(["status", "--short"], path)
    if rc != 0:
        return (None, err.strip() or "git status failed")
    lines = [l for l in out.splitlines() if l.strip()]
    return (lines, None)


def git_status_long(path) -> tuple:
    out, err, rc = _run(["status"], path)
    if rc != 0:
        return (None, err.strip() or "git status failed")
    return (out, None)


def git_add_files(path, files: list) -> tuple:
    out, err, rc = _run(["add"] + files, path)
    if rc != 0:
        return (False, err.strip() or "git add failed")
    return (True, None)


def git_commit(path, message: str) -> tuple:
    out, err, rc = _run(["commit", "-m", message], path)
    if rc != 0:
        return (False, err.strip() or "git commit failed")
    summary = out.strip().splitlines()[0] if out.strip() else "committed"
    return (True, summary)


def git_push(path) -> tuple:
    out, err, rc = _run(["push"], path)
    if rc != 0:
        return (False, err.strip() or "git push failed")
    return (True, out or err)


def git_pull(path) -> tuple:
    out, err, rc = _run(["pull"], path)
    if rc != 0:
        return (False, err.strip() or "git pull failed")
    return (True, out or err)


def git_clone(url: str, dest_dir) -> tuple:
    result = subprocess.run(
        ["git", "clone", url],
        capture_output=True,
        text=True,
        cwd=str(dest_dir),
    )
    if result.returncode != 0:
        return (False, result.stderr.strip() or "git clone failed")
    return (True, None)


# ── Branch operations ─────────────────────────────────────────────────────────

def git_branch_list(path) -> tuple:
    """Return (list_of_branch_strings, error). Current branch prefixed with '*'."""
    out, err, rc = _run(["branch", "-a", "--no-color"], path)
    if rc != 0:
        return (None, err.strip() or "git branch failed")
    lines = [l for l in out.splitlines() if l.strip()]
    return (lines, None)


def git_branch_switch(path, name) -> tuple:
    """git checkout <name>. Return (bool, output_or_error)."""
    out, err, rc = _run(["checkout", name], path)
    if rc != 0:
        return (False, err.strip() or "git checkout failed")
    return (True, out.strip() or err.strip())


def git_branch_create(path, name) -> tuple:
    """git checkout -b <name>. Return (bool, output_or_error)."""
    out, err, rc = _run(["checkout", "-b", name], path)
    if rc != 0:
        return (False, err.strip() or "git checkout -b failed")
    return (True, out.strip() or err.strip())


def git_branch_delete(path, name, force=False) -> tuple:
    """git branch -d <name> (or -D if force=True). Return (bool, output_or_error)."""
    flag = "-D" if force else "-d"
    out, err, rc = _run(["branch", flag, name], path)
    if rc != 0:
        return (False, err.strip() or "git branch delete failed")
    return (True, out.strip() or err.strip())


# ── Stash operations ──────────────────────────────────────────────────────────

def git_stash_save(path, message="") -> tuple:
    """git stash push [-m message]. Return (bool, output_or_error)."""
    args = ["stash", "push"]
    if message:
        args += ["-m", message]
    out, err, rc = _run(args, path)
    if rc != 0:
        return (False, err.strip() or "git stash push failed")
    return (True, out.strip() or err.strip())


def git_stash_list(path) -> tuple:
    """Return (list_of_stash_strings, error)."""
    out, err, rc = _run(["stash", "list"], path)
    if rc != 0:
        return (None, err.strip() or "git stash list failed")
    lines = [l for l in out.splitlines() if l.strip()]
    return (lines, None)


def git_stash_pop(path) -> tuple:
    """git stash pop. Return (bool, output_or_error)."""
    out, err, rc = _run(["stash", "pop"], path)
    if rc != 0:
        return (False, err.strip() or "git stash pop failed")
    return (True, out.strip() or err.strip())


def git_stash_apply(path, index=0) -> tuple:
    """git stash apply stash@{index}. Return (bool, output_or_error)."""
    out, err, rc = _run(["stash", "apply", f"stash@{{{index}}}"], path)
    if rc != 0:
        return (False, err.strip() or "git stash apply failed")
    return (True, out.strip() or err.strip())


def git_stash_drop(path, index=0) -> tuple:
    """git stash drop stash@{index}. Return (bool, output_or_error)."""
    out, err, rc = _run(["stash", "drop", f"stash@{{{index}}}"], path)
    if rc != 0:
        return (False, err.strip() or "git stash drop failed")
    return (True, out.strip() or err.strip())


# ── Log ───────────────────────────────────────────────────────────────────────

def git_log(path, count=20) -> tuple:
    """git log --oneline --graph --decorate -<count>. Return (output_str, error)."""
    out, err, rc = _run(["log", "--oneline", "--graph", "--decorate", f"-{count}"], path)
    if rc != 0:
        return (None, err.strip() or "git log failed")
    return (out, None)


# ── Undo operations ───────────────────────────────────────────────────────────

def git_reset_soft(path) -> tuple:
    """git reset --soft HEAD~1. Return (bool, output_or_error)."""
    out, err, rc = _run(["reset", "--soft", "HEAD~1"], path)
    if rc != 0:
        return (False, err.strip() or out.strip() or "git reset --soft failed")
    return (True, err.strip() or out.strip() or "Reset successful.")


def git_reset_mixed(path) -> tuple:
    """git reset --mixed HEAD~1. Return (bool, output_or_error)."""
    out, err, rc = _run(["reset", "--mixed", "HEAD~1"], path)
    if rc != 0:
        return (False, err.strip() or out.strip() or "git reset --mixed failed")
    return (True, err.strip() or out.strip() or "Reset successful.")


def git_unstage_all(path) -> tuple:
    """git reset HEAD (unstage everything). Return (bool, output_or_error)."""
    out, err, rc = _run(["reset", "HEAD"], path)
    # rc=1 means "nothing to unstage" which is acceptable
    if rc not in (0, 1):
        return (False, err.strip() or out.strip() or "git reset HEAD failed")
    return (True, out.strip() or err.strip() or "Unstaged all.")


def git_discard_all(path) -> tuple:
    """git checkout -- . (discard ALL unstaged changes). Return (bool, output_or_error)."""
    out, err, rc = _run(["checkout", "--", "."], path)
    if rc != 0:
        return (False, err.strip() or out.strip() or "git checkout -- . failed")
    return (True, out.strip() or "Changes discarded.")


def git_repo_summary(path) -> dict:
    p = pathlib.Path(path)
    if not p.exists() or not (p / ".git").exists():
        return {
            "path": str(path),
            "branch": "",
            "clean": False,
            "ahead": 0,
            "behind": 0,
            "status": "missing",
        }

    branch_out, _, branch_rc = _run(["rev-parse", "--abbrev-ref", "HEAD"], p)
    branch = branch_out.strip() if branch_rc == 0 else ""

    ahead, behind = 0, 0
    ab_out, _, ab_rc = _run(
        ["rev-list", "--left-right", "--count", "HEAD...@{upstream}"], p
    )
    if ab_rc == 0 and ab_out.strip():
        parts = ab_out.strip().split()
        if len(parts) == 2:
            try:
                ahead = int(parts[0])
                behind = int(parts[1])
            except ValueError:
                pass

    status_lines, status_err = git_status(p)
    if status_err is not None:
        clean = False
        status_str = "dirty"
    elif len(status_lines) == 0:
        clean = True
        status_str = "clean"
    else:
        clean = False
        status_str = "dirty"

    return {
        "path": str(path),
        "branch": branch,
        "clean": clean,
        "ahead": ahead,
        "behind": behind,
        "status": status_str,
    }
