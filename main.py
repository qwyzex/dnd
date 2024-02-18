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
        player_inventory = []
        for player_item in player.inventory.items:
            item_data = player_item.to_json()
            player_inventory.append(item_data)

        player_equipped_item_weapon_index = None
        player_equipped_item_armor_index = None

        if player.equipped_items["weapon"] is not None:
            for i, item in enumerate(player.inventory.items, start=0):
                if item == player.equipped_items["weapon"]:
                    player_equipped_item_weapon_index = i
            # player_equipped_item_weapon = player.equipped_items["weapon"].to_json()
        if player.equipped_items["armor"] is not None:
            for i, item in enumerate(player.inventory.items, start=0):
                if item == player.equipped_items["armor"]:
                    player_equipped_item_armor_index = i
                    # player_equipped_item_armor = player.equipped_items["armor"].to_json()

        player_equipped_items = {
            "weapon": player_equipped_item_weapon_index,
            "armor": player_equipped_item_armor_index
        }

        player_data = {
            "name": player.name,
            "level": player.level,
            "experience": player.experience,
            "health_max_base": player.health_max,
            "health_max_item": player.health_max_item,
            "current_health": player.current_health,
            "attack_power_base": player.attack_power_base,
            "attack_power_item": player.attack_power_item,
            "inventory_capacity": player.inventory.capacity,
            "inventory_items": player_inventory,
            "equipped_items": player_equipped_items,
            "currency_gold": player.currency_gold
        }

        with open("dnd_save_file.json", "w") as file:
            json.dump(player_data, file)
        print(C.green("   Game Saved Successfully!"))

    # Check if there is an existing save file
    try:
        with open("dnd_save_file.json", "r") as file:
            p = json.load(file)
            inventory_items = []
            for item_data in p["inventory_items"]:
                if item_data["type"] == "weapon":
                    item = Weapon(item_data["name"], item_data["level"], item_data["description"], item_data["damage"], item_data["rarity"], item_data["equipped"])
                elif item_data["type"] == "armor":
                    item = Armor(item_data["name"], item_data["level"], item_data["description"], item_data["defense"], item_data["rarity"], item_data["equipped"])
                else:
                    item = Item(item_data["name"], item_data["description"])
                inventory_items.append(item)

            player = Player(p["name"], [p["level"], p["experience"]], Inventory(p["inventory_capacity"], inventory_items), {"weapon": None, "armor": None}, [p["health_max_base"], p["health_max_item"], p["current_health"]], [p["attack_power_base"], p["attack_power_item"]], p["currency_gold"])
            if p["equipped_items"]["weapon"] is not None:
                pew_index = p["equipped_items"]["weapon"]
                player.equip_item(player.inventory.items[pew_index])
                # player.equipped_items[0] = player.inventory.items[pew_index]
                # equipped_item_weapon = Weapon(pew["name"], pew["description"], pew["damage"], pew["rarity"], pew["equipped"])
            if p["equipped_items"]["armor"] is not None:
                pea_index = p["equipped_items"]["armor"]
                player.equip_item(player.inventory.items[pea_index])
                # player.equipped_items[1] = player.inventory.items[pea_index]
                # equipped_item_armor = Armor(pea["name"], pea["description"], pea["defense"], pea["rarity"], pea["equipped"])
    except FileNotFoundError:
        # Initialize new player
        print("Creating new Character...")
        player_name = ""
        while True:
            player_name = input("Enter your player name: ").strip().upper()
            if not player_name == "":
                break
            elif player_name == "":
                player_name = "Warrior"
                break

        # New player object instantiation
        player = Player(player_name, level=[1, 0], inventory=Inventory(20, [Weapon("Wooden Sword", 1, "Fragile short sword made of Alp wood.", 4, "a", False)]), equipped_items={"weapon": None, "armor": None}, health=[100, 0, 100], attack_power=[4, 0], gold=0)  # Adjust initial stats as needed

    welcome(player)
    print("\nMAIN VILLAGE")

    # Main game loop
    while True:
        # Main player input
        command_raw = input("\n@> ").strip().lower()
        command_len = command_raw.split(" ")
        if len(command_len) == 1:
            command = command_len[0]
            flag = None
        elif len(command_len) == 2:
            command = command_len[0]
            flag = command_len[1]
        else:
            print(C.yellow("   Invalid input format. Cannot receive more than two values!"))

        print("") # Blank line

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
        elif command == "bag" or command == "inventory" or command == "i" or command == "char" or command =="Character":
            player.display_inventory(welcome)
        elif command == "rest":
            player.rest(player.health_max)
        elif command == "explore" or command == "expl":
            if flag is None or flag == "n" or flag == "normal":
                dungeon_explore(player, "normal")
            elif flag.isdigit():
                dungeon_explore(player, flag)
            elif flag == "s" or flag == "static":
                dungeon_explore(player, "static")
            elif flag == "b" or flag == "beginning":
                dungeon_explore(player, "beginning")
            else:
                print(C.yellow("   Invalid explore flag! Available expl flag: (number), static, beginning and normal!"))
        elif command == "save" or command == "sv":
            save_game(player)
        elif command == "quit" or command == "exit" or command == "logout":
            quit_confirmation = input(f"!> Are you sure you want to exit the game? [Enter, yes/no] ").strip().lower()
            if quit_confirmation == "yes" or quit_confirmation == "y" or quit_confirmation == "":
                # UN-COMMENT 2 LINE BELLOW TO SAVE PLAYER DATA AUTOMATICALLY BEFORE EXITING THE GAME
                print("")
                save_game(player)
                print("\n   Exiting the game. Goodbye!\n")
                break
            elif quit_confirmation == "no" or quit_confirmation == "n" :
                print("\n   Cancelled.")
        else:
            print(C.yellow("   Invalid command. Type 'help' for a list of commands."))

# Dungeon System
def dungeon_explore(player, flag):
    def determine_appropriate_tier():
        if player.level in range(1, 5):
            return 1
        elif player.level in range(5, 10):
            return 2
        elif player.level in range(10, 15):
            return 3
        elif player.level in range(15, 20):
            return 4
        elif player.level in range(20, 25):
            return 5
        elif player.level in range(25, 30):
            return 6
        elif player.level in range(30, 35):
            return 7
        elif player.level in range(35, 40):
            return 8
        elif player.level in range(40, 45):
            return 9
        elif player.level in range(45, 50):
            return 10
        elif player.level in range(50, 55):
            return 11
        elif player.level in range(55, 60):
            return 12
        elif player.level in range(60, 65):
            return 13
        elif player.level in range(65, 70):
            return 14
        elif player.level in range(70, 75):
            return 15
        elif player.level in range(75, 80):
            return 16
        elif player.level in range(80, 85):
            return 17
        elif player.level in range(85, 90):
            return 18
        elif player.level in range(90, 95):
            return 19
        elif player.level in range(95, 100):
            return 20
    appropriate_tier = determine_appropriate_tier()
    dungeon_tier = 1
    exit_confirmation_text = ""


    if flag.isdigit():
        dungeon_tier = int(flag)
        exit_confirmation_text = f"Do you want to re-play tier-{flag} dungeon? (yes/no): "
    elif flag == "static":
        dungeon_tier = appropriate_tier
        exit_confirmation_text = "Do you want to re-play the static dungeon? (yes/no): "
    elif flag == "beginning":
        exit_confirmation_text = "Do you want to continue the adventure? (yes/no): "
    elif flag == "normal":
        dungeon_tier = appropriate_tier
        exit_confirmation_text = "Do you want to continue the adventure? (yes/no): "
        # dungeon_tier += 1

    def explore(dungeon_tier):
        dungeon = Dungeon(11, player, min(10, dungeon_tier))
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
            choice = input(f"\n!> {exit_confirmation_text}").strip().lower()
            print("")
            if choice == "yes" or choice == "y":
                player.current_room = 1
                if flag.isdigit():
                    explore(dungeon_tier)
                elif flag == "static":
                    explore(dungeon_tier)
                elif flag == "beginning":
                    dungeon_tier += 1
                    explore(dungeon_tier)
                elif flag == "normal":
                    dungeon_tier += 1
                    explore(dungeon_tier)
                return False
            elif choice == "no" or choice == "n":
                player.current_room = 1
                print(">> Exiting the dungeon. Goodbye!")
                time.sleep(2)
                clears()
                print("MAIN VILLAGE")
                return False
            else:
                print(C.yellow("\n   Invalid input. Please choose between the options."))

    explore(dungeon_tier)

if __name__ == "__main__":
    main()
