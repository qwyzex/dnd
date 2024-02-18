import random
from inventory import Item, Weapon, Armor

# ITEMS
# World items are items that are found in the wilds without buying, but can still be selled for gold
class WorldItems:
    def __init__(self, level):
        # WEAPON
        self.a_stone_sword = Weapon("Stone Sword", level, "Pretty sharp short stone sword", 5, "a", False)
        self.a_metal_bar = Weapon("Metal Bar", level, "It's a bar, metal one.", 6, "a", False)
        self.b_steel_sword = Weapon("Steel Sword", level, "Fine steel sword", 12, "b", False)
        self.c_harakis_katana = Weapon("Haraki's Katana", level, "Lightweight blade made by the greatest smith in Asia", 25, "c", False)
        # ARMOR
        self.a_rugged_robe = Armor("Rugged Robe", level, "This is not an armor, but still usable...", 2, "a", False)
        self.a_cardboard_clothes = Armor("Cardboard Clothes", level, "Thin cardboard armor made by cosplayers", 3, "a", False)
        self.b_tight_robe = Armor("Tight Robe", level, "A good clothes is a good clothes", 7, "b", False)
        self.c_knights_chainmail = Armor("Knight's Chainmail", level, "Strong chainmail armor used by the Knights", 19, "c", False)

# EXP gain library for various event
class XP:
    class ev:
        treasure = 15

# ENEMY
# ENEMY CLASS-A
# CLASS-A enemies are weak and found more often in the lower levels of the dungeon
class EnemyA:
    def __init__(self, name, health, attack_power, exp_gain, player, modifier, item_modifier):
        self.name = name
        self.level = 1
        self.health = health
        self.attack_power = attack_power
        self.exp_gain = exp_gain
        self.player = player
        # Modifier of each unique enemy in combat
        self.fleeing_chance = modifier[0]
        self.modifier_gold_chance = modifier[1]
        self.modifier_gold_amount = modifier[2]
        # Item rarity modifier dropped by enemy
        self.modifier_item_rarity = [item_modifier[0], item_modifier[1], item_modifier[2]]
        self.modifier_item_rarity_A = self.modifier_item_rarity[0]
        self.modifier_item_rarity_B = self.modifier_item_rarity[1]
        self.modifier_item_rarity_C = self.modifier_item_rarity[2]

    def adapt(self):
        self.health = round(max(self.health * (self.level * 0.9), self.health))
        self.attack_power = round(max(self.attack_power * (self.level * 0.9), self.attack_power))
        # self.exp_gain = round(max(self.exp_gain * (self.level * 0.6), self.exp_gain))
        self.exp_gain = round(self.exp_gain * self.level)
        # Modifier of each unique enemy in combat
        self.modifier_gold_chance = self.modifier_gold_chance
        self.modifier_gold_amount = round(max(self.modifier_gold_amount * (self.level * 0.006), self.modifier_gold_amount))
        # Item rarity modifier dropped by enemy
        # self.modifier_item_rarity_A = min(self.modifier_item_rarity[0] * (self.level * 0.01), 2)
        # self.modifier_item_rarity_B = min(self.modifier_item_rarity[1] * (self.level * 0.01), 2)
        # self.modifier_item_rarity_C = min(self.modifier_item_rarity[2] * (self.level * 0.01), 2)

    def attack(self):
        min_damage = round(max(1, self.attack_power - 2))
        max_damage = round(self.attack_power + 2)
        damage = random.randint(min_damage, max_damage)
        return damage
    def attack_player(self, player):
        damage = self.attack()
        self.player.take_damage(damage)
    def take_damage(self, damage):
        self.health -= damage

class EnemyB:
    def __init__(self, name, health, attack_power, exp_gain, player, modifier, item_modifier):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.exp_gain = exp_gain
        self.player = player
        # Modifier of each unique enemy in combat
        self.fleeing_chance = modifier[0]
        self.modifier_gold_chance = modifier[1]
        self.modifier_gold_amount = modifier[2]
        # Item rarity modifier dropped by enemy
        self.modifier_item_rarity = [item_modifier[0], item_modifier[1], item_modifier[2]]
        self.modifier_item_rarity_A = self.modifier_item_rarity[0]
        self.modifier_item_rarity_B = self.modifier_item_rarity[1]
        self.modifier_item_rarity_C = self.modifier_item_rarity[2]

        def attack(self):
            min_damage = max(1, self.attack_power - 2)
            max_damage = self.attack_power + 2
            damage = random.randint(min_damage, max_damage)
            return damage
        def attack_player(self, player):
            damage = self.attack()
            self.player.take_damage(damage)
        def take_damage(self, damage):
            self.health -= damage

# Enemy instantiation data collection
class BestiaryA:
    def __init__(self, player):
        self.player = player # pass the player param
        self.goblin = EnemyA("Goblin", 20, 6, 13, self.player, [1, 0.5, 1], [0.18, 0, 0])
        self.wolf = EnemyA("Wild Wolf", 18, 8, 17, self.player, [0.95, 0, 0], [0.1, 0, 0])
        self.skeleton = EnemyA("Skeleton", 14, 9, 14, self.player, [1, 0.3, 1], [0.18, 0, 0])

class BestiaryB:
    def __init__(self, player):
        self.player = player
        self.mimic = EnemyB("Mimic", 34, 11, 29, self.player, [0.96, 2, 1.2], [0.22, 0.06, 0.001])
