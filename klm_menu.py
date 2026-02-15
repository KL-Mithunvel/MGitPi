# klm_menu.py  (fix module error + fix weird chars + keep your names)
# IMPORTANT FIXES:
# 1) present_menu EXISTS (your error was because your klm_menu.py got overwritten without it)
# 2) Stop stripping ESC (it was turning "\033[36m" into "[36m")
# 3) Remove ONLY the form-feed "\f" from any printed box content
# 4) Banner uses art.brand_banner() and does NOT include header text anymore

import os
import re
import shutil
import art  # <-- new file

M_CMD = 0
M_PROMPT = 1
M_HOTKEY = 2

back_option = ["back", "Back...", "b"]

ANSI = True  # keep consistent with art.py if needed


def _clear():
    os.system("clear" if os.name != "nt" else "cls")


def _term_width(default=90):
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return default


def _strip_formfeed(s: str) -> str:
    # remove ONLY the \f (form feed) which shows as that weird character
    return str(s).replace("\f", "")


def _pad(s, w):
    s = _strip_formfeed(str(s))
    if len(s) > w:
        return s[: max(0, w - 1)] + "…"
    return s + " " * (w - len(s))


def _box(lines, width=90, title=None):
    out = []
    inner = width - 2
    out.append("┌" + "─" * inner + "┐")

    if title:
        t = f"[ {title} ]"
        left = max(0, (inner - len(t)) // 2)
        right = inner - len(t) - left
        out.append("│" + ("─" * left) + t + ("─" * right) + "│")

    for ln in lines:
        out.append("│" + _pad(ln, inner) + "│")

    out.append("└" + "─" * inner + "┘")
    return "\n".join(out)


# -------------------------
# YOUR ORIGINAL FLOW (same)
# -------------------------

def present_menu(menu_to_present, menu_system):
    menu = menu_system[menu_to_present]
    while menu is not None:
        display_menu(menu)
        act = get_menu_input(menu)
        if ":" in act:
            menu_name = act.split(":")[1]
            menu = menu_system[menu_name]
        else:
            menu_name = menu["name"]
            return act, menu_name


def print_banner(width=90):
    # static brand banner only (no header here)
    print(art.brand_banner(width=width))


def display_menu(menu_dict):
    _clear()

    # clamp to terminal width to prevent right-side artifacts
    width = menu_dict.get("width", 90)
    width = max(60, min(width, _term_width() - 2))

    # brand banner
    print_banner(width=width)
    print()

    # menu title INSIDE menu box (as you want)
    menu_title = menu_dict["menu"]

    lines = []
    lines.append("Select an option:")
    lines.append("")

    index = 1
    for opt in menu_dict["options"]:
        prompt = opt[M_PROMPT]
        hotkey = opt[M_HOTKEY]
        left = f"{index:>2}) {prompt}"
        right = f"({hotkey})"
        gap = (width - 2) - len(left) - len(right)
        if gap < 1:
            gap = 1
        lines.append(left + (" " * gap) + right)
        index += 1

    if menu_dict["back_option"]:
        left = f"{index:>2}) {back_option[M_PROMPT]}"
        right = f"({back_option[M_HOTKEY]})"
        gap = (width - 2) - len(left) - len(right)
        if gap < 1:
            gap = 1
        lines.append(left + (" " * gap) + right)

    print(_box(lines, width=width, title=menu_title))
    print()


def get_menu_input(menu):
    valid_chars = get_valid_hotkeys(menu)
    max_num = get_valid_choice_nums(menu)

    while True:
        inp = input("Perform action >> ").strip()

        # Quit ONLY if the menu explicitly allows it (main menu only)
        if menu.get("allow_quit", False) and inp.lower() == "q":
            return "exit"

        if not inp.isalnum():
            print("Invalid input.")
            continue

        if inp.isdigit():
            choice_num = int(inp)
            if 0 < choice_num <= max_num:
                return get_menu_cmd_for_input(menu, choice_num)
            print("Invalid number entered. ", end="")
            continue

        if inp.isalpha():
            ch = inp.lower()
            if ch in valid_chars:
                return get_menu_cmd_for_input(menu, ch)
            print("Invalid character entered. ", end="")
            continue


def get_valid_hotkeys(menu):
    hotkeys = []
    for i in menu["options"]:
        hotkeys.append(i[M_HOTKEY])
    if menu["back_option"]:
        hotkeys.append(back_option[M_HOTKEY])
    return hotkeys


def get_valid_choice_nums(menu):
    return len(menu["options"]) + (1 if menu["back_option"] else 0)


def get_menu_cmd_for_input(menu, inp):
    if type(inp) is str:
        if inp == back_option[M_HOTKEY] and menu["back_option"]:
            return "menu:" + menu["back_to"]
        for i in menu["options"]:
            if i[M_HOTKEY] == inp:
                return i[M_CMD]

    if type(inp) is int:
        options = menu["options"]
        if inp == len(options) + 1 and menu["back_option"]:
            return "menu:" + menu["back_to"]
        return options[inp - 1][M_CMD]
