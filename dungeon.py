import random
from player import Player
from combat import battle  # Import the battle function from combat.py

class Dungeon:
    def __init__(self, length, player):
        self.length = length
        self.rooms = ["enemy" if random.random() < 0.95 else "treasure" if random.random() < 0.05 else "camp" for _ in range(length)]
        self.player = player  # Store the player object

    def explore_room(self):
        room_type = self.rooms[self.player.current_room]
        if self.player.current_room % 5 == 0:  # Camp every 5th room
            print("You found a camp! You can rest here.")
            self.player.rest(20)  # Restore player health
        elif room_type == "enemy":
            print("Enemy encounter! Get ready to fight!")
            if not battle(self.player):  # Pass the player object to the battle function
                print("You were defeated! Game over.")
                return False  # End exploration if the player is defeated
        elif room_type == "treasure":
            print("You found a treasure chest!")
            # Implement treasure discovery logic here

        # Increment current room
        self.player.current_room += 1

        # Check if all rooms have been cleared
        if self.player.current_room < self.length:
            response = input("Do you want to continue exploring? (yes/no): ").lower()
            if response == "yes":
                self.explore_room()
            else:
                print("Exiting dungeon.")
        else:
            print("You've cleared all rooms in the dungeon. Exiting dungeon.")

        return True  # Continue exploration if the player is still alive or found a treasure
