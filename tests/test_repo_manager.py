import sys
import json
import pathlib
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import repo_manager


@pytest.fixture(autouse=True)
def redirect_paths(tmp_path, monkeypatch):
    mgitpi_dir = tmp_path / ".mgitpi"
    mgitpi_dir.mkdir()
    monkeypatch.setattr(repo_manager, "MGITPI_DIR",    mgitpi_dir)
    monkeypatch.setattr(repo_manager, "REPOS_FILE",    mgitpi_dir / "repos.json")
    monkeypatch.setattr(repo_manager, "HISTORY_FILE",  mgitpi_dir / "history.json")
    monkeypatch.setattr(repo_manager, "SNAPSHOT_FILE", mgitpi_dir / "status_snapshot.json")


@pytest.fixture
def git_repo(tmp_path):
    repo_dir = tmp_path / "myrepo"
    repo_dir.mkdir()
    (repo_dir / ".git").mkdir()
    return repo_dir


def test_load_repos_empty():
    result = repo_manager.load_repos()
    assert result == []


def test_add_valid_repo(git_repo):
    ok, err = repo_manager.add_repo(str(git_repo))
    assert ok is True
    assert err is None
    repos = repo_manager.load_repos()
    assert str(git_repo) in repos


def test_add_nonexistent_path(tmp_path):
    missing = tmp_path / "does_not_exist"
    ok, err = repo_manager.add_repo(str(missing))
    assert ok is False
    assert "does not exist" in err.lower() or "not exist" in err.lower()


def test_add_non_git_directory(tmp_path):
    plain_dir = tmp_path / "notgit"
    plain_dir.mkdir()
    ok, err = repo_manager.add_repo(str(plain_dir))
    assert ok is False
    assert ".git" in err


def test_add_duplicate_repo(git_repo):
    repo_manager.add_repo(str(git_repo))
    ok, err = repo_manager.add_repo(str(git_repo))
    assert ok is False
    assert err is not None


def test_remove_existing_repo(git_repo):
    repo_manager.add_repo(str(git_repo))
    ok, err = repo_manager.remove_repo(str(git_repo))
    assert ok is True
    assert err is None
    repos = repo_manager.load_repos()
    assert str(git_repo) not in repos


def test_remove_nonexistent_repo(tmp_path):
    ok, err = repo_manager.remove_repo(str(tmp_path / "ghost"))
    assert ok is False
    assert err is not None


def test_validate_ok_repo(git_repo):
    repo_manager.add_repo(str(git_repo))
    results = repo_manager.validate_repos()
    path_status = {p: s for p, s in results}
    assert path_status[str(git_repo)] == "ok"


def test_validate_missing_repo(tmp_path):
    missing = tmp_path / "gone"
    missing.mkdir()
    (missing / ".git").mkdir()
    repo_manager.add_repo(str(missing))
    missing.rename(tmp_path / "gone_renamed")
    results = repo_manager.validate_repos()
    path_status = {p: s for p, s in results}
    assert path_status[str(missing)] == "missing"


def test_validate_non_git_dir(tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    repos = repo_manager.load_repos()
    repos.append(str(plain))
    repo_manager.save_repos(repos)
    results = repo_manager.validate_repos()
    path_status = {p: s for p, s in results}
    assert path_status[str(plain)] == "no .git"


def test_history_add_logged(git_repo):
    repo_manager.add_repo(str(git_repo))
    with open(repo_manager.HISTORY_FILE) as f:
        history = json.load(f)
    events = [e["event"] for e in history]
    assert "added" in events


def test_history_remove_logged(git_repo):
    repo_manager.add_repo(str(git_repo))
    repo_manager.remove_repo(str(git_repo))
    with open(repo_manager.HISTORY_FILE) as f:
        history = json.load(f)
    events = [e["event"] for e in history]
    assert "removed" in events


def test_history_validate_logged(git_repo):
    repo_manager.add_repo(str(git_repo))
    repo_manager.validate_repos()
    with open(repo_manager.HISTORY_FILE) as f:
        history = json.load(f)
    events = [e["event"] for e in history]
    assert "validated" in events


def test_save_load_snapshot_roundtrip():
    snapshots = [
        {"path": "/some/repo", "branch": "main", "clean": True, "ahead": 0, "behind": 0, "status": "clean"}
    ]
    repo_manager.save_status_snapshot(snapshots)
    loaded = repo_manager.load_status_snapshot()
    assert loaded is not None
    assert "repos" in loaded
    assert loaded["repos"] == snapshots
    assert "ts" in loaded


def test_load_snapshot_missing_file():
    result = repo_manager.load_status_snapshot()
    assert result is None
