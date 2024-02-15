# Thiago Schcuk 23 January 2024
# This script is the class file for the battleship game. It contains the classes for the AI and the player.

# Player class
class Player:

    # Declare class attributes
    ships = {}    # {Ship:position}

    # Player object constructor with name and ships position
    def __init__(self, name):
        self.name = name

    # Function to choose ship positions
    def choose_ships(self):
        pass

    # Function to choose a position to attack
    def choose_position(self):
        pass

# AI class
class AI(Player):

    # Declare class attributes
    name = "AI"
    ships = {}    # {Ship:position}

    # AI object constructor with difficulty and ships position
    def __init__(self, difficulty):
        self.difficulty = difficulty    # Save the difficulty

        super().__init__(self.name)   # Call the parent class constructor

    # Function to choose ship positions based on diffiuclty
    def choose_ships(self):
        
        # Declare ships

        # Get difficulty
        if self.difficulty == 1:
            pass
        
        elif self.difficulty == 2:
            pass

        elif self.difficulty == 3:
            pass

        else:
            print("Invalid difficulty")

    # Function to choose a random position to attack
    def choose_position(self):
        pass