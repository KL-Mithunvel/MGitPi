import sys
import pathlib
import subprocess
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import git_ops


@pytest.fixture
def temp_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=str(repo), check=True, capture_output=True)
    readme = repo / "README.md"
    readme.write_text("# Test Repo\n")
    subprocess.run(["git", "add", "."], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=str(repo), check=True, capture_output=True)
    return repo


def test_git_status_clean(temp_repo):
    lines, err = git_ops.git_status(temp_repo)
    assert err is None
    assert lines == []


def test_git_status_untracked_file(temp_repo):
    (temp_repo / "newfile.txt").write_text("hello")
    lines, err = git_ops.git_status(temp_repo)
    assert err is None
    assert any("newfile.txt" in l for l in lines)


def test_git_status_modified_file(temp_repo):
    (temp_repo / "README.md").write_text("# Modified\n")
    lines, err = git_ops.git_status(temp_repo)
    assert err is None
    assert any("README.md" in l for l in lines)


def test_git_status_not_a_repo(tmp_path):
    plain = tmp_path / "notrepo"
    plain.mkdir()
    lines, err = git_ops.git_status(plain)
    assert lines is None
    assert err is not None
    assert isinstance(err, str)
    assert len(err) > 0


def test_git_add_specific_file(temp_repo):
    new_file = temp_repo / "staged.txt"
    new_file.write_text("staged content")
    ok, err = git_ops.git_add_files(temp_repo, ["staged.txt"])
    assert ok is True
    assert err is None
    out, _, _ = git_ops._run(["status", "--short"], temp_repo)
    assert "staged.txt" in out


def test_git_add_all_dot(temp_repo):
    (temp_repo / "file1.txt").write_text("f1")
    (temp_repo / "file2.txt").write_text("f2")
    ok, err = git_ops.git_add_files(temp_repo, ["."])
    assert ok is True
    assert err is None
    out, _, _ = git_ops._run(["status", "--short"], temp_repo)
    assert "file1.txt" in out
    assert "file2.txt" in out


def test_git_commit_success(temp_repo):
    (temp_repo / "commit_me.txt").write_text("content")
    git_ops.git_add_files(temp_repo, ["."])
    ok, result = git_ops.git_commit(temp_repo, "test commit")
    assert ok is True
    assert isinstance(result, str)
    assert len(result) > 0


def test_git_commit_nothing_staged(temp_repo):
    ok, result = git_ops.git_commit(temp_repo, "nothing to commit")
    assert ok is False
    assert isinstance(result, str)
    assert len(result) > 0


def test_git_status_long_output(temp_repo):
    out, err = git_ops.git_status_long(temp_repo)
    assert err is None
    assert out is not None
    assert isinstance(out, str)
    assert len(out) > 0
    lower = out.lower()
    assert "nothing to commit" in lower or "clean" in lower or "branch" in lower


def test_git_repo_summary_clean(temp_repo):
    summary = git_ops.git_repo_summary(temp_repo)
    assert summary["status"] == "clean"
    assert summary["clean"] is True
    assert isinstance(summary["branch"], str)
    assert len(summary["branch"]) > 0


def test_git_repo_summary_dirty(temp_repo):
    (temp_repo / "dirty.txt").write_text("dirty")
    summary = git_ops.git_repo_summary(temp_repo)
    assert summary["status"] == "dirty"
    assert summary["clean"] is False


def test_git_repo_summary_missing(tmp_path):
    nonexistent = tmp_path / "no_such_dir"
    summary = git_ops.git_repo_summary(nonexistent)
    assert summary["status"] == "missing"


def test_git_clone_local(temp_repo, tmp_path):
    dest = tmp_path / "clones"
    dest.mkdir()
    ok, err = git_ops.git_clone(str(temp_repo), dest)
    assert ok is True
    assert err is None
    cloned = dest / temp_repo.name
    assert cloned.exists()
    assert (cloned / ".git").exists()
