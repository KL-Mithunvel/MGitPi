# MGitPi — Raspberry Pi Hardware Testing Checklist

Run these tests in order on real Pi hardware. Each test has a setup step,
what to do, and what a passing result looks like.

Tick each box as you go. A single `[ FAIL ]` should be noted with the error
message before moving on.

---

## 0. Pre-flight

### 0.1 Python version

```bash
python3 --version
```

**Pass:** `Python 3.10.x` or higher is shown.

---

### 0.2 Git version

```bash
git --version
```

**Pass:** Any version is shown (e.g. `git version 2.39.2`).

---

### 0.3 Terminal width

```bash
tput cols
```

**Pass:** Value is at least `80`. If less, widen the terminal window before continuing.

---

### 0.4 SSH key exists

```bash
ls ~/.ssh/id_ed25519
```

**Pass:** File exists. If not, run `bash setup.sh` first (see Section 1).

---

## 1. Setup Script

### 1.1 First-time run (no credentials file)

```bash
bash setup.sh
```

**What to check:**

- `[INFO] Creating secrets/ from template...` message appears.
- `secrets/credentials.env` is created.
- Script exits asking you to edit the file.

**Pass:** File `secrets/credentials.env` now exists.

---

### 1.2 Credentials edit

```bash
nano secrets/credentials.env
```

Set your values:
```
SSH_KEY_PATH=~/.ssh/id_ed25519
SSH_PASSPHRASE=        ← leave blank or add yours
GITHUB_USERNAME=your_github_username
GITHUB_HOST=github.com
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

---

### 1.3 Full setup run

```bash
bash setup.sh
```

**What to check (in order):**

- `[ OK ] Python 3.x.x`
- `[ OK ] Git x.x.x`
- `[ OK ] pytest installed`
- `[ OK ] Data directory: /home/pi/.mgitpi`
- `[ OK ] Credentials loaded`
- `[ OK ] SSH key: ~/.ssh/id_ed25519`
- `[ OK ] ~/.ssh/config updated for github.com` (or "already has entry")
- `[ OK ] Key loaded into ssh-agent`
- `[ OK ] SSH connection to github.com — authenticated`

**Pass:** All lines show `[ OK ]`. The last line reads `Setup complete!`

---

### 1.4 Data directory created

```bash
ls ~/.mgitpi/
```

**Pass:** Directory exists (may be empty at this stage).

---

## 2. Application Launch

### 2.1 Splash screen

```bash
python3 main.py
```

**What to check:**

- Screen clears.
- Large ASCII block-letter logo renders without wrapping.
- Project name, tagline, and author shown below the logo.
- Screen clears after a few seconds and the menu appears.

**Pass:** No visual glitches; text fits within the terminal width.

---

### 2.2 Brand banner

After the splash, look at the top of the screen.

**Pass:** A box with `[ MGITPI ]` centered and the tagline below it is shown before every menu.

---

### 2.3 Workspace menu loads

**Pass:** Menu box appears with options 1–7 and their hotkeys `(o)(p)(c)(a)(r)(v)(x)`.

---

## 3. Menu Navigation

### 3.1 Hotkey input

At the workspace menu, type `v` then Enter.

**Pass:** Validate action runs (shows "No repos saved." or a list). Returns to menu after pressing Enter.

---

### 3.2 Number input

At the workspace menu, type `6` then Enter. (6 is Validate)

**Pass:** Same result as 3.1.

---

### 3.3 Invalid input — rejected silently

Type `z` then Enter (not a valid hotkey).

**Pass:** Prompt repeats. No crash. No error message printed — just prompts again.

---

### 3.4 Invalid number — rejected silently

Type `99` then Enter.

**Pass:** Prompt repeats silently.

---

### 3.5 Help system — workspace menu

Type `?` then Enter.

**Pass:**
- Screen clears.
- A help box appears listing every option with a description.
- Pressing Enter returns to the menu.

---

### 3.6 Back navigation

From the workspace menu, press `o` to open repo. Then press `b` to go back.

**Pass:** Returns to workspace menu cleanly.

---

## 4. Repo Management

> For this section, you need at least one git repository on your Pi.
> Create a test repo if you don't have one:
> ```bash
> mkdir ~/test-repo && cd ~/test-repo && git init && git commit --allow-empty -m "init"
> ```

### 4.1 Add a repo

At workspace menu → `a` (Add repo).

Enter the path: `/home/pi/test-repo` (or wherever your test repo is).

**Pass:** "Repo added." message shown.

---

### 4.2 Validate repo list — shows OK

At workspace menu → `v` (Validate).

**Pass:** `[ OK ]  /home/pi/test-repo  (ok)` shown.

---

### 4.3 Validate with missing repo

Manually add a fake path:

```bash
python3 -c "
import json, pathlib
f = pathlib.Path.home() / '.mgitpi/repos.json'
data = json.loads(f.read_text())
data['repos'].append('/home/pi/nonexistent-repo')
f.write_text(json.dumps(data, indent=2))
"
```

Then at workspace menu → `v` (Validate).

**Pass:** `[ OK ]` for the real repo, `[ERR]` for the fake path. Both shown clearly.

Remove the fake path:

```bash
python3 -c "
import json, pathlib
f = pathlib.Path.home() / '.mgitpi/repos.json'
data = json.loads(f.read_text())
data['repos'] = [r for r in data['repos'] if 'nonexistent' not in r]
f.write_text(json.dumps(data, indent=2))
"
```

---

### 4.4 Open repo from saved list

At workspace menu → `o` (Open repo).

**Pass:**
- Numbered list of saved repos shown.
- Type `1` → Repo menu loads, showing the repo path in the title.

---

### 4.5 Open repo by path (one-time)

At workspace menu → `p` (Open by path).

Enter the path to your test repo.

**Pass:** Repo menu loads without saving to the list.

---

### 4.6 Remove a repo

At workspace menu → `r` (Remove repo).

Select the repo from the list.

**Pass:** "Removed." message. Validate list (`v`) now shows it gone.

Add it back via `a` before continuing.

---

### 4.7 History log written

```bash
cat ~/.mgitpi/history.json
```

**Pass:** JSON array with events like:
```json
[
  {"event": "added",   "detail": "/home/pi/test-repo", "ts": "2026-..."},
  {"event": "validated", "detail": "...",              "ts": "2026-..."},
  {"event": "removed", "detail": "/home/pi/test-repo", "ts": "2026-..."},
  {"event": "added",   "detail": "/home/pi/test-repo", "ts": "2026-..."}
]
```

---

### 4.8 Status snapshot written on launch

Exit the app (`x`) and re-launch (`python3 main.py`).

```bash
cat ~/.mgitpi/status_snapshot.json
```

**Pass:** JSON with `"ts"` field and `"repos"` array showing each repo's branch, clean/dirty status, and ahead/behind counts.

---

## 5. Git Operations (inside Repo Menu)

> Open your test repo: workspace → `o` → select it.
> Make sure the repo has at least one commit.

### 5.1 Status — clean repo

In repo menu → `s` (Status).

**Pass:** Full `git status` output shown. Reads "nothing to commit, working tree clean."

---

### 5.2 Status — dirty repo

```bash
echo "test change" >> ~/test-repo/README.md
```

Then in repo menu → `s`.

**Pass:** Shows `README.md` as modified.

---

### 5.3 Stage specific files

In repo menu → `a` (Stage changes).

**Pass:**
- Numbered list of changed files shown.
- Type `1` (the README.md entry).
- "Staged." message shown.
- Run Status again — README.md now shows as staged (green `M` in short status).

---

### 5.4 Stage all

Add another file:

```bash
echo "new" > ~/test-repo/newfile.txt
```

In repo menu → `a` (Stage changes).

Type `all` at the prompt.

**Pass:** "Staged." shown. Both files appear as staged in status.

---

### 5.5 Commit

In repo menu → `c` (Commit).

Enter message: `test commit from MGitPi`

**Pass:** Git commit summary shown (hash, branch, message). No error.

---

### 5.6 Help on repo menu

In repo menu → `?`

**Pass:** Help box shows descriptions for Status, Stage changes, Commit, Pull, Push, etc.

---

### 5.7 Push

In repo menu → `p` (Push).

**Pass (if remote configured):** "Everything up-to-date" or upload progress shown.
**Pass (no remote):** Error message shown clearly. Does not crash.

---

### 5.8 Pull

In repo menu → `u` (Pull).

**Pass (if remote configured):** "Already up to date." or changes listed.
**Pass (no remote):** Error message shown clearly. Does not crash.

---

## 6. Branch Tools

> From repo menu → `b` (Branch tools)

### 6.1 List branches

In branch menu → `l` (List branches).

**Pass:** At least one branch shown. Current branch has `*` prefix.

---

### 6.2 Create branch

In branch menu → `c` (Create branch).

Enter name: `test-feature`

**Pass:** Branch created and switched. Run List again — `* test-feature` shown.

---

### 6.3 Switch branch

In branch menu → `s` (Switch branch).

Enter the original branch name (e.g., `main` or `master`).

**Pass:** Branch switched. List shows `*` on the original branch.

---

### 6.4 Delete branch

In branch menu → `d` (Delete branch).

Select `test-feature` from the list.

Confirm with `y`.

**Pass:** Branch deleted. List no longer shows `test-feature`.

---

### 6.5 Help on branch menu

In branch menu → `?`

**Pass:** Descriptions for List, Switch, Create, Delete shown.

---

## 7. Stash Tools

> Make an unstaged change first:
> ```bash
> echo "stash me" >> ~/test-repo/README.md
> ```
> From repo menu → `t` (Stash tools)

### 7.1 Stash save

In stash menu → `s` (Stash save).

Enter message: `wip changes`

**Pass:** Stash saved. Running Status in repo menu shows clean working tree.

---

### 7.2 Stash list

In stash menu → `l` (Stash list).

**Pass:** `stash@{0}: On <branch>: wip changes` shown.

---

### 7.3 Stash pop

In stash menu → `p` (Stash pop).

**Pass:** Changes restored. Stash list is now empty. Status shows README.md modified again.

---

### 7.4 Stash drop

Save again: stash menu → `s`, message `drop this`.

Then in stash menu → `d` (Stash drop).

Select index `0`. Confirm with `y`.

**Pass:** Stash list is empty. Changes are gone.

---

## 8. Log Viewer

> From repo menu → `g` (Log)

### 8.1 Log output

**Pass:**
- Commit history shown with hash, branch decoration, and message.
- At minimum the `init` commit and `test commit from MGitPi` are visible.
- Pressing Enter returns to repo menu.

---

## 9. Undo Tools

> From repo menu → `u` (Undo / Cleanup)

### 9.1 Undo last commit — soft (cancel test)

In undo menu → `s` (Undo soft).

Type `n` at the confirmation.

**Pass:** "Cancelled." shown. Commit is still there (check log).

---

### 9.2 Undo last commit — soft (confirm)

Make and commit a throwaway change:

```bash
echo "throwaway" > ~/test-repo/throwaway.txt
git -C ~/test-repo add . && git -C ~/test-repo commit -m "throwaway"
```

In undo menu → `s`. Confirm `y`.

**Pass:** Commit undone. `throwaway.txt` is still staged. Log no longer shows "throwaway" commit.

---

### 9.3 Unstage all

In undo menu → `u` (Unstage all). Confirm `y`.

**Pass:** `throwaway.txt` is now untracked/unstaged. Status shows it modified or untracked, not staged.

---

### 9.4 Discard all — wrong confirmation rejected

In undo menu → `x` (Discard ALL changes).

At the prompt, type `yes` (not `discard`).

**Pass:** "Cancelled." shown. Files unchanged.

---

### 9.5 Discard all — correct confirmation

In undo menu → `x`.

Type `discard` at the prompt.

**Pass:** All unstaged changes discarded. Working tree is clean.

---

## 10. Clone

> From workspace menu → `c` (Clone repo)

### 10.1 Clone a repo

Enter an SSH URL to a repo you have access to:

```
git@github.com:your-username/your-repo.git
```

Enter destination directory: `/home/pi` (or any existing directory)

**Pass:** Clone completes. `ls /home/pi/your-repo` shows the repo contents.

---

### 10.2 Clone invalid URL

Enter a fake SSH URL: `git@github.com:nobody/doesnotexist12345.git`

**Pass:** Clear error message shown. App does not crash. Returns to workspace menu.

---

## 11. Edge Cases

### 11.1 Open repo with empty saved list

Remove all repos (or use a fresh `~/.mgitpi/repos.json`), then workspace → `o`.

**Pass:** "No repos saved. Use 'a' to add one." shown. No crash.

---

### 11.2 Add non-existent path

Workspace → `a`. Enter `/home/pi/this-does-not-exist`.

**Pass:** Error message "Path does not exist" shown.

---

### 11.3 Add non-git directory

```bash
mkdir ~/not-a-git-dir
```

Workspace → `a`. Enter `/home/pi/not-a-git-dir`.

**Pass:** Error message about missing `.git` folder shown.

---

### 11.4 Commit with nothing staged

In a clean repo, repo menu → `c` (Commit). Enter any message.

**Pass:** Error shown (nothing to commit). No crash.

---

### 11.5 Narrow terminal test (80 columns)

Resize your terminal to exactly 80 columns:

```bash
printf '\033[8;24;80t'    # resize to 80×24 (works in most terminal emulators)
```

Then `python3 main.py`.

**Pass:** Menus render without line wrapping or garbled characters.

---

### 11.6 Very narrow terminal test (60 columns)

Resize to 60 columns:

```bash
printf '\033[8;24;60t'
```

**Pass:** Menu boxes adapt. Text may truncate (`…`) rather than wrap.

---

## 12. Graceful Recovery

### 12.1 Corrupt repos.json

```bash
echo "NOT JSON" > ~/.mgitpi/repos.json
python3 main.py
```

**Pass:** App launches normally. Repo list is empty. No crash or Python traceback.

Restore: `echo '{"repos":[]}' > ~/.mgitpi/repos.json`

---

### 12.2 Missing .mgitpi directory

```bash
rm -rf ~/.mgitpi
python3 main.py
```

**Pass:** App creates `~/.mgitpi/` automatically on first repo operation. No crash.

---

## 13. Test Summary Table

Copy this and tick off as you complete each section:

```
[ ] 0. Pre-flight checks
[ ] 1. Setup script
[ ] 2. Application launch
[ ] 3. Menu navigation
[ ] 4. Repo management
[ ] 5. Git operations
[ ] 6. Branch tools
[ ] 7. Stash tools
[ ] 8. Log viewer
[ ] 9. Undo tools
[ ] 10. Clone
[ ] 11. Edge cases
[ ] 12. Graceful recovery
```

---

## Notes

Use this section to record any failures when testing on hardware:

```
Date tested  :
Pi model     :
OS version   :
Python ver   :
Git version  :
Terminal     :

Failures:
- [ ] Section X.Y — <description of what went wrong>
```
