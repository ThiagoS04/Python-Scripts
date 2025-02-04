# Thiago Schuck 23 January 2023
# This script is a battleship game. The user can play against an AI with multiple difficulty settings or against another player.

# Import modules
global BattleshipClasses
import BattleshipClasses
import os

# Main function
def main():

    # Declare fields
    boardSize = 10
    playerList = []         # List to iterate over to determine which player's turn
    playerWon = False       # Boolean to determine if the game is over

    # Ask if user wants to play against AI or another player
    playAI = True if input("Do you want to play against AI? (y/n):\t") == "y" else False
    numPlayers = 1 if playAI else 2     # Save the number of players

    # Call method to setup game
    playerList = setupGame(numPlayers, playerList)

    # Loop until the game is over
    while not playerWon:
            
        # Loop through the player list
        for i in range(playerList):

            # Create player references
            attackPlayer  = playerList[i]
            defendPlayer = playerList[(i + 1) % numPlayers]         # i = 1 | 2, i=2 + 1 % numPlayers = 1

            # Call method to get player's attack
            attack(attackPlayer, defendPlayer)            


""" Function to setup the game

    numPlayers: int - the number of players
    playerList: list - the list of player objects

"""
def setupGame(numPlayers: int, playerList: list) -> list:
    
    # Loop through the number of players
    for i in range(numPlayers):

        # Call method to create the player class objects
        playerList.append(createPlayerObject(i + 1))

        # Call method to choose ship positions
        playerList[i].placeShips()

        # Clear terminal so player cannot see other player's ship locations
        os.system('cls')

    if numPlayers == 1:      # If the user is playing against AI

        # Ask for difficulty
        difficulty = input("What difficulty do you want to play on?\n"
                               "\t\tEasy\n"
                               "\t\tMedium\n"
                               "\t\tHard\n")
        
        # Create the AI class object
        AI = BattleshipClasses.AI(difficulty)      # Call the function to create the AI class
        playerList.append(AI)      # Add the AI to the player list

    # Return list of complete player objects
    return playerList


""" Function to get create player object"""
def createPlayerObject(playerNum: int) -> BattleshipClasses.Player:

    # Get player name and initialize object
    name = input(f"Enter player number {playerNum}'s name:\t")     # Print the player number

    # Return the player object
    return BattleshipClasses.Player(name)


""" Function to get player's attack

    attackPlayer: Player - the player object that is attacking
    defendPlayer: Player - the player object that is being attacked

"""
def attack(attackPlayer: BattleshipClasses.Player, defendPlayer: BattleshipClasses.Player) -> None:

    # Declare fields
    hit = False
    newAttack = False
    attackType: int | None = None           # 0 = miss, 1 = already attacked, 2 = hit

    # Loop until the player enters a valid attack
    while not newAttack:

        # Get attack coords
        attackCoords = attackPlayer.getAttack()

        # Get validity of attack
        attackType = defendPlayer.checkAttack(attackCoords)

        # Check attack type
        if attackType == (0 | 2):         # If the attack was a miss or a hit

            # Set newAttack to True
            newAttack = True

        else:       # If the attack coordinate was already attacked

            print("You have already attacked this location. Please try again.")

    # If the attack hit update boards
    if attackType == 2:
        
        hit = True

    # Update boards
    attackPlayer.updateAttackBoard(attackCoords, hit)


# Start the game
if __name__ == "__main__":
    main()