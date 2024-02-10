from player import Player
from dungeon import Dungeon

def main():
    # Initialize player
    player_name = input("Enter your player name: ")
    player = Player(player_name, max_health=100, attack_power=10)  # You can adjust initial stats as needed

    dungeon = Dungeon(10, player)

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
            dungeon.explore_room()
        elif command == "quit":
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()
