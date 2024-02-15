import colorama
from colorama import Fore, Style

# Initiate colorama
colorama.init()

# Welcome title
def title_wide():
    print("")
    print("[\\][\\][/][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][\\][/][/]")
    print("   [\\][|]                                                                     [|][/]")
    print("      [|]  |||||||||||||||||||                        |||||||||||||||||||     [|]")
    print("      [|]    ||||||         |||                         ||||||         |||    [|]")
    print("      [|]     ||||           |||                         ||||           |||   [|]")
    print("      [|]     |||             ||| |||||||||||||     //   |||             |||  [|]")
    print("      [|]     |||             |||  ||||      ||||| //    |||             |||  [|]")
    print("      [|]     |||             ||| ||||         ||||      |||             |||  [|]")
    print("      [|]     |||             |||  |||         |||       |||             |||  [|]")
    print("      [|]     |||            |||   ||           ||       |||            |||   [|]")
    print("      [|]     ||||          |||    ||           ||       ||||          |||    [|]")
    print("      [|]    ||||||        |||    |||           |||     ||||||        |||     [|]")
    print("      [|]  ||||||||||||||||||    |||||         |||||  ||||||||||||||||||      [|]")
    print("      [|]                                                                     [|]")
    print("      [|]  D  O  O  D  L  I  N  G  S    A  N  D    D  U  C  K  L  I  N  G  S  [|]")
    print("   [/][|]                                                                     [|][\\]")
    print("[/][/][\\][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][-][/][\\][\\]")
    print("")

# Color class
class C:
    @staticmethod
    def red(text):
        return f"{Fore.RED}{text}{Fore.RESET}"
    @staticmethod
    def green(text):
        return f"{Fore.GREEN}{text}{Fore.RESET}"
    @staticmethod
    def blue(text):
        return f"{Fore.BLUE}{text}{Fore.RESET}"
    @staticmethod
    def yellow(text):
        return f"{Fore.YELLOW}{text}{Fore.RESET}"
    @staticmethod
    def magenta(text):
        return f"{Fore.MAGENTA}{text}{Fore.RESET}"
    @staticmethod
    def cyan(text):
        return f"{Fore.CYAN}{text}{Fore.RESET}"
    @staticmethod
    def white(text):
        return f"{Fore.WHITE}{text}{Fore.RESET}"

# Clear terminal screen
def clears():
    print('\033c', end='')

# Round number to 3 digits deep
def roundF(num):
    rounded_num = round(num, 3)  # Round to 3 decimal places
    last_digit = int(rounded_num * 1000) % 10  # Get the last digit after rounding
    if last_digit < 5:  # If the last digit is less than 5, round up
        rounded_num = round(rounded_num + 0.005, 2)  # Add 0.005 to round up
    else:  # If the last digit is greater than or equal to 5, round down
        rounded_num = round(rounded_num - 0.005, 2)  # Subtract 0.005 to round down
    return rounded_num
