import json
import pathlib
import datetime

MGITPI_DIR    = pathlib.Path.home() / ".mgitpi"
REPOS_FILE    = MGITPI_DIR / "repos.json"
HISTORY_FILE  = MGITPI_DIR / "history.json"
SNAPSHOT_FILE = MGITPI_DIR / "status_snapshot.json"


def _ensure_dir():
    MGITPI_DIR.mkdir(parents=True, exist_ok=True)


def load_repos() -> list:
    if not REPOS_FILE.exists():
        return []
    try:
        with open(REPOS_FILE, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []


def save_repos(repos: list):
    _ensure_dir()
    with open(REPOS_FILE, "w") as f:
        json.dump(repos, f, indent=2)


def add_repo(path: str):
    resolved = pathlib.Path(path).resolve()
    if not resolved.exists():
        return (False, f"Path does not exist: {resolved}")
    if not (resolved / ".git").exists():
        return (False, f"Not a git repository (no .git): {resolved}")
    repos = load_repos()
    path_str = str(resolved)
    if path_str in repos:
        return (False, f"Already in list: {path_str}")
    repos.append(path_str)
    save_repos(repos)
    _log_event("added", path_str)
    return (True, None)


def remove_repo(path: str):
    resolved = str(pathlib.Path(path).resolve())
    repos = load_repos()
    if resolved not in repos:
        return (False, f"Not in list: {resolved}")
    repos.remove(resolved)
    save_repos(repos)
    _log_event("removed", resolved)
    return (True, None)


def validate_repos() -> list:
    repos = load_repos()
    results = []
    for p in repos:
        rp = pathlib.Path(p)
        if not rp.exists():
            results.append((p, "missing"))
        elif not (rp / ".git").exists():
            results.append((p, "no .git"))
        else:
            results.append((p, "ok"))
    _log_event("validated", f"{len(repos)} repos checked")
    return results


def _log_event(event: str, detail: str):
    _ensure_dir()
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
            if not isinstance(history, list):
                history = []
        except Exception:
            history = []
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    history.append({"event": event, "detail": detail, "ts": ts})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def save_status_snapshot(snapshots: list):
    _ensure_dir()
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    data = {"ts": ts, "repos": snapshots}
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_status_snapshot():
    if not SNAPSHOT_FILE.exists():
        return None
    try:
        with open(SNAPSHOT_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return None
