# Thiago Schuck 23 January 2023
# This script is a battleship game. The user can play against an AI with multiple difficulty settings or against another player.

# Main function
def main():
    
    # Import modules
    global BattleshipClasses
    import BattleshipClasses

    # Declare fields
    playerList = []

    # Ask if user wants to play against AI or another player
    playAI = True if input("Do you want to play against AI? (y/n): ") == "y" else False
    numPlayers = 1 if playAI else 2     # Save the number of players

    # Create the player class objects
    for i in range(numPlayers):     # Loop through the number of players
        playerList.append(create_player(numPlayers))       # Call the function to create the player class

    if numPlayers == 1:      # If the user is playing against AI
        # Ask for difficulty
        difficulty = int(input("What difficulty do you want to play on?\n"
                               "1. Easy\n"
                               "2. Medium\n"
                               "3. Hard\n"))
        # Create the AI class object
        AI = BattleshipClasses.AI(difficulty)      # Call the function to create the AI class
        playerList.append(AI)      # Add the AI to the player list

    # Create the board
    create_board(playerList)      # Call the function to create the board GUI


# Function to create player class with number of players as parameter
def create_player(numPlayers):
        
    # Ask for player name
    name = input("What is your name?")

    # Create the player object
    player = BattleshipClasses.Player(name)

    # Return player reference
    return player


# Function to create the board GUI
def create_board(playerList):

    # Import modules
    import PySimpleGUI as sg

    # Declare fields
    boardSize = 10      # Board size
    layout = []         # Layout of GUI list
    length = 2          # Length of the buttons
    width = 1           # Width of the buttons

    # Create the board layout
    leftBoard = [(sg.Button(" ", size=(length, width), pad=(0,0), key=(i,j)) for j in range(boardSize)) for i in range(boardSize)]
    leftBoardName = [(sg.Text(playerList[0].name, size = (10,1), pad = (0,0), justification="center"))]

    rightBoard = [(sg.Button(" ", size=(length, width), pad=(0,0), key=(i,j)) for j in range(boardSize)) for i in range(boardSize)]
    rightBoardName = [(sg.Text(playerList[1].name, size = (10,1), pad = (0,0), justification = "center"))]

    layout = [
        [sg.Column([leftBoardName]), sg.VerticalSeparator(pad=(boardSize * 13.6 + 100, 0)), sg.Column([rightBoardName])],
        [sg.Column(leftBoard), sg.VerticalSeparator(pad=(100, 0)),  sg.Column(rightBoard)]
        ]

    # Create board
    window = sg.Window("Battleship", layout)

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if isinstance(event, tuple) and len(event) == 2:
            print(event)
            print(event[1])

# Start the game
if __name__ == "__main__":
    main()