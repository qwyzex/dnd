import random
from player import Player

class Enemy:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self):
        return random.randint(1, self.attack_power)
    def attack_player(self, player):
        damage = self.attack()
        player.take_damage(damage)
    def take_damage(self, damage):
        self.health -= damage
    

def battle(player):
    enemy = Enemy("Goblin", 50, 10)  # Example enemy stats
    print(f"A wild {enemy.name} appears!")
    print(f"Player Health: {player.current_health}")
    print(f"Enemy Health: {enemy.health}")

    while player.current_health > 0 and enemy.health > 0:
        action = input("Choose your action: [attack], [hattack], [heal], [block], or [flee]? ").lower()
        if action == "attack":
            player.attack(enemy)
        elif action == "hattack":
            player.heavy_attack(enemy)
        elif action == "heal":
            player.heal()
        elif action == "block":
            player.block_attack(enemy)
        elif action == "flee":
            print("You fled from the battle!")
            return False
        else:
            print("Invalid action. Please choose from the available options.")

        if enemy.health <= 0:
            print(f"You defeated the {enemy.name}!")
            return True

        enemy.attack_player(player)
        if player.current_health <= 0:
            print("You have been defeated!")
            return False
