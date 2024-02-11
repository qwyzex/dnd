import time
from utils import C, clears
from player import Player
from dungeon import Dungeon

def welcome(player):
    print(f"\nWelcome to the Doodling n Duckling game, {C.cyan(player.name)}!")
    print("Type 'help' for a list of commands.")

def main():
    # Initialize player
    player_name = input("Enter your player name: ")
    player = Player(player_name, max_health=100, attack_power=20)  # You can adjust initial stats as needed

    welcome(player)

    # Main game loop
    while True:
        command = input("\n>> ").lower()

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
            print("Exiting the game. Goodbye!\n")
            break
        else:
            print("Invalid command. Type 'help' for a list of commands.")

def dungeon_explore(player):
    # Create a dungeon with 10 rooms
    dungeon = Dungeon(11, player)

    # Explore each room in the dungeon
    print(C.yellow("\n   Entering Dungeon..."))
    while player.current_room <= dungeon.length:
        interroominput = input(f"\n>> Press {C.cyan("Enter")} to explore the next room... ").lower()
        if interroominput == "stat" or interroominput == "statfull":
            player.statf()
            input(f"\n>> Press {C.cyan("Enter")} to explore the next room... ")
            dungeon.explore_room()
        else:
            dungeon.explore_room()

    # After exploring all rooms
    print("\n   You have explored all the rooms in the dungeon.")

    # Ask the player if they want to continue the adventure or exit the dungeon
    choice = input("\n>> Do you want to continue the adventure? (yes/no): ").lower()
    if choice == "yes" or choice == "y":
        player.current_room = 1
        dungeon_explore(player)
    elif choice == "no" or choice == "n":
        player.current_room = 1
        print(">> Exiting the dungeon. Goodbye!")
        time.sleep(2)
        clears()
        welcome(player)
    else:
        print(">> Invalid input. Please choose between the options.")

if __name__ == "__main__":
    main()
