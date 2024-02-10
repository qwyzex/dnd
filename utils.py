import colorama
from colorama import Fore, Style

colorama.init()

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
