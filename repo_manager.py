import json
from pathlib import Path

_DATA_DIR = Path.home() / ".mgitpi"
_REPOS_FILE = _DATA_DIR / "repos.json"


def _ensure_dir():
    _DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_repos():
    _ensure_dir()
    if not _REPOS_FILE.exists():
        return []
    try:
        with open(_REPOS_FILE, "r") as f:
            return json.load(f).get("repos", [])
    except Exception:
        return []


def save_repos(repos):
    _ensure_dir()
    with open(_REPOS_FILE, "w") as f:
        json.dump({"repos": repos}, f, indent=2)


def add_repo(path):
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return False, f"Path does not exist: {p}"
    if not (p / ".git").exists():
        return False, f"Not a git repo (no .git folder): {p}"
    repos = load_repos()
    s = str(p)
    if s in repos:
        return False, "Already in saved list."
    repos.append(s)
    save_repos(repos)
    return True, s


def remove_repo(index):
    repos = load_repos()
    if index < 0 or index >= len(repos):
        return False, "Invalid selection."
    removed = repos.pop(index)
    save_repos(repos)
    return True, removed


def validate_repos():
    repos = load_repos()
    results = []
    for r in repos:
        p = Path(r)
        if not p.exists():
            results.append((r, "missing directory"))
        elif not (p / ".git").exists():
            results.append((r, "no .git folder"))
        else:
            results.append((r, "ok"))
    return results
