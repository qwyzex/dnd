from player import Player

def main():
    # Initialize player
    player_name = input("Enter your player name: ")
    player = Player(player_name, max_health=100, attack_power=10)  # You can adjust initial stats as needed

    print("Welcome to the Doodling n Duckling game!")
    print("Type 'help' for a list of commands.")

    # Main game loop
    while True:
        command = input(">> ").lower()

        if command == "help":
            print("Available commands:")
            print(" - stat: Display player's current stats")
            print(" - statfull: Display detailed player's stats")
            print(" - attack: Attack an enemy")
            print(" - heavy_attack: Perform a heavy attack (cooldown: 5 turns)")
            print(" - rest: Rest and restore health")
            print(" - quit: Exit the game")

        elif command == "stat":
            player.stat()

        elif command == "statfull":
            player.statfull()

        elif command == "attack":
            # Placeholder for attack functionality
            pass

        elif command == "heavy_attack":
            # Placeholder for heavy attack functionality
            pass

        elif command == "rest":
            # Placeholder for rest functionality
            pass

        elif command == "quit":
            print("Exiting the game. Goodbye!")
            break

        else:
            print("Invalid command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()
