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


# ── Branch tests ──────────────────────────────────────────────────────────────

def test_branch_list_has_current(temp_repo):
    lines, err = git_ops.git_branch_list(temp_repo)
    assert err is None
    assert any("*" in l for l in lines)  # current branch marked


def test_branch_create_and_list(temp_repo):
    ok, out = git_ops.git_branch_create(temp_repo, "feature-x")
    assert ok, f"create failed: {out}"
    lines, _ = git_ops.git_branch_list(temp_repo)
    assert any("feature-x" in l for l in lines)


def test_branch_switch(temp_repo):
    git_ops.git_branch_create(temp_repo, "other")
    ok, out = git_ops.git_branch_switch(temp_repo, "other")
    assert ok, f"switch failed: {out}"


def test_branch_delete(temp_repo):
    git_ops.git_branch_create(temp_repo, "to-delete")
    git_ops.git_branch_switch(temp_repo, "main")  # switch away first
    # git might use 'master' as default — switch to whatever the initial branch is
    # Get current branch name
    lines, _ = git_ops.git_branch_list(temp_repo)
    current = next((l.strip().lstrip("* ") for l in lines if "*" in l), "main")
    # Create and switch away, then delete
    git_ops.git_branch_create(temp_repo, "deleteme")
    git_ops.git_branch_switch(temp_repo, current)
    ok, out = git_ops.git_branch_delete(temp_repo, "deleteme")
    assert ok, f"delete failed: {out}"


# ── Stash tests ───────────────────────────────────────────────────────────────

def test_stash_save_and_list(temp_repo):
    (temp_repo / "stashme.txt").write_text("stash content")
    git_ops.git_add_files(temp_repo, ["stashme.txt"])
    ok, out = git_ops.git_stash_save(temp_repo, "test stash")
    assert ok, f"stash save failed: {out}"
    entries, err = git_ops.git_stash_list(temp_repo)
    assert err is None
    assert len(entries) >= 1


def test_stash_pop(temp_repo):
    (temp_repo / "popme.txt").write_text("pop content")
    git_ops.git_add_files(temp_repo, ["popme.txt"])
    git_ops.git_stash_save(temp_repo)
    ok, out = git_ops.git_stash_pop(temp_repo)
    assert ok, f"stash pop failed: {out}"


def test_stash_drop(temp_repo):
    (temp_repo / "dropme.txt").write_text("drop content")
    git_ops.git_add_files(temp_repo, ["dropme.txt"])
    git_ops.git_stash_save(temp_repo)
    ok, out = git_ops.git_stash_drop(temp_repo, 0)
    assert ok, f"stash drop failed: {out}"
    entries, _ = git_ops.git_stash_list(temp_repo)
    assert len(entries) == 0


# ── Log test ──────────────────────────────────────────────────────────────────

def test_git_log_returns_commits(temp_repo):
    out, err = git_ops.git_log(temp_repo)
    assert err is None
    assert out is not None
    assert "init" in out.lower() or len(out) > 0  # the initial commit should appear


# ── Undo tests ────────────────────────────────────────────────────────────────

def test_git_reset_soft(temp_repo):
    (temp_repo / "undo.txt").write_text("undo")
    git_ops.git_add_files(temp_repo, ["."])
    git_ops.git_commit(temp_repo, "commit to undo")
    ok, out = git_ops.git_reset_soft(temp_repo)
    assert ok, f"reset soft failed: {out}"
    # File should still be staged after soft reset
    status, _ = git_ops.git_status(temp_repo)
    assert any("undo.txt" in l for l in status)


def test_git_reset_mixed(temp_repo):
    (temp_repo / "unmix.txt").write_text("unmix")
    git_ops.git_add_files(temp_repo, ["."])
    git_ops.git_commit(temp_repo, "commit to unmix")
    ok, out = git_ops.git_reset_mixed(temp_repo)
    assert ok, f"reset mixed failed: {out}"


def test_git_unstage_all(temp_repo):
    (temp_repo / "unstage.txt").write_text("unstage")
    git_ops.git_add_files(temp_repo, ["unstage.txt"])
    ok, out = git_ops.git_unstage_all(temp_repo)
    assert ok, f"unstage failed: {out}"


def test_git_discard_all(temp_repo):
    (temp_repo / "README.md").write_text("modified")
    ok, out = git_ops.git_discard_all(temp_repo)
    assert ok, f"discard failed: {out}"
    content = (temp_repo / "README.md").read_text()
    assert content == "# Test Repo\n"  # restored to committed state


# ── Branch tests ──────────────────────────────────────────────────────────────

def test_branch_list_has_current(temp_repo):
    lines, err = git_ops.git_branch_list(temp_repo)
    assert err is None
    assert any("*" in l for l in lines)


def test_branch_create_and_list(temp_repo):
    ok, out = git_ops.git_branch_create(temp_repo, "feature-x")
    assert ok, f"create failed: {out}"
    lines, _ = git_ops.git_branch_list(temp_repo)
    assert any("feature-x" in l for l in lines)


def test_branch_switch(temp_repo):
    git_ops.git_branch_create(temp_repo, "other-branch")
    # switch back to original branch
    lines, _ = git_ops.git_branch_list(temp_repo)
    original = next(
        (l.strip().lstrip("* ") for l in lines if "*" not in l and "other-branch" not in l),
        None
    )
    if original:
        ok, out = git_ops.git_branch_switch(temp_repo, original)
        assert ok, f"switch failed: {out}"


def test_branch_delete(temp_repo):
    lines, _ = git_ops.git_branch_list(temp_repo)
    current = next(l.strip().lstrip("* ") for l in lines if "*" in l)
    git_ops.git_branch_create(temp_repo, "deleteme")
    git_ops.git_branch_switch(temp_repo, current)
    ok, out = git_ops.git_branch_delete(temp_repo, "deleteme")
    assert ok, f"delete failed: {out}"
    lines, _ = git_ops.git_branch_list(temp_repo)
    assert not any("deleteme" in l for l in lines)


# ── Stash tests ───────────────────────────────────────────────────────────────

def test_stash_save_and_list(temp_repo):
    (temp_repo / "stashme.txt").write_text("stash content")
    git_ops.git_add_files(temp_repo, ["stashme.txt"])
    ok, out = git_ops.git_stash_save(temp_repo, "test stash")
    assert ok, f"stash save failed: {out}"
    entries, err = git_ops.git_stash_list(temp_repo)
    assert err is None
    assert len(entries) >= 1


def test_stash_pop(temp_repo):
    (temp_repo / "popme.txt").write_text("pop content")
    git_ops.git_add_files(temp_repo, ["popme.txt"])
    git_ops.git_stash_save(temp_repo)
    ok, out = git_ops.git_stash_pop(temp_repo)
    assert ok, f"stash pop failed: {out}"


def test_stash_drop(temp_repo):
    (temp_repo / "dropme.txt").write_text("drop content")
    git_ops.git_add_files(temp_repo, ["dropme.txt"])
    git_ops.git_stash_save(temp_repo)
    ok, out = git_ops.git_stash_drop(temp_repo, 0)
    assert ok, f"stash drop failed: {out}"
    entries, _ = git_ops.git_stash_list(temp_repo)
    assert len(entries) == 0


# ── Log test ──────────────────────────────────────────────────────────────────

def test_git_log_returns_commits(temp_repo):
    out, err = git_ops.git_log(temp_repo)
    assert err is None
    assert out is not None
    assert len(out) > 0


# ── Undo tests ────────────────────────────────────────────────────────────────

def test_git_reset_soft(temp_repo):
    (temp_repo / "undo.txt").write_text("undo")
    git_ops.git_add_files(temp_repo, ["."])
    git_ops.git_commit(temp_repo, "commit to undo")
    ok, out = git_ops.git_reset_soft(temp_repo)
    assert ok, f"reset soft failed: {out}"
    status, _ = git_ops.git_status(temp_repo)
    assert any("undo.txt" in l for l in status)


def test_git_reset_mixed(temp_repo):
    (temp_repo / "unmix.txt").write_text("unmix")
    git_ops.git_add_files(temp_repo, ["."])
    git_ops.git_commit(temp_repo, "commit to unmix")
    ok, out = git_ops.git_reset_mixed(temp_repo)
    assert ok, f"reset mixed failed: {out}"
    status, _ = git_ops.git_status(temp_repo)
    assert any("unmix.txt" in l for l in status)


def test_git_unstage_all(temp_repo):
    (temp_repo / "unstage.txt").write_text("unstage")
    git_ops.git_add_files(temp_repo, ["unstage.txt"])
    ok, out = git_ops.git_unstage_all(temp_repo)
    assert ok, f"unstage failed: {out}"
    status, _ = git_ops.git_status(temp_repo)
    assert any("unstage.txt" in l for l in status)


def test_git_discard_all(temp_repo):
    (temp_repo / "README.md").write_text("modified content")
    ok, out = git_ops.git_discard_all(temp_repo)
    assert ok, f"discard failed: {out}"
    content = (temp_repo / "README.md").read_text()
    assert content == "# Test Repo\n"
