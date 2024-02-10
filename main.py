import colorama
from colorama import Fore, Style
from player import Player
from dungeon import Dungeon

colorama.init()

def main():
    # Initialize player
    player_name = input("Enter your player name: ")
    player = Player(player_name, max_health=100, attack_power=20)  # You can adjust initial stats as needed

    print("Welcome to the Doodling n Duckling game!")
    print("Type 'help' for a list of commands.")

    # Main game loop
    while True:
        command = input(">> ").lower()

        if command == "help":
            print("Available commands:")
            print(" - stat: Display player's current stats")
            print(" - statfull: Display detailed player's stats")
            print(" - explore: Explore the dungeon")
            print(" - quit: Exit the game")
        elif command == "stat":
            player.stat()
        elif command == "statfull":
            player.statf()
        elif command == "explore":
            dungeon_explore(player)
        elif command == "quit":
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid command. Type 'help' for a list of commands.")

def dungeon_explore(player):
    # Create a dungeon with 10 rooms
    dungeon = Dungeon(11, player)

    # Explore each room in the dungeon
    print(f'{Fore.YELLOW}>> Entering Dungeon...{Style.RESET_ALL}')
    while player.current_room <= dungeon.length:
        input(">> Press Enter to explore the next room...")
        dungeon.explore_room()

    # After exploring all rooms
    print(">> You have explored all the rooms in the dungeon.")

    # Ask the player if they want to continue the adventure or exit the dungeon
    choice = input(">> Do you want to continue the adventure? (yes/no): ").lower()
    if choice == "yes" or choice == "y":
        player.current_room = 1
        dungeon_explore(player)
    elif choice == "no" or choice == "n":
        player.current_room = 1
        print(">> Exiting the dungeon. Goodbye!")
    else:
        print(">> Invalid input. Please choose between the options.")

if __name__ == "__main__":
    main()
