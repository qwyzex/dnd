import random
from utils import roundF, C

class Player:
    def __init__(self, name, max_health, attack_power):
        self.name = name
        # Basic Stat
        self.max_health = max_health
        self.current_health = max_health
        self.attack_power = attack_power
        # Level and Experience
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 70 + (self.level * 30)
        # Attack Blocking
        self.block_strength = round(4 + (self.level * 0.5))  # Amount of damage reduced when blocking
        self.is_blocking = False
        # Healing Potion
        self.heal_amount = round(12 + (self.level * 1.2))  # Amount of health restored when healing
        self.heal_cooldown_duration = 3  # Cooldown period for healing ability (in turns)
        self.heal_cooldown = 0  # Turns remaining until healing ability is available again
        # Heavy Attack
        self.heavy_attack_mod = roundF(min(1.1 * 1.0 + (0.1 * self.level), 2.0))  #Heavy Attack Increase Modifier
        self.heavy_attack_cooldown_duration = 5  # Cooldown period for heavy attack ability (in turns)
        self.heavy_attack_cooldown = 0  # Turns remaining until heavy attack ability is available again
        # Currencies
        self.currency_gold = 0
        # DUNGEONS
        self.current_room = 1

    # Player main functions
    def stat(self):
        print(f"Name            : {self.name}")
        print(f"Level           : {self.level}")
        print(f"Experience      : {self.experience}/{self.experience_to_next_level}")
        print(f"Health          : {self.current_health}/{self.max_health}")
        print(f"Attack Power    : {self.attack_power}")
        print(f"Gold            : {self.currency_gold}")

    def statf(self):
        print(f"Name            : {self.name}")
        print(f"Level           : {self.level}")
        print(f"Experience      : {self.experience}/{self.experience_to_next_level}")
        print(f"Health          : {self.current_health}/{self.max_health}")
        print(f"Attack Power    : {self.attack_power}")
        print(f"Block Strength  : {self.block_strength}")
        print(f"Heal Amount     : {self.heal_amount}, {self.heal_cooldown}")
        print(f"Heavy Attack    : {self.heavy_attack_mod}, {self.heavy_attack_cooldown}")
        print(f"Gold            : {self.currency_gold}")

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            print(f"\n{C.cyan(self.name)} gain {C.magenta(amount)} {C.magenta('EXP')} and leveled up to level {self.level}!\nEXP need to next level: {self.experience}/{self.experience_to_next_level}")
        else:
            print(f"\n{C.cyan(self.name)} gain {C.magenta(amount)} {C.magenta('EXP')}!\nEXP need to next level: {self.experience}/{self.experience_to_next_level}")

    # LEVEL UP Constants
    def increase_max_health(self):
        base_health_increase = 5
        if self.level % 2 == 0:
            health_increase = max(base_health_increase + (self.level // 2) - 2, 0)
        else:
            health_increase = max(base_health_increase + ((self.level - 1) // 2) - 2, 0)
        self.max_health += health_increase
        self.current_health += health_increase

    def increase_attack_power(self):
        base_attack_increase = 3
        if self.level % 2 == 0:
            attack_increase = max(base_attack_increase + (self.level // 2) - 2, 1)
        else:
            attack_increase = max(base_attack_increase + ((self.level - 1) // 2) - 2, 1)
        self.attack_power += attack_increase

    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level += 38 + round(self.level * 0.6)
        self.increase_max_health()
        self.increase_attack_power()
        if self.level % 10 == 0 and self.heavy_attack_cooldown_duration > 3:
            self.heavy_attack_cooldown_duration -= 1

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
            self.current_health = min(self.max_health, self.current_health + self.heal_amount)
            print(f"{C.cyan(self.name)} heals for {self.heal_amount} health!")
            self.heal_cooldown = self.heal_cooldown_duration
        else:
            print(C.yellow("   Healing ability is on cooldown."))

    # Currencies
    def collect_gold(self, object, modifier_gold_chance, modifier_gold_amount):
        if random.random() < modifier_gold_chance:
            amount_gold = random.randint(10, 20) * modifier_gold_amount
            self.currency_gold += amount_gold
            print(f"\n{self.name} collected {C.yellow(amount_gold)} {C.yellow('Gold')} from {object}!")

    # Misc
    def reduce_cooldown(self):
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        if self.heavy_attack_cooldown > 0:
            self.heavy_attack_cooldown -= 1

    def rest(self, amount):
        if self.current_health < self.max_health:
            before = round(self.current_health)
            self.current_health = min(self.max_health, self.current_health + amount)
            after = round(self.current_health)
            amount_healed = after - before
            print(f"{C.cyan(self.name)} rests and restores {amount_healed} health. Current health: {self.current_health}/{self.max_health}")
        else:
            print("Your health is already full!")
