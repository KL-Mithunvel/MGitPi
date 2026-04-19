import os
import sys
import shutil

# Windows setup: enable ANSI colors and switch stdout to UTF-8
if os.name == "nt":
    import ctypes
    ctypes.windll.kernel32.SetConsoleMode(
        ctypes.windll.kernel32.GetStdHandle(-11), 7
    )
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Project Identity ───────────────────────────────────────────────────────────
# Change these 4 lines to fully rebrand the splash and banner for any project.
PROJECT_NAME    = "MGITPI"
PROJECT_TAGLINE = "Git Control Interface for Raspberry Pi"
PROJECT_AUTHOR  = "mithunvel-kl"
ACCENT_COLOR    = "cyan"   # cyan | green | yellow | magenta | blue | red

# ── ANSI Toggle ────────────────────────────────────────────────────────────────
ANSI = True


# ── Color Helpers ──────────────────────────────────────────────────────────────

def _c(text, code):
    if not ANSI:
        return text
    return f"\033[{code}m{text}\033[0m"


def accent(t):
    """Apply the configured ACCENT_COLOR to text."""
    _codes = {
        "cyan":    "36",
        "green":   "32",
        "yellow":  "33",
        "magenta": "35",
        "blue":    "34",
        "red":     "31",
    }
    return _c(t, _codes.get(ACCENT_COLOR, "36"))


def cyan(t):    return _c(t, "36")
def green(t):   return _c(t, "32")
def yellow(t):  return _c(t, "33")
def magenta(t): return _c(t, "35")
def blue(t):    return _c(t, "34")
def red(t):     return _c(t, "31")
def dim(t):     return _c(t, "2")
def bold(t):    return _c(t, "1")


# ── Terminal Utilities ─────────────────────────────────────────────────────────

def clear():
    if ANSI:
        # ANSI clear works in any ANSI-capable terminal (PyCharm, Windows Terminal, Linux).
        # os.system("cls") is intentionally avoided: it spawns a subprocess whose
        # exit code leaks as a stray "0" into PyCharm's terminal emulator.
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    elif os.name == "nt":
        os.system("cls")  # fallback: ANSI disabled, plain Windows console


def term_width(default=90):
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return default


def center(s, w):
    s = str(s)
    visible = _strip_ansi(s)
    pad = max(0, w - len(visible))
    left = pad // 2
    right = pad - left
    return (" " * left) + s + (" " * right)


def _strip_ansi(s):
    """Return string with ANSI escape codes removed (for length calculations)."""
    result = []
    i = 0
    while i < len(s):
        if s[i] == "\033" and i + 1 < len(s) and s[i + 1] == "[":
            i += 2
            while i < len(s) and s[i] not in "mABCDEFGHJKSTfn":
                i += 1
            i += 1
        else:
            result.append(s[i])
            i += 1
    return "".join(result)


# ── Built-in ASCII Block Font (A–Z, 0–9, common symbols) ──────────────────────
# Each character is exactly 6 lines.  The renderer pads lines to equal width
# per character before joining them side-by-side.

_FONT = {
    ' ': ["    ", "    ", "    ", "    ", "    ", "    "],

    'A': ["   /\\   ", "  /  \\  ", " / /\\ \\ ", "/ ____ \\", "/_/  \\_\\", "        "],
    'B': [" ____  ", "|  _ \\ ", "| |_) |", "|  _ < ", "| |_) |", "|____/ "],
    'C': ["  _____ ", " / ____|", "| |     ", "| |     ", "| |____ ", " \\_____|"],
    'D': [" _____  ", "|  __ \\ ", "| |  | |", "| |  | |", "| |__| |", "|_____/ "],
    'E': [" ______ ", "|  ____|", "| |__   ", "|  __|  ", "| |____ ", "|______|"],
    'F': [" ______ ", "|  ____|", "| |__   ", "|  __|  ", "| |     ", "|_|     "],
    'G': ["  _____ ", " / ____|", "| |  __ ", "| | |_ |", "| |__| |", " \\_____|"],
    'H': [" _    _ ", "| |  | |", "| |__| |", "|  __  |", "| |  | |", "|_|  |_|"],
    'I': [" _____ ", "|_   _|", "  | |  ", "  | |  ", " _| |_ ", "|_____|"],
    'J': ["      _ ", "     | |", "     | |", " _   | |", "| |__| |", " \\____/ "],
    'K': [" _  __ ", "| |/ / ", "| ' /  ", "|  <   ", "| . \\ ", "|_|\\_\\"],
    'L': [" _      ", "| |     ", "| |     ", "| |     ", "| |____ ", "|______|"],
    'M': [" __  __ ", "|  \\/  |", "| \\  / |", "| |\\/| |", "| |  | |", "|_|  |_|"],
    'N': [" _   _ ", "| \\ | |", "|  \\| |", "| . ` |", "| |\\  |", "|_| \\_|"],
    'O': ["  ____  ", " / __ \\ ", "| |  | |", "| |  | |", "| |__| |", " \\____/ "],
    'P': [" _____  ", "|  __ \\ ", "| |__) |", "|  ___/ ", "| |     ", "|_|     "],
    'Q': ["  ____  ", " / __ \\ ", "| |  | |", "| |  | |", "| |__\\| |", " \\___\\_\\"],
    'R': [" _____  ", "|  __ \\ ", "| |__) |", "|  _  / ", "| | \\ \\ ", "|_|  \\_\\"],
    'S': ["  _____ ", " / ____|", "| (___  ", " \\___ \\ ", " ____) |", "|_____/ "],
    'T': [" _______ ", "|__   __|", "   | |   ", "   | |   ", "   | |   ", "   |_|   "],
    'U': [" _    _ ", "| |  | |", "| |  | |", "| |  | |", "| |__| |", " \\____/ "],
    'V': ["__      __", "\\ \\    / /", " \\ \\  / / ", "  \\ \\/ /  ", "   \\  /   ", "    \\/    "],
    'W': ["__        __", "\\ \\      / /", " \\ \\ /\\ / / ", "  \\ V  V /  ", "   \\_/\\_/   ", "            "],
    'X': ["__   __", "\\ \\ / /", " \\ V / ", "  > <  ", " / . \\ ", "/_/ \\_\\"],
    'Y': ["__   __", "\\ \\ / /", " \\ V / ", "  | |  ", "  | |  ", "  |_|  "],
    'Z': [" ______", "|___  /", "   / / ", "  / /  ", " / /__ ", "/_____|"],

    '0': [" ___  ", "/ _ \\ ", "| | | |", "| |_| |", "\\___/ ", "      "],
    '1': [" _ ", "/  |", "| |", "| |", "|_|", "   "],
    '2': [" ___ ", "|_  )", " / / ", "/ /_ ", "/____|", "     "],
    '3': [" ___ ", "|_  )", " _) |", "/ __/", "\\___|", "     "],
    '4': [" _ _  ", "| | | ", "| | | ", "|_  _|", "  |_| ", "      "],
    '5': [" ___ ", "| __|", "|__ \\", " __) |", "|____/", "      "],
    '6': ["  __ ", " / / ", "/ _ \\", "| (_) |", "\\___/ ", "      "],
    '7': [" ____ ", "|__  |", "   / /", "  / / ", " /_/  ", "      "],
    '8': ["  _  ", " (_) ", " / \\ ", "| / \\ |", " \\_/ ", "      "],
    '9': ["  _  ", " (_) ", " / \\ ", " \\_, |", "  /_/ ", "      "],

    '-': ["      ", "      ", " ____ ", "|____|", "      ", "      "],
    '_': ["      ", "      ", "      ", "      ", " ____ ", "|____|"],
    '.': ["   ", "   ", "   ", "   ", " _ ", "(_)"],
    '!': [" _ ", "| |", "| |", "|_|", "(_)", "   "],
}


# ── ASCII Renderer ─────────────────────────────────────────────────────────────

def _render_ascii(text, max_width=None):
    """
    Render *text* as 6-line block letters using the built-in font.

    If the rendered result is wider than *max_width*, falls back to a simple
    box-framed title so the splash never overflows the terminal.
    """
    chars = []
    for ch in text.upper():
        if ch in _FONT:
            chars.append(_FONT[ch])
        # silently skip characters not in the font

    if not chars:
        return text

    # Pad every line of each character to that character's max line width
    normalized = []
    for char_lines in chars:
        w = max(len(l) for l in char_lines)
        normalized.append([l.ljust(w) for l in char_lines])

    # Join: stitch line-N of every character together with a 2-space gap
    rows = ["  ".join(c[row] for c in normalized) for row in range(6)]
    result = "\n".join(rows)

    if max_width and any(len(r) > max_width for r in rows):
        return _boxed_title(text, max_width)

    return result


def _boxed_title(text, width):
    """Fallback banner used when the ASCII art is too wide for the terminal."""
    inner = width - 4
    label = text.upper()[:inner]
    pad_l = (inner - len(label)) // 2
    pad_r = inner - len(label) - pad_l
    bar = "─" * (width - 2)
    return "\n".join([
        "┌" + bar + "┐",
        "│" + " " * (width - 2) + "│",
        "│  " + " " * pad_l + label + " " * pad_r + "  │",
        "│" + " " * (width - 2) + "│",
        "└" + bar + "┘",
        " " * (width),
    ])


# ── Splash Screen ──────────────────────────────────────────────────────────────

def splash(wait_sec=5):
    w = max(60, min(120, term_width(90)))
    clear()

    logo = _render_ascii(PROJECT_NAME, max_width=w - 4)

    logo_lines = [accent(center(line, w)) for line in logo.split("\n")]

    sep = dim(center("─" * min(40, w - 10), w))

    lines = (
        [""]
        + logo_lines
        + [
            "",
            sep,
            "",
            bold(accent(center(PROJECT_NAME, w))),
            dim(center(PROJECT_TAGLINE, w)),
            dim(center(f"by {PROJECT_AUTHOR}", w)),
            "",
            sep,
            "",
            dim(center("Loading menus...", w)),
        ]
    )

    print("\n".join(lines), flush=True)
    clear()


# ── Brand Banner (top of every menu screen) ───────────────────────────────────

def brand_banner(width=90):
    width = max(60, min(width, term_width(90)))
    inner = width - 2

    deco = "═" * inner
    title = f" [ {PROJECT_NAME} ] "
    subtitle = PROJECT_TAGLINE

    pad_left = max(0, (inner - len(title)) // 2)
    pad_right = inner - len(title) - pad_left
    title_line = ("─" * pad_left) + title + ("─" * pad_right)

    def _line(s):
        return "│" + s + "│"

    top = "┌" + "─" * inner + "┐"
    bot = "└" + "─" * inner + "┘"

    return "\n".join([
        top,
        _line(accent(deco)),
        _line(accent(title_line)),
        _line(accent(center(subtitle, inner))),
        _line(accent(deco)),
        bot,
    ])