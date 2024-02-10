import random
from utils import C
from player import Player

class Enemy:
    def __init__(self, name, health, attack_power, player):
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
    enemy = Enemy("Goblin", 20, 10, player)  # Example enemy stats

    def battle_status():
        print(f"Player Health: {C.green(player.current_health)}")
        print(f"Enemy Health: {C.red(enemy.health)}")

    print(f"A wild {C.red(enemy.name)} appears!\n")
    battle_status()

    def proceed():
        if enemy.health <= 0:
            print(f"{C.green('You defeated the')} {C.green(enemy.name)}")
            player.current_room += 1
            player.reduce_cooldown()
            if player.is_blocking:
                player.is_blocking = False
            return True

        enemy.attack_player(player)

        # Will Run Regardless
        player.reduce_cooldown()
        if player.is_blocking:
            player.is_blocking = False

        battle_status()

        if player.current_health <= 0:
            print(C.red("You have been defeated!"))
            return False

    while player.current_health > 0 and enemy.health > 0:
        action = input(f"\nChoose your action: [{C.red("attack")}], [{C.red("hattack")} {player.heavy_attack_cooldown}], [{C.green("heal")} {player.heal_cooldown}], [{C.blue("block")}], or [{C.yellow("flee")}]? ").lower()
        print("")
        if action == "attack":
            player.attack(enemy)
            if proceed():
                break
        elif action == "hattack":
            if not player.heavy_attack_cooldown > 0:
                player.heavy_attack(enemy)
                player.heavy_attack_cooldown += 1
                if proceed():
                    break
            else:
                player.heavy_attack(enemy)
        elif action == "heal":
            if not player.heal_cooldown > 0:
                player.heal()
                player.heal_cooldown += 1
                if proceed():
                    break
            else:
                player.heal()
        elif action == "block":
            player.block_attack(enemy)
            if proceed():
                break
        elif action == "flee":
            print(f"You {C.yellow('fled')} from the battle!")
            player.current_room += 1
            if player.is_blocking:
                player.is_blocking = False
            return False
        else:
            print(C.yellow("! Invalid action. Please choose from the available options."))
