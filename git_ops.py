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
