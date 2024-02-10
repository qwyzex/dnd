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
        self.experience_to_next_level = 100
        # Attack Blocking
        self.block_strength = 5  # Amount of damage reduced when blocking
        # Healing Potion
        self.heal_amount = 15  # Amount of health restored when healing
        self.heal_cooldown_duration = 3  # Cooldown period for healing ability (in turns)
        self.heal_cooldown = 0  # Turns remaining until healing ability is available again
        # Heavy Attack
        self.heavy_attack_mod = min(1.1 * 1.0 + (0.1 * self.level), 2.0)  #Heavy Attack Increase Modifier
        self.heavy_attack_cooldown_duration = 5  # Cooldown period for heavy attack ability (in turns)
        self.heavy_attack_cooldown = 0  # Turns remaining until heavy attack ability is available again

    # Player main functions
    def stat(self):
        print(f"Name            : {self.name}")
        print(f"Level           : {self.level}")
        print(f"Health          : {self.current_health}/{self.max_health}")
        print(f"Attack Power    : {self.attack_power}")
        print(f"Experience      : {self.experience}/{self.experience_to_next_level}")

    def statf(self):
        print(f"Name            : {self.name}")
        print(f"Level           : {self.level}")
        print(f"Experience      : {self.experience}/{self.experience_to_next_level}")
        print(f"Health          : {self.current_health}/{self.max_health}")
        print(f"Attack Power    : {self.attack_power}")
        print(f"Block Strength  : {self.block_strength}")
        print(f"Heal Amount     : {self.heal_amount}, {self.heal_cooldown}")
        print(f"Heavy Attack    : {self.heavy_attack_mod}, {self.heavy_attack_cooldown}")

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    def increase_max_health(self):
        base_health_increase = 7
        if self.level % 2 == 0:
            health_increase = max(base_health_increase + (self.level // 2) - 2, 0)
        else:
            health_increase = max(base_health_increase + ((self.level - 1) // 2) - 2, 0)

        self.max_health += health_increase
        self.current_health += health_increase

    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level += 30
        self.increase_max_health()
        self.attack_power += 5
        self.block_strength += 2
        self.heal_amount += 3
        if self.level % 7 == 0 and self.heavy_attack_cooldown_duration > 3:
            self.heavy_attack_cooldown_duration -= 1
        print(f"{self.name} leveled up to level {self.level}!")

    # Combat Abilities
    def attack(self, enemy):
        damage = self.attack_power
        enemy.take_damage(damage)

    def heavy_attack(self, enemy):
        if self.heavy_attack_cooldown == 0:
            damage = self.attack_power * self.heavy_attack_mod
            enemy.take_damage(damage)
            print(f"{self.name} performs a heavy attack, dealing {damage} damage!")
            self.heavy_attack_cooldown = self.heavy_attack_cooldown_duration
        else:
            print("Heavy attack is on cooldown.")

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} take {damage} damage!")

    def block_attack(self, damage):
        if damage > 0:
            blocked_damage = max(0, damage - self.block_strength)
            self.take_damage(blocked_damage)
            print(f"{self.name} blocks the enemy's attack and takes {blocked_damage} damage.")
        else:
            print(f"{self.name} braces for an attack, but the enemy does not attack.")

    def heal(self):
        if self.heal_cooldown == 0:
            self.current_health = min(self.max_health, self.current_health + self.heal_amount)
            print(f"{self.name} heals for {self.heal_amount} health!")
            self.heal_cooldown = self.heal_cooldown_duration
        else:
            print("Healing ability is on cooldown.")

    # Misc
    def reduce_cooldown(self):
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        if self.heavy_attack_cooldown > 0:
            self.heavy_attack_cooldown -= 1

    def rest(self, amount):
        if self.current_health < self.max_health:
            self.current_health = min(self.max_health, self.current_health + amount)
            print(f"{self.name} rests and restores {amount} health. Current health: {self.current_health}/{self.max_health}")
        else:
            print(f"Your health is already full!")
