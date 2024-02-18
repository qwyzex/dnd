from utils import C

# Base item class
class Item:
    def __init__(self, name, description):
        self.type = "ordinary"
        self.name = name
        self.description = description

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type
        }

# Item type weapon
class Weapon(Item):
    def __init__(self, name, level, description, damage, rarity, equipped):
        super().__init__(name, description)
        self.type = "weapon"
        self.level = level
        self.damage_raw = damage
        self.damage = self.damage_raw * self.level
        self.equipped = equipped
        self.rarity = rarity

    def to_json(self):
        return {
            "name" : self.name,
            "level": self.level,
            "description": self.description,
            "type" : self.type,
            "damage" : self.damage_raw,
            "equipped" : self.equipped,
            "rarity" : self.rarity
        }

# Item type armor
class Armor(Item):
    def __init__(self, name, level, description, defense, rarity, equipped):
        super().__init__(name, description)
        self.type = "armor"
        self.level = level
        self.defense_raw = defense
        self.defense = self.defense_raw * self.level
        self.equipped = equipped
        self.rarity = rarity

    def to_json(self):
        return {
            "name" : self.name,
            "level": self.level,
            "description": self.description,
            "type" : self.type,
            "defense" : self.defense_raw,
            "equipped" : self.equipped,
            "rarity" : self.rarity
        }

# Main inventory class
class Inventory:
    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"\nAdded {item.name} to inventory.")
        else:
            print("Inventory is full.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item.name} from inventory.")
        else:
            print(f"{item.name} not found in inventory.")

# class InventoryScreen:

    # OLD INVENTORY SCREEN WITH CURSES LIB

    # def __init__(self, items):
    #     self.items = items
    #     self.selected_index = 0
    #
    # def display(self, stdscr):
    #     stdscr.clear()
    #     stdscr.addstr(0, 0, "Inventory:")
    #     for i, item in enumerate(self.items):
    #         if i == self.selected_index:
    #             stdscr.addstr(i + 1, 0, f"> {item}")
    #         else:
    #             stdscr.addstr(i + 1, 0, f"  {item}")
    #     stdscr.refresh()
    #
    # def handle_input(self, stdscr):
    #     key = stdscr.getch()
    #     if key == curses.KEY_UP:
    #         self.selected_index = max(0, self.selected_index - 1)
    #     elif key == curses.KEY_DOWN:
    #         self.selected_index = min(len(self.items) - 1, self.selected_index + 1)
    #     elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
    #         selected_item = self.items[self.selected_index]
    #         # Do something with the selected item
    #         stdscr.addstr(len(self.items) + 2, 0, f"Selected item: {selected_item}")
    #         stdscr.refresh()
