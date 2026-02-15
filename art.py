# art.py  (new file)
# Reusable aesthetic / branding functions for MGitPi
# - No box for splash (as you asked)
# - Waits 5 seconds
# - Adds "KLM🎶" as part of the art
# - ANSI colors optional (works if your terminal supports it)

import os
import sys
import time
import shutil

ANSI = True  # set False if colors look weird in your terminal


def _c(text, code):
    if not ANSI:
        return text
    return f"\033[{code}m{text}\033[0m"


def cyan(t): return _c(t, "36")
def dim(t): return _c(t, "2")
def bold(t): return _c(t, "1")


def clear():
    # better clear for Windows + Linux
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def term_width(default=90):
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return default


def center(s, w):
    s = str(s)
    if len(s) >= w:
        return s[:w]
    left = (w - len(s)) // 2
    right = w - len(s) - left
    return (" " * left) + s + (" " * right)


def splash(wait_sec=5):
    w = max(60, min(120, term_width(90)))
    clear()

    lines = [
        cyan(""),
        cyan(center(" __  __    _____   _____   _____   _____   _____ ",w)),
        cyan(center("|  \/  |  / ____| |_   _| |_   _| |  __ \ |_   _|",w)),
        cyan(center("| \  / | | |  __    | |     | |   | |__) |  | |  ",w)),
        cyan(center("| |\/| | | | |_ |   | |     | |   |  ___/   | |  ",w)),
        cyan(center("| |  | | | |__| |  _| |_    | |   | |      _| |_ ",w)),
        cyan(center("|_|  |_|  \_____| |_____|   |_|   |_|     |_____|",w)),
        "",
        bold(cyan(center("WELCOME KLM🎶", w))),
        dim(center("Project: MGitPi", w)),
        dim(center("Made by: mithunvel-kl", w)),
        "",
        dim(center("Loading menus...", w)),
    ]

    # print raw (do NOT strip control chars here; ANSI needs ESC)
    print("\n".join(lines), flush=True)
    time.sleep(wait_sec)
    clear()


def brand_banner(width=90):
    """
    Static branding block for the top of menus (box-like but not required).
    Returns a STRING (so klm_menu can print it).
    """
    width = max(60, min(width, term_width(90)))
    inner = width - 2

    deco = "═" * inner
    title = " [ MGitPi ] "
    subtitle = "Git Control Interface for Raspberry Pi"

    def line(s):
        return "│" + s + "│"

    top = "┌" + "─" * inner + "┐"
    bot = "└" + "─" * inner + "┘"

    # center title inside a cyan deco line
    pad_left = max(0, (inner - len(title)) // 2)
    pad_right = inner - len(title) - pad_left
    title_line = ("─" * pad_left) + title + ("─" * pad_right)

    out = []
    out.append(top)
    out.append(line(cyan(deco)))
    out.append(line(cyan(title_line)))
    out.append(line(cyan(center(subtitle, inner))))
    out.append(line(cyan(deco)))
    out.append(bot)
    return "\n".join(out)
