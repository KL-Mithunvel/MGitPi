# secrets/ — SSH Credentials

This folder stores your SSH credentials for MGitPi's SSH setup.

**The `secrets/` folder is gitignored — never commit your actual credentials.**

---

## Quick Setup

```bash
# 1. Copy the template
cp secrets.example/credentials.env secrets/credentials.env

# 2. Edit with your values (SSH key path, passphrase, GitHub username)
nano secrets/credentials.env

# 3. (Optional) Place your SSH private key directly in the secrets folder.
#    The setup script will copy it to ~/.ssh/ automatically.
cp ~/.ssh/id_ed25519     secrets/id_ed25519
cp ~/.ssh/id_ed25519.pub secrets/id_ed25519.pub

# 4. Run setup
bash setup.sh        # Linux / Raspberry Pi
setup.bat            # Windows
```

---

## Folder Contents

| File | Purpose |
|------|---------|
| `credentials.env` | SSH settings — key path, passphrase, username, host |
| `id_ed25519` | *(optional)* Private SSH key — copied to `~/.ssh/` by setup |
| `id_ed25519.pub` | *(optional)* Matching public key |

---

## How the Setup Script Uses These

1. **Reads** `credentials.env` to get `SSH_KEY_PATH`, `SSH_PASSPHRASE`, `GITHUB_HOST`
2. **Copies** `secrets/id_ed25519` → `~/.ssh/id_ed25519` if the file is present
3. **Generates** a new ED25519 key if no key exists at `SSH_KEY_PATH`
4. **Updates** `~/.ssh/config` with a Host entry for `GITHUB_HOST`
5. **Adds** the key to `ssh-agent` (using `SSH_PASSPHRASE` if set)
6. **Tests** the connection with `ssh -T git@GITHUB_HOST`

---

## Security Notes

- Keep `secrets/` out of any backup tools that sync to the cloud.
- If your Pi is shared, use a passphrase on the SSH key.
- Rotate keys regularly: generate a new one and update GitHub's SSH keys page.
