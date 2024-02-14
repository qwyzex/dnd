from utils import C

# stdscr = curses.initscr()

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Weapon(Item):
    def __init__(self, name, description, damage, equipped):
        super().__init__(name, description)
        self.damage = damage
        self.equipped = False

class Armor(Item):
    def __init__(self, name, description, defense, equipped):
        super().__init__(name, description)
        self.defense = defense
        self.equipped = False

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Added {item.name} to inventory.")
        else:
            print("Inventory is full.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item.name} from inventory.")
        else:
            print(f"{item.name} not found in inventory.")

    def display(self):
        print("Inventory:")
        for item in self.items:
            print(f"- {C.cyan(item.name)}: {item.description}")

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
