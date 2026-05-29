#!/usr/bin/env bash
# MGitPi setup script — Raspberry Pi / Linux
set -euo pipefail

# ── Color helpers ──────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[  OK  ]${NC} $1"; }
err()  { echo -e "${RED}[ ERR  ]${NC} $1"; }
info() { echo -e "${CYAN}[ INFO ]${NC} $1"; }
warn() { echo -e "${YELLOW}[ WARN ]${NC} $1"; }

echo ""
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}${BOLD}       MGitPi Setup — Raspberry Pi / Linux Edition             ${NC}"
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECRETS_DIR="$SCRIPT_DIR/secrets"
SECRETS_FILE="$SECRETS_DIR/credentials.env"
EXAMPLE_FILE="$SCRIPT_DIR/secrets.example/credentials.env"

# ── 1. Python 3.10+ ────────────────────────────────────────────────────────────
info "Checking Python..."
if ! command -v python3 &>/dev/null; then
    err "python3 not found. Install Python 3.10+ first."
    exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    err "Python 3.10+ required. Found: $PY_VER"
    exit 1
fi
ok "Python $PY_VER"

# ── 2. Git ─────────────────────────────────────────────────────────────────────
info "Checking Git..."
if ! command -v git &>/dev/null; then
    warn "Git not found."
    if command -v apt-get &>/dev/null; then
        info "Installing git via apt-get..."
        sudo apt-get update -qq && sudo apt-get install -y git -qq
        ok "Git installed."
    else
        err "Please install git manually and re-run setup."
        exit 1
    fi
else
    GIT_VER=$(git --version | awk '{print $3}')
    ok "Git $GIT_VER"
fi

# ── 3. Dev dependencies (pytest) ───────────────────────────────────────────────
info "Installing dev dependencies..."
if python3 -m pip install -r "$SCRIPT_DIR/requirements-dev.txt" -q 2>/dev/null; then
    ok "pytest installed"
else
    warn "Could not install pytest (non-fatal — only needed for running tests)"
fi

# ── 4. MGitPi data directory ───────────────────────────────────────────────────
MGITPI_DIR="$HOME/.mgitpi"
mkdir -p "$MGITPI_DIR"
ok "Data directory: $MGITPI_DIR"

# ── 5. Secrets / credentials ───────────────────────────────────────────────────
if [ ! -f "$SECRETS_FILE" ]; then
    warn "No credentials file found."
    info "Creating secrets/ from template..."
    mkdir -p "$SECRETS_DIR"
    cp "$EXAMPLE_FILE" "$SECRETS_FILE"
    echo ""
    echo -e "${YELLOW}  Next step: edit secrets/credentials.env with your SSH details.${NC}"
    echo "  Example:"
    echo "    nano $SECRETS_FILE"
    echo ""
    echo "  Then re-run: bash setup.sh"
    echo ""
    exit 0
fi

# Load credentials (ignore blank lines and comments)
while IFS='=' read -r key value; do
    [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
    key="${key// /}"
    value="${value%%#*}"   # strip inline comments
    value="${value%"${value##*[! ]}"}"  # strip trailing whitespace
    export "$key"="$value"
done < "$SECRETS_FILE"

ok "Credentials loaded from secrets/credentials.env"

# ── 6. SSH key setup ───────────────────────────────────────────────────────────
info "Setting up SSH..."
SSH_DIR="$HOME/.ssh"
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

GITHUB_HOST="${GITHUB_HOST:-github.com}"
SSH_KEY_PATH="${SSH_KEY_PATH:-~/.ssh/id_ed25519}"
EXPANDED_KEY="${SSH_KEY_PATH/#\~/$HOME}"

# If a key was placed inside secrets/, copy it to ~/.ssh/
LOCAL_PRIV="$SECRETS_DIR/id_ed25519"
LOCAL_PUB="$SECRETS_DIR/id_ed25519.pub"
if [ -f "$LOCAL_PRIV" ]; then
    info "Installing SSH key from secrets/ → ~/.ssh/"
    cp "$LOCAL_PRIV" "$EXPANDED_KEY"
    chmod 600 "$EXPANDED_KEY"
    [ -f "$LOCAL_PUB" ] && cp "$LOCAL_PUB" "${EXPANDED_KEY}.pub"
    ok "SSH key copied to $EXPANDED_KEY"
fi

# Generate a new key if still not found
if [ ! -f "$EXPANDED_KEY" ]; then
    warn "SSH key not found at: $EXPANDED_KEY"
    info "Generating new ED25519 SSH key..."
    EMAIL="${GITHUB_USERNAME:-mgitpi}@mgitpi"
    PASSPHRASE="${SSH_PASSPHRASE:-}"
    ssh-keygen -t ed25519 -C "$EMAIL" -f "$EXPANDED_KEY" -N "$PASSPHRASE" -q
    ok "New SSH key generated: $EXPANDED_KEY"

    echo ""
    echo -e "${YELLOW}${BOLD}  Add this public key to your GitHub account:${NC}"
    echo -e "${YELLOW}  GitHub → Settings → SSH and GPG keys → New SSH key${NC}"
    echo ""
    cat "${EXPANDED_KEY}.pub"
    echo ""
    read -r -p "  Press Enter once you've added the key to GitHub..."
fi

ok "SSH key: $EXPANDED_KEY"

# ── 7. ~/.ssh/config entry ────────────────────────────────────────────────────
SSH_CONFIG="$SSH_DIR/config"
touch "$SSH_CONFIG"
chmod 600 "$SSH_CONFIG"

if ! grep -q "Host $GITHUB_HOST" "$SSH_CONFIG" 2>/dev/null; then
    info "Adding $GITHUB_HOST to ~/.ssh/config..."
    cat >> "$SSH_CONFIG" << EOF

Host $GITHUB_HOST
    HostName $GITHUB_HOST
    User git
    IdentityFile $EXPANDED_KEY
    AddKeysToAgent yes
    IdentitiesOnly yes
EOF
    ok "~/.ssh/config updated for $GITHUB_HOST"
else
    ok "~/.ssh/config already has $GITHUB_HOST entry"
fi

# ── 8. ssh-agent ──────────────────────────────────────────────────────────────
info "Loading key into ssh-agent..."
eval "$(ssh-agent -s)" > /dev/null 2>&1 || true

if [ -f "$EXPANDED_KEY" ]; then
    PASSPHRASE="${SSH_PASSPHRASE:-}"
    if [ -n "$PASSPHRASE" ]; then
        SSH_ASKPASS_REQUIRE=force SSH_ASKPASS=/bin/echo \
            ssh-add "$EXPANDED_KEY" <<< "$PASSPHRASE" 2>/dev/null || \
        ssh-add "$EXPANDED_KEY" 2>/dev/null || true
    else
        ssh-add "$EXPANDED_KEY" 2>/dev/null || true
    fi
    ok "Key loaded into ssh-agent"
fi

# ── 9. Test SSH connection ────────────────────────────────────────────────────
info "Testing SSH connection to $GITHUB_HOST..."
SSH_OUTPUT=$(ssh -T "git@$GITHUB_HOST" \
    -o StrictHostKeyChecking=no \
    -o ConnectTimeout=8 \
    -o BatchMode=yes 2>&1 || true)

if echo "$SSH_OUTPUT" | grep -qi "success\|Hi \|welcome"; then
    ok "SSH connection to $GITHUB_HOST — authenticated"
elif echo "$SSH_OUTPUT" | grep -qi "Permission denied"; then
    warn "SSH auth failed — make sure your public key is added to $GITHUB_HOST"
    echo ""
    echo "  Public key:"
    cat "${EXPANDED_KEY}.pub" 2>/dev/null || echo "  (key file not found)"
else
    warn "SSH test result: $SSH_OUTPUT"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}${BOLD}  Setup complete!${NC}"
echo ""
echo "  Run the app:   python3 main.py"
echo "  Run tests:     python3 -m pytest tests/ -v"
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
