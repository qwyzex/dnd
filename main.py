import time
import json
from utils import C, clears, title_wide
from inventory import Item, Weapon, Armor, Inventory
from player import Player
from dungeon import Dungeon

def welcome(player):
    print(f"\nWelcome to the Doodlings n\' Ducklings game, {C.cyan(player.name)}!")
    print("Type 'help' for a list of commands.")

def main():
    clears()
    title_wide()

    # Save player data in local json file
    def save_game(player):
        player_data = {
            "name": player.name,
            "level": player.level,
            "experience": player.experience,
            "health_max": player.health_max,
            "current_health": player.current_health,
            "attack_power": player.attack_power,
            "inventory": player.inventory,
            "equipped_items": player.equipped_items,
            "currency_gold": player.currency_gold
        }

        with open("dnd_save_file.json", "w") as file:
            json.dump(player_data, file)

    # Check if there is an existing save file
    try:
        with open("dnd_save_file.json", "r") as file:
            p = json.load(file)
            player = Player(p["name"], [p["level"], p["epperience"]], p["inventory"], p["equipped_items"], [p["health_map_base"], p["health_map_item"], p["current_health"]], [p["attack_power_base"], p["attack_power_item"]], p["currency_gold"])
    except FileNotFoundError:
        print("N E W   G A M E")

        # Initialize new player
        print("\nCreating new Character...")
        player_name = ""
        while True:
            player_name = input("Enter your player name: ").strip().upper()
            if not player_name == "":
                break
            elif player_name == "":
                player_name = "Warrior"
                break

        # New player object instantiation
        player = Player(player_name, level=[1, 0], inventory=Inventory(capacity=20), equipped_items={"weapon": None, "armor": None}, health=[100, 0, 100], attack_power=[4, 0], gold=0)  # Adjust initial stats as needed
        player.inventory.items.append(Weapon("Wooden Sword", "Fragile short sword made of Alp wood.", 4, "a")) # Beginner sword

    welcome(player)

    # Main game loop
    while True:
        # Main player input
        command = input("\n@> ").strip().lower()
        print("")

        # Commands condition
        if command == "help":
            print("Available commands:")
            print(" - stat: Display player's current stats")
            print(" - statfull: Display detailed player's stats")
            print(" - bag/inventory: Display current inventory")
            print(" - rest: Restore full health")
            print(" - explore: Explore the dungeon")
            print(" - quit: Exit the game")
        elif command == "stat":
            player.stat()
        elif command == "statfull" or command == "statf":
            player.statf()
        elif command == "bag" or command == "inventory":
            player.display_inventory()
        elif command == "rest":
            player.rest(player.health_max)
        elif command == "explore" or command == "expl":
            dungeon_explore(player)
        elif command == "quit" or command == "exit" or command == "logout":
            quit_confirmation = input(f"!> Are you sure you want to exit the game? [Enter, yes/no] ").strip().lower()
            if quit_confirmation == "yes" or quit_confirmation == "y" or quit_confirmation == "":
                print("\n   Exiting the game. Goodbye!\n")
                # uncomment the line below to save player data
                #save_game(player)
                break
            elif quit_confirmation == "no" or quit_confirmation == "n" :
                print("\n   Cancelled.")
        else:
            print(C.yellow("   Invalid command. Type 'help' for a list of commands."))

# Dungeon System
def dungeon_explore(player):
    # Create a dungeon with 11 rooms
    dungeon = Dungeon(11, player)

    # Explore each room in the dungeon
    print(C.green("   Entering Dungeon..."))
    input(f"\n@> Press {C.cyan('Enter')} to explore the first room... ")
    while player.current_room <= dungeon.length and player.current_health > 0:
        if player.current_room > 1:
            interroominput = input(f"\n@> Press {C.cyan('Enter')} to explore the next room or see stat... ").strip().lower()
        else:
            interroominput = ""
        # Give option to see current stat inbetween rooms
        if player.current_room > 1 and interroominput == "stat" or interroominput == "statfull":
            player.statf()
            input(f"\n@> Press {C.cyan('Enter')} to explore the next room... ")
            dungeon.explore_room()
        else:
            dungeon.explore_room()

        # Player dies and get rescued by the village guard
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
        choice = input("\n!> Do you want to continue the adventure? (yes/no): ").strip().lower()
        print("")
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
