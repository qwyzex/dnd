import random
from utils import C
from libs import XP, BestiaryA
from player import Player

def select_enemy(player):
    bestiary = BestiaryA(player)

    enemies = [getattr(bestiary, enemy_name) for enemy_name in vars(bestiary) if not enemy_name.startswith('__')]
    enemies = [enemy for enemy in enemies if enemy != player]

    enemy = random.choice(enemies)
    return enemy

def battle(player):
    enemy = select_enemy(player)

    def battle_status():
        print(f"\nPlayer Health: {C.green(player.current_health)}")
        print(f"Enemy Health: {C.red(enemy.health)}")

    print(f"A {C.red(enemy.name)} appears!")
    battle_status()

    def proceed():
        if enemy.health <= 0:
            print(f"{C.green('You defeated the')} {C.green(enemy.name)}")
            player.collect_gold(enemy.name, enemy.modifier_gold_chance, enemy.modifier_gold_amount)
            player.gain_experience(enemy.exp_gain)
            player.reduce_cooldown()
            player.current_room += 1
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
            print(f"\n{C.red('You have been defeated by a')} {C.red(enemy.name)}")
            return False

    while player.current_health > 0 and enemy.health > 0:
        action = input(f"\nChoose your action: [{C.red('attack')}], [{C.red('hattack')} {player.heavy_attack_cooldown}], [{C.green('heal')} {player.heal_cooldown}], [{C.blue('block')}], or [{C.yellow('flee')}]? ").strip().lower()
        print("")
        if action == "attack" or action == "a":
            player.attack(enemy)
            if proceed():
                break
        elif action == "hattack" or action == "ha":
            if not player.heavy_attack_cooldown > 0:
                player.heavy_attack(enemy)
                player.heavy_attack_cooldown += 1
                if proceed():
                    break
            else:
                player.heavy_attack(enemy)
        elif action == "heal" or action == "he":
            if not player.heal_cooldown > 0:
                player.heal()
                player.heal_cooldown += 1
                if proceed():
                    break
            else:
                player.heal()
        elif action == "block" or action == "bl":
            player.block_attack(enemy)
            if proceed():
                break
        elif action == "flee" or action == "fl":
            if (random.random() * enemy.fleeing_chance) > 0.5:
                print(f"   You {C.yellow('fled')} from the battle!")
                player.current_room += 1
                if player.is_blocking:
                    player.is_blocking = False
                return False
            else:
                print(C.red("   You tried to flee the battle, but FAILED!\n"))
                if proceed():
                    break
        else:
            print(C.yellow("   ! Invalid action. Please choose from the available options."))
