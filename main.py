import time
from utils import C, clears
from player import Player
from dungeon import Dungeon

def welcome(player):
    print(f"\nWelcome to the Doodling n Duckling game, {C.cyan(player.name)}!")
    print("Type 'help' for a list of commands.")

def main():
    # Initialize player
    player_name = input("\nEnter your player name: ").strip().upper()
    player = Player(player_name, max_health=100, attack_power=10)  # Adjust initial stats as needed

    welcome(player)

    # Main game loop
    while True:
        command = input("\n>> ").strip().lower()
        print("")

        if command == "help":
            print("Available commands:")
            print(" - stat: Display player's current stats")
            print(" - statfull: Display detailed player's stats")
            print(" - rest: Restore full health")
            print(" - explore: Explore the dungeon")
            print(" - quit: Exit the game")
        elif command == "stat":
            player.stat()
        elif command == "statfull":
            player.statf()
        elif command == "rest":
            player.rest(player.max_health)
        elif command == "explore" or command == "expl":
            dungeon_explore(player)
        elif command == "quit":
            print("Exiting the game. Goodbye!\n")
            break
        else:
            print(C.yellow("   Invalid command. Type 'help' for a list of commands."))

def dungeon_explore(player):
    # Create a dungeon with 10 rooms
    dungeon = Dungeon(11, player)

    # Explore each room in the dungeon
    print(C.yellow("\n   Entering Dungeon..."))
    while player.current_room <= dungeon.length and player.current_health > 0:
        interroominput = input(f"\n>> Press {C.cyan('Enter')} to explore the next room or see stat... ").strip().lower()
        if interroominput == "stat" or interroominput == "statfull":
            player.statf()
            input(f"\n>> Press {C.cyan('Enter')} to explore the next room... ")
            dungeon.explore_room()
        else:
            dungeon.explore_room()

        if player.current_health <= 0:
            player.current_room = 1
            input(C.red("Returning to main village..."))
            clears()
            welcome(player)
            player.current_health = 1
            return False

    # After exploring all rooms
    print("\n   You have explored all the rooms in the dungeon.")

    # Ask the player if they want to continue the adventure or exit the dungeon
    while True:
        choice = input("\n>> Do you want to continue the adventure? (yes/no): ").strip().lower()
        if choice == "yes" or choice == "y":
            player.current_room = 1
            dungeon_explore(player)
            return False
        elif choice == "no" or choice == "n":
            player.current_room = 1
            print(">> Exiting the dungeon. Goodbye!")
            time.sleep(2)
            clears()
            welcome(player)
            return False
        else:
            print(C.yellow("\n   Invalid input. Please choose between the options."))

if __name__ == "__main__":
    main()
