def print_banner(header, width=70):
    title = "MGitPi"
    subtitle = "Git Control Interface for Raspberry Pi"

    top = "┌" + "─" * (width - 2) + "┐"
    empty = "│" + " " * (width - 2) + "│"
    mid1 = "│" + title.center(width - 2) + "│"
    mid2 = "│" + subtitle.center(width - 2) + "│"
    mid3 = "│" + header.center(width - 2) + "│"
    bot = "└" + "─" * (width - 2) + "┘"

    print("\n" + top)
    print(empty)
    print(mid1)
    print(mid2)
    print(empty)
    print(mid3)
    print(bot + "\n")
