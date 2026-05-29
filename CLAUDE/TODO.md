# TODO

## In Progress
- [ ] None currently

## Done
- [x] Splash screen with animated ASCII art and ANSI colors (`art.py`)
- [x] Menu engine (`klm_menu.py`) — hotkey navigation, back navigation, input validation
- [x] All menu structure definitions in `main.py` (workspace, repo, branch, stash, rebase, undo)
- [x] Terminal width detection and responsive layout
- [x] `art.py` — ANSI helpers, `clear()`, `center()`, `term_width()`
- [x] `repo_manager.py` stub file created
- [x] `git_ops.py` stub file created

## Not Started

### Core Git Operations (`git_ops.py`)
- [ ] Implement `git_status(repo_path)` — `git status --short`
- [ ] Implement `git_add_interactive(repo_path)` — show changed files, user selects
- [ ] Implement `git_commit(repo_path, message)` — `git commit -m`
- [ ] Implement `git_push(repo_path)` — `git push`
- [ ] Implement `git_pull(repo_path)` — `git pull`
- [ ] Implement `git_list_branches(repo_path)` — `git branch -a`
- [ ] Implement `git_checkout(repo_path, branch)` — `git checkout`
- [ ] Implement `git_create_branch(repo_path, name)` — `git checkout -b`
- [ ] Implement `git_delete_branch(repo_path, name)` — `git branch -d`
- [ ] Implement `git_stash(repo_path)` — `git stash`
- [ ] Implement `git_stash_pop(repo_path)` — `git stash pop`
- [ ] Implement `git_log(repo_path)` — formatted `git log`
- [ ] Implement `git_diff(repo_path)` — `git diff`
- [ ] Implement `git_reset(repo_path)` — `git reset`
- [ ] Implement `git_clone(url, target_dir)` — SSH clone workflow

### Repo Manager (`repo_manager.py`)
- [ ] Implement `load_repos()` — read `~/.mgitpi/repos.json`; auto-create if missing
- [ ] Implement `add_repo(path)` — validate path has `.git`, save to JSON
- [ ] Implement `remove_repo(path)` — remove entry from JSON
- [ ] Implement `validate_repos()` — check each saved path still exists and has `.git`

### Wiring
- [ ] Wire all `main.py` handler stubs to `git_ops` and `repo_manager` implementations

### UI
- [ ] Create `ui_box.py` with reusable UTF-8 box-drawing components
- [ ] Commit log viewer — formatted `git log` output displayed in a box
- [ ] Interactive `git diff` viewer

### Testing
- [ ] Set up `tests/` directory with pytest
- [ ] Write tests for all `git_ops.py` functions using `tempfile.mkdtemp()` repos
- [ ] Write tests for `repo_manager.py`
