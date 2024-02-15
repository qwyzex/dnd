import random
from inventory import Item, Weapon, Armor

# ITEMS
# World items are items that are found in the wilds without buying, but can still be selled for gold
class WorldItems:
    def __init__(self):
        # WEAPON
        self.a_stone_sword = Weapon("Stone Sword", "Pretty sharp short stone sword", 5, "a")
        self.a_metal_bar = Weapon("Metal Bar", "It's a bar, metal one.", 6, "a")
        self.b_steel_sword = Weapon("Steel Sword", "Fine steel sword", 12, "b")
        self.c_harakis_katana = Weapon("Haraki's Katana", "Lightweight blade made by the greatest smith in Asia", 25, "c")
        # ARMOR
        self.a_rugged_robe = Armor("Rugged Robe", "This is not an armor, but still usable...", 2, "a")
        self.a_cardboard_clothes = Armor("Cardboard Clothes", "Thin cardboard armor made by cosplayers", 3, "a")
        self.b_tight_robe = Armor("Tight Robe", "A good clothes is a good clothes", 7, "b")
        self.c_knights_chainmail = Armor("Knight's Chainmail", "Strong chainmail armor used by the Knights", 19, "c")

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
        self.goblin = EnemyA("Goblin", 20, 6, 13, self.player, [1, 0.5, 1], [0.8, 0, 0])
        self.wolf = EnemyA("Wild Wolf", 18, 8, 17, self.player, [0.95, 0, 0], [0.1, 0, 0])
        self.skeleton = EnemyA("Skeleton", 14, 9, 14, self.player, [1, 0.3, 1], [0.8, 0, 0])
