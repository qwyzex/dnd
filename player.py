import random
from utils import roundF, C, clears
from libs import WorldItems
from inventory import Inventory, Weapon, Armor

class Player:
    # Load Instantiation
    #                                         Current experience for the next level        Currently equipped item state     Core stat of max health, increased by leveling up          Core stat of AP, increased by leveling up                        Player's gold left
    #                                                            |                                       |                          |                                                                          |                                                  |
    #                  Player's name    Current level           |      Inventory object as-is           |                          |    Item stat increasing total max health    Current health state         |    Item stat increasing total max health         |
    #                      /--|--\        /--|---\       /-----|-----\        /----|-----\       /-----|--------\         /-------|-------\         /-------|------\         /----|--------\          /------|-----------\       /--------|---------\        /--|----------\
    #                     |      |       |       |      |            |       |           |      |               |        |                |        |               |        |              |         |                   |      |                   |       |              |
    # player = Player(data["name"], [data["level"], data["experience"]], data["inventory"], data["equipped_items"], [data["health_max_base"], data["health_max_item"], data["current_health"]], [data["attack_power_base"], data["attack_power_item"]], data["currency_gold"])
    #                 \_________/   \____[0]____________[1]__________/   \______________/   \___________________/   \____[0]______________________[1]______________________[2]______________/   \____[0]________________________[1]_________________/   \__________________/
    #                      |                         |                          |                     |                                             |                                                                    |                                       |
    #                    Name             Level array, length 2             Inventory          Equipped Items                           Health array, length 3                                               Attack power array, length 2                      Gold
    #
    #                         [2]                                [3]       [2]
    def __init__(self, name, level, inventory, equipped_items, health, attack_power, gold):
        self.name = name
        # Level and Experience
        self.level = level[0]
        self.experience = level[1]
        self.experience_to_next_level = round(31 * self.level + (0.9 * (self.level - 1)))
        # Inventory
        self.inventory = inventory
        self.equipped_items = {
            "weapon": equipped_items["weapon"],
            "armor": equipped_items["armor"]
        }
        # Health Stat
        self.health_max_base = health[0]
            #self.health_max_item = self.equipped_items["armor"].defense if equipped_items["armor"] is not None else 0
        self.health_max_item = health[1]
        self.health_max = self.health_max_base + self.health_max_item
        self.current_health = health[2]
        # Power Stat
        self.attack_power_base = attack_power[0]
            #self.attack_power_item = self.equipped_items["weapon"].damage if equipped_items["weapon"] is not None else 0
        self.attack_power_item = attack_power[1]
        self.attack_power = self.attack_power_base + self. attack_power_item
        # Attack Blocking
        self.block_strength = round(self.level * 7.5 + self.health_max_item)
        self.is_blocking = False
        # Healing Potion
        self.heal_amount = self.level * 0.025
        self.heal_cooldown_duration = 3
        self.heal_cooldown = 0
        # Heavy Attack
        self.heavy_attack_mod = roundF(min(1.0 + (0.01 * self.level), 2.0))
        self.heavy_attack_cooldown_duration = 5 if self.level < 31 else 4 if self.level >= 31 and self.level < 61 else 3
        self.heavy_attack_cooldown = 0
        # Currencies
        self.currency_gold = gold
        # DUNGEONS
        self.current_room = 1

    # Player main functions
    def stat(self):
        print(f"   Name            : {self.name}")
        print(f"   Level           : {self.level}")
        print(f"   Experience      : {self.experience}/{self.experience_to_next_level}")
        print(f"   Health          : {self.current_health}/{self.health_max}")
        print(f"   Attack Power    : {self.attack_power}")
        print(f"   Gold            : {self.currency_gold}")
        print(f"   Inventory       : {len(self.inventory.items)}/{self.inventory.capacity}")

    def statf(self):
        print(f"   Name            : {self.name}")
        print(f"   Level           : {self.level}")
        print(f"   Experience      : {self.experience}/{self.experience_to_next_level}")
        print(f"   Health          : {self.current_health}/{self.health_max} ({self.health_max_base} + {self.health_max_item})")
        print(f"   Attack Power    : {self.attack_power} ({self.attack_power_base} + {self.attack_power_item})")
        print(f"   Block Strength  : {self.block_strength}")
        print(f"   Heal Amount     : {self.heal_amount}, {self.heal_cooldown}")
        print(f"   Heavy Attack    : {self.heavy_attack_mod}, {self.heavy_attack_cooldown}")
        print(f"   Gold            : {self.currency_gold}")
        print(f"   Inventory       : {len(self.inventory.items)}/{self.inventory.capacity}")

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            print(f"\n{C.cyan(self.name)} gain {C.magenta(amount)} {C.magenta('EXP')} and leveled up to level {self.level}!\nEXP need to next level: {self.experience}/{self.experience_to_next_level}")
        else:
            print(f"\n{C.cyan(self.name)} gain {C.magenta(amount)} {C.magenta('EXP')}!\nEXP need to next level: {self.experience}/{self.experience_to_next_level}")

    # LEVEL UP Constants
    def update_total_stats(self):
        self.attack_power = self.attack_power_base + self.attack_power_item
        self.health_max = self.health_max_base + self.health_max_item

    def increase_max_health(self):
        base_health_increase = 5
        health_increase = round(max((2 * self.level) + (self.level * 0.5) - 3, 0))
        self.health_max_base += health_increase
        self.current_health += health_increase

    def increase_attack_power(self):
        base_attack_increase = 1
        attack_increase = round(max(base_attack_increase + (self.level * 0.5 ) - 2, 1))
        self.attack_power_base += attack_increase

    def level_up(self):
        # Level and Experiences
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level += round(31 * self.level + (0.9 * max(1, (self.level - 1))))
        # Health and Power
        self.increase_max_health()
        self.increase_attack_power()
        self.update_total_stats()
        # Level-relative upgrade
        self.heal_amount = self.level * 0.025
        self.block_strength = round(self.level * 7.5 + self.health_max_item)
        self.heavy_attack_mod = roundF(min(1.0 + (0.01 * self.level), 2.0))
        # Every 12 level reduce heavy attack cooldown by 1 until it becomes 3
        if self.level % 31 == 0 and self.heavy_attack_cooldown_duration > 3:
            self.heavy_attack_cooldown_duration -= 1

    # INVENTORY
    def gain_worldItem(self, modifier, enemy_level):
        chance = random.random()
        if chance < modifier[2]:
            rarity = "c"
        elif chance < modifier[1]:
            rarity = "b"
        elif chance < modifier[0]:
            rarity = "a"
        else:
            return None

        if rarity is not None:
            item_library = WorldItems(enemy_level)
            items_to_drop = [getattr(item_library, item_name) for item_name in vars(item_library) if not item_name.startswith('__')]
            items_to_drop = [item for item in items_to_drop if item.rarity == rarity]

            # print(items_to_drop)
            item_drop = random.choice(items_to_drop)
            if isinstance(item_drop, Weapon):
                item_drop.damage += random.randint(-1 * round((item_drop.level * 0.25)), 1 * round((item_drop.level * 0.25)))
            elif isinstance(item_drop, Armor):
                item_drop.defense += random.randint(-1 * round((item_drop.level * 0.2)), 1 * round((item_drop.level * 0.2)))
            print(f"Get Item: {item_drop.name}")
            self.inventory.add_item(item_drop)

    def equip_item(self, item):
        if isinstance(item, Weapon):
            if self.equipped_items["weapon"] is not None:
                self.unequip_item(self.equipped_items["weapon"])
            self.equipped_items["weapon"] = item
            self.attack_power_item = item.damage
            self.update_total_stats()
            item.equipped = True
            # print((f"   {C.green("Equipped")} {item.name}. Attack power increased by {C.green(item.damage)}."))
        elif isinstance(item, Armor):
            if self.equipped_items["armor"] is not None:
                self.unequip_item(self.equipped_items["armor"])
            self.equipped_items["armor"] = item
            self.health_max_item = item.defense
            self.update_total_stats()
            item.equipped = True
            # print((f"   {C.green("Equipped")} {item.name}. Max health increased by {C.green(item.defense)}."))

    def unequip_item(self, item):
        if isinstance(item, Weapon):
            if self.equipped_items["weapon"] == item:
                self.attack_power_item -= item.damage
                self.equipped_items["weapon"] = None
                self.update_total_stats()
                item.equipped = False
                # print((f"   {C.yellow("Unequipped")} {item.name}. Attack power decreased by {C.red(item.damage)}."))
        elif isinstance(item, Armor):
            if self.equipped_items["armor"] == item:
                self.health_max_item -= item.defense
                self.equipped_items["armor"] = None
                self.update_total_stats()
                item.equipped = False
                # print((f"   {C.yellow("Unequipped")} {item.name}. Max health decreased by {C.red(item.defense)}."))

    def display_inventory(self, welcome):
        def display():
            clears()
            print(f"INVENTORY SCREEN\n")

            self.statf()
            print("")

            print("   ~ Equipped Items:")
            print(f"   Armor   : {C.cyan(self.equipped_items['armor'].name) if self.equipped_items['armor'] is not None else C.yellow('No armor wore.')}")
            print(f"   Weapon  : {C.cyan(self.equipped_items['weapon'].name) if self.equipped_items['weapon'] is not None else C.yellow('No weapon equipped.')}")

            print(f"\n   ~ Inventory ({len(self.inventory.items)}/{self.inventory.capacity}) :")
            if not self.inventory.items:
                print(C.yellow("\n   Your inventory is empty"))
            else:
                def elabel(index):
                    equipped_label = C.green("(equipped) ") if self.inventory.items[index].equipped == True else ""
                    return equipped_label
                def slabel(index):
                    if hasattr(self.inventory.items[index], 'damage'):
                        stat_label = self.inventory.items[index].damage
                    elif hasattr(self.inventory.items[index], 'defense'):
                        stat_label = self.inventory.items[index].defense
                    else:
                        stat_label = ""
                    return stat_label
                for i, item in enumerate(self.inventory.items, start=0):
                    print(f"   [{i + 1}] {C.cyan(item.name)} {C.yellow(item.level)} ({C.red(slabel(i))})\n        └ {elabel(i)}{item.description}")

                print(f"\n   {C.red('[')}d - Drop Item{C.red(']')} {C.green('[')}e/u - Equip, Unequip/Use Item{C.green(']')} {C.yellow('[')}q - Quit Inventory{C.yellow(']')}")
                print("   Select an item and what action to perform: ")

        display()
        while True:
            selection_action = input("\ni> ").strip().lower()
            print("")
            if selection_action == "q" or selection_action == "quit" or selection_action == "exit":
                clears()
                print("MAIN VILLAGE")
                break

            try:
                item_indices, action = selection_action.split(";")
                item_indices.strip()
                action.strip()
                item_indices = item_indices.replace("[", "").replace("]", "").split(",")
                item_indices = [int(index.strip()) for index in item_indices]
                item_indices.sort(reverse=True)

                invalid_indices = [index for index in item_indices if index < 1 or index > len(self.inventory.items)]

                if invalid_indices:
                    print(C.yellow("Invalid item indexes. Please choose again."))
                    continue

                # if not isinstance(item_index, list):
                #     item_index = int(item_index) - 1
                #     if (item_index) < 0 or item_index >= len(self.inventory.items):
                #         print(C.yellow("   Invalid item index. Please choose again."))
                #         continue
                # elif isinstance(item_index, list):
                #     items_index = []
                #     for index in item_index:
                #         items_index.append(index - 1)
                #     for index in items_index:
                #         if index < 0 or index >= len(self.inventory.items):
                #             print(C.yellow("   Invalid item indexes. Please choose again."))

            except ValueError:
                print(C.yellow(f"   Invalid input format. Please enter the prompt using the proper format (e.g.: {C.green('1, 2;d')}{C.yellow(')!')}"))
                continue

            absolute_index = []
            for index in item_indices:
                absolute_index.append(index - 1)

            if action == "d":
                for index in absolute_index:
                    self.inventory.remove_item(self.inventory.items[index])
                display()
            elif action == "e" or action == "u":
                if len(absolute_index) == 1:
                    if self.inventory.items[absolute_index[0]].equipped:
                        self.unequip_item(self.inventory.items[absolute_index[0]])
                        display()
                    else:
                        self.equip_item(self.inventory.items[absolute_index[0]])
                        display()
                    continue
                elif len(item_indices) > 1:
                    print("Cannot equip more than one item at a time. Please equip item one by one!")
            else:
                print(C.yellow("\n   Invalid action, please choose again."))

    # Combat Abilities
    def attack(self, enemy):
        damage = self.attack_power
        enemy.take_damage(damage)
        print(f"{C.cyan(self.name)} inflicting {C.red(damage)} {C.red('damage')}!")

    def heavy_attack(self, enemy):
        if self.heavy_attack_cooldown == 0:
            damage = round(self.attack_power * self.heavy_attack_mod)
            enemy.take_damage(damage)
            print(f"{C.cyan(self.name)} performs a heavy attack, dealing {C.red(damage)} {C.red('damage')}!")
            self.heavy_attack_cooldown = self.heavy_attack_cooldown_duration
        else:
            print(C.yellow("   Heavy attack is on cooldown."))

    def take_damage(self, damage):
        if self.is_blocking:
            blocked_damage = max(0, damage - self.block_strength)
            self.current_health -= max(0, blocked_damage)
            print(f"{C.cyan(self.name)} blocks the enemy's attack and takes {C.red(blocked_damage)} {C.red('damage')}.")
        else:
            self.current_health -= max(0, damage)
            print(f"{C.cyan(self.name)} take {C.red(damage)} {C.red('damage')}!")

        # if self.current_health <= 0:
        #    print(C.red("\nYou died!"))

    def block_attack(self, damage):
        self.is_blocking = True

    def heal(self):
        if self.heal_cooldown == 0:
            self.current_health = min(self.health_max, self.current_health + (self.health_max * max(1, self.heal_amount)))
            print(f"{C.cyan(self.name)} heals for {self.heal_amount} health!")
            self.heal_cooldown = self.heal_cooldown_duration
        else:
            print(C.yellow("   Healing ability is on cooldown."))

    # Currencies
    def collect_gold(self, object, modifier_gold_chance, modifier_gold_amount):
        if random.random() < modifier_gold_chance:
            if random.random() > 0.5:
                modifier_evener = random.randint(1, 3)
            else:
                modifier_evener = (- random.randint(1, 3))
            amount_gold = (random.randint(10, 20) * modifier_gold_amount) + modifier_evener
            self.currency_gold += amount_gold
            print(f"\n{self.name} collected {C.yellow(amount_gold)} {C.yellow('Gold')} from {object}!")

    # Misc
    def reduce_cooldown(self):
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        if self.heavy_attack_cooldown > 0:
            self.heavy_attack_cooldown -= 1

    def rest(self, amount):
        if self.current_health < self.health_max:
            before = round(self.current_health)
            self.current_health = min(self.health_max, self.current_health + amount)
            after = round(self.current_health)
            amount_healed = after - before
            self.reduce_cooldown()
            print(f"{C.cyan(self.name)} rests and restores {amount_healed} health. Current health: {self.current_health}/{self.health_max}")
        else:
            print(C.yellow("   Your health is already full!"))
