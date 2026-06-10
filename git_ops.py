import subprocess
from pathlib import Path


def _run(cmd, cwd=None):
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def git_clone(url, dest_dir=None):
    if dest_dir is None:
        dest_dir = str(Path.home())
    out, err, rc = _run(["git", "clone", url], cwd=dest_dir)
    if rc != 0:
        return None, err or "Clone failed."
    folder = url.rstrip("/").split("/")[-1]
    if folder.endswith(".git"):
        folder = folder[:-4]
    return str(Path(dest_dir) / folder), None


def git_status(repo_path):
    out, err, rc = _run(["git", "status"], cwd=repo_path)
    if rc != 0:
        return None, err
    return out, None


def git_add_all(repo_path):
    _, err, rc = _run(["git", "add", "-A"], cwd=repo_path)
    if rc != 0:
        return False, err
    return True, None


def git_commit(repo_path, message):
    out, err, rc = _run(["git", "commit", "-m", message], cwd=repo_path)
    if rc != 0:
        return False, err or "Commit failed (nothing staged?)"
    return True, out


def git_pull(repo_path):
    out, err, rc = _run(["git", "pull"], cwd=repo_path)
    if rc != 0:
        return False, err
    return True, out


def git_push(repo_path):
    out, err, rc = _run(["git", "push"], cwd=repo_path)
    if rc != 0:
        return False, err
    return True, out


def git_list_branches(repo_path):
    out, err, rc = _run(["git", "branch", "-a"], cwd=repo_path)
    if rc != 0:
        return None, err
    return out, None


def git_checkout(repo_path, branch):
    out, err, rc = _run(["git", "checkout", branch], cwd=repo_path)
    if rc != 0:
        return False, err
    return True, out


def git_log(repo_path, n=15):
    out, err, rc = _run(
        ["git", "log", "--oneline", "--decorate", f"-{n}"], cwd=repo_path
    )
    if rc != 0:
        return None, err
    return out, None
