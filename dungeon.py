import random
from utils import C, clears
from libs import XP
from player import Player
from combat import battle

class Dungeon:
    def __init__(self, length, player):
        self.length = length
        self.rooms = ["enemy" if random.random() < 0.95 else "treasure" for _ in range(length)]
        self.player = player # Store the player object

    # Explore the rooms in the dungeon
    def explore_room(self):
        clears()
        room_type = self.rooms[self.player.current_room - 1]
        print(f"{C.blue('ROOM')} {self.player.current_room}")
        if self.player.current_room > 0 and self.player.current_room % 5 == 0:  # Camp every 5th room
            print("You found a camp! You can rest here.")
            self.player.rest(20) # Automatically rest and restore health
        elif room_type == "enemy":
            print("Enemy encounter! Get ready to fight!")
            if not battle(self.player):
                return False # Player is defeated
        elif room_type == "treasure":
            print(f"You found a {C.yellow('treasure')} chest!")
            self.player.collect_gold("Treasure Chest", 1, 3)
            self.player.gain_experience(XP.ev.treasure)

        # Increment current room
        self.player.current_room += 1

        return True  # Continue exploration if the player is still alive or found a treasure
