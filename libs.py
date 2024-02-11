import random

class XP:
    class ev:
        treasure = 15

# Enemy Class-A Blueprint
class EnemyA:
    def __init__(self, name, health, attack_power, exp_gain, player, modifier):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.exp_gain = exp_gain
        self.player = player
        # Modifier of each unique enemy in combat
        self.fleeing_chance = modifier[0]
        self.modifier_gold_chance = modifier[1]
        self.modifier_gold_amount = modifier[2]

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

class BestiaryA:
    def __init__(self, player):
        self.player = player # pass the player param
        self.goblin = EnemyA("Goblin", 20, 6, 25, self.player, [1, 0.5, 1])
        self.wolf = EnemyA("Wild Wolf", 18, 8, 30, self.player, [0.95, 0, 0])
