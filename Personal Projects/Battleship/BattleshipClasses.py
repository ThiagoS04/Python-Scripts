# Thiago Schcuk 23 January 2024
# This script is the class file for the battleship game. It contains the classes for the player, AI, and ships.

# Ship class
class Ship:

    # Declare fields
    size = 0                # Size of ship
    position = (-1, -1)     # Position of top of ship (row, col)
    orientation = ""        # Orientation of ship
    id: int                 # Ship id
    shipSegments = []       # List of ship segments
    sunk = False            # Whether ship is sunk or not

    # Constructor of ship object
    def __init__(self, size: int, orientation: str, position: tuple, id: int) -> None:
        self.size = size
        self.position = position
        self.orientation = orientation
        self.id = id

        # Create ship segments
        for i in range(size):

            # Create ship segment object
            segment = self.ShipSegment(position)

            # Store ship segment
            self.shipSegments.append(segment)

    # Class to hold whether ship segment is hit or not
    class ShipSegment:
        
        # Declare fields
        position = (-1, -1)     # Position of ship segment
        hit = False             # Whether ship segment is hit or not

        # Constructor of ship segment object
        def __init__(self, position: tuple) -> None:
            self.position = position

        # Function to set ship segment as hit
        def hit(self) -> None:
            self.hit = True

    # Function to determine if ship is sunk (All segments are hit)
    def isSunk(self) -> bool:

        # Loop through all ship segments
        for segment in self.shipSegments:

            # If any segment is not hit, return False
            if not segment.hit:
                return False

        # If all segments are hit, return True
        return True

    # Getter methods
    def getSize(self) -> int:
        return self.size
    
    def getPosition(self) -> list:
        return self.position
    
    def getOrientation(self) -> int:
        return self.orientation
    

# Player class
class Player:

    # Declare class attributes
    boardSize = 10
    numShips = 5
    ships = {}    # {Ship id # : Ship}
    columnLetters = [chr(65 + i) for i in range(boardSize)]    # List of column letters

    """ Player object constructor with name and ships position
    
    Sets name and creates board
    " - " is empty space and ship size is ship
    " X " is a hit, " O " is a miss
    
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.board = [[" - " for i in range(self.boardSize)] for i in range(self.boardSize)]            # Board to keep track of ships
        self.attackBoard = [[" - " for i in range(self.boardSize)] for i in range(self.boardSize)]      # Board to keep track of attacks


    # Function to choose ship positions
    def placeShips(self) -> None:

        # Declare fields
        allShips = [2, 3, 3, 4, 5]            # List of all ships
        availableShips = allShips[:]          # List of ships user hasn't placed yet

        # Notify which player is choosing ships
        print(f"Place your ships {self.name}")

        # Loop through for each ship
        for i in range(self.numShips):

            # Create ship verification flag
            verifiedShip = False

            # Loop through until ship is verified
            while not verifiedShip:

                # Call method to get desired ship
                shipSize = self.selectShip(availableShips)

                # Call method to get desired position
                print("Choose a position for your ship.")
                position = self.selectPosition()

                # Call method to get desired orientation
                orientation = self.selectOrientation()

                # Check if ship has room
                try:
                    
                    # Create hasSpace flag
                    hasSpace = False

                    # Call method to verify every ship square
                    hasSpace = self.checkSpace(shipSize, position, orientation)

                except ValueError as e:         # Catch if ship goes out of bounds or overlaps another ship

                    print(e)            # Print error

                if hasSpace:        # Proceed only if ship has space to be placed

                    # Confirm user wants to place ship
                    confirmation = input("Are you sure you want to place a ship of size"
                                        f"{shipSize} at position {position} with orientation {orientation}? (y/n)\t")
                    if confirmation.upper()[0] == "Y":
                        verifiedShip = True

            # Create ship id
            shipId = allShips.index(shipSize)
            if shipId == 1:         # Distinguish between the two 3 size ships
                shipId = 11 if shipId not in self.ships else 12     # If the first size 3 ship is already placed, set the id to 12

            # Create ship object
            ship = Ship(shipSize, orientation, position, shipId)

            # Add ship to dictionary
            self.ships[shipId] = ship

            # Remove ship from available ships
            availableShips.remove(shipSize)

            # Place ship on board
            self.placeShipOnBoard(ship)

            # Print board
            self.printBoard()
            

    """ Function to select ship

    @param availableShips: list of available ships
    @return shipSize: size of ship selected

    """
    def selectShip(self, availableShips: list) -> int:

        # Create invalid ship flag
        incorrectShip = True

        # Create verification loop
        while incorrectShip:

            # Get ship user wants to place
            shipSize = int(input(f"Which size ship would you like to place?\n"
                    f"The sizes available are {' '.join(map(str, availableShips))}\t"))
            
            # Note which ship was selected
            print("You chose the ship with a size of", shipSize)

            # Return if ship size is valid
            if self.verifyShipSize(shipSize) and shipSize in availableShips:
                return shipSize
            else:
                print("Invalid ship size. Please try again.")       # Catch invalid input
    

    """ Function to select position

    @return position: position of ship selected
    
    """
    def selectPosition(self) -> tuple:
        
        # Print board
        self.printBoard()

        # Create invalid position flag
        incorrectPosition = True

        # Create verification loop
        while incorrectPosition:

            # Ask user for position of ship
            col = input("Select column:\t").upper()
            row = int(input("Select row:\t"))

            # Return of position is valid
            if self.verifyPosition((col, row)):
                return (col, row)
            else:
                print("Invalid position. Please try again.")       # Catch invalid input
    

    """ Function to select orientation
    
    @return orientation: orientation of ship selected
    
    """
    def selectOrientation(self) -> int:
        
        # Create invalid direction flag
        incorrectDirection = True

        # Create verification loop
        while incorrectDirection:

            # Ask user for orientation of ship
            orientation = input("Do you want the ship to go up, down, left, or right?\t").lower()

            # Return of orientation orientation
            if self.verifyOrientation(orientation):
                return orientation
            else:
                print("Invalid direction. Please try again.")       # Catch invalid input


    """ Functions to verify input
    
    @param input: input to verify
    @return bool: if input is valid or not

    """
    def verifyShipSize(self, shipSize: int) -> bool:
        return shipSize in [2, 3, 3, 4, 5]
    
    def verifyPosition(self, position: tuple) -> bool:
        return position[0] in self.columnLetters and position[1] in range(self.boardSize + 1) and self.board[position[1] - 1][self.columnLetters.index(position[0])] == " - "
    
    def verifyOrientation(self, orientation: str) -> bool:
        return orientation in ["up", "down", "left", "right"]
    
    # Function to adjust position for 0 index and convert column letter to number
    def adjustPosition(self, position: tuple) -> tuple:

        # Declare fields
        col, row = position
        row -= 1                                    # Adjust for 0 index
        colIndex = self.columnLetters.index(col)         # Convert to number

        return (colIndex, row)
    

    # Function checks if all spaces the ship would occupy are empty
    def checkSpace(self, shipSize: int, position: tuple, orientation: str):

        # Declare fields
        col, row = self.adjustPosition(position)
        direction = self.getDirections().get(orientation)
        newRow, newCol = row, col         # Initialize new row and column

        # Check shipSize num spaces
        for i in range(shipSize):
            
            # Starting from position check every space going in orientation's direction
            if (newRow < 0 or newRow >= self.boardSize) or (newCol < 0 or newCol >= self.boardSize):
                
                raise ValueError("Ship cannot be placed out of bounds")
            
            elif (self.board[newRow][newCol]) != " - ":
                
                raise ValueError("Ship cannot be placed on top of another ship")
            
            # Update new row and column
            newRow += direction[0]
            newCol += direction[1]
            
        # If all spaces are empty return True
        return True
    

    """ Function to print board

    @param ship to place

    """
    def placeShipOnBoard(self, ship: Ship) -> None:

        # Declare fields
        print("Placing ship of size", ship.getSize(), "at position", ship.getPosition(), "with orientation", ship.getOrientation())
        col, row = self.adjustPosition(ship.getPosition())
        orientation = ship.getOrientation()
        size = ship.getSize()
        
        # Get row and column changes
        rowChange, colChange = self.getDirections().get(orientation)
        
        # Place ship on board
        for i in range(size):
            self.board[row + i * rowChange][col + i * colChange] = " " + str(size) + " "

    """ Function to print board with ships

        Grid is printed with " - " as empty space and ship size as ship    

    """
    def printBoard(self) -> None:
        
        # Print column letters
        print("\n\n\n")         # Add separation
        print("     ", end="")    # Add space for row numbers

        for i in range(self.boardSize):
            print(f"{self.columnLetters[i]:^6}", end="")

        for row in range(self.boardSize):
            
            print(f"\n{row + 1:^4}", end="")     # Print row number
            print (f"| {" | ".join(self.board[row])} |")   # Print row
        
        print("\n\n\n")


    """ Function to print attack board
    
        Grid is printed with " - " as unattacked space, " X " as hit, and " O " as miss
    
    """
    def printAttackBoard(self) -> None:

        # Print column letters
        print("\n\n\n")         # Add separation
        print("     ", end="")    # Add space for row numbers

        for i in range(self.boardSize):
            print(f"{self.columnLetters[i]:^6}", end="")

        for row in range(self.boardSize):
            
            print(f"\n{row + 1:^4}", end="")     # Print row number
            print (f"| {" | ".join(self.attackBoard[row])} |")   # Print row
        
        print("\n\n\n")


    """ Function to attack a position

        Get position and verifies it hasn't been attacked yet
        @return position: position to attack

    """
    def getAttack(self) -> tuple:

        # Create invalid attack flag
        incorrectAttack = True

        # Create verification loop
        while incorrectAttack:

            # Call method to get position to attack
            print("Choose a position to attack.")
            position = self.selectPosition()

            # Declare col and row
            col, row = self.adjustPosition(position)

            # Check if position has already been attacked
            if self.attackBoard[row][col] == " - ":
                return position
            else:
                print("Position has already been attacked. Please try again.")       # Catch invalid input


    """ Function to check if attack hits a ship
    
    @param position: position to attack
    @return int: 0 = miss, 1 = already attacked, 2 = hit

    """
    def checkAttack(self, position: tuple) -> int:

        # Declare fields
        col, row = self.adjustPosition(position)

        # Check if position has a ship
        if self.board[row][col] == " - ":       # Miss

            return 0
        
        elif self.board[row][col] == (" X " | " O "):      # Already attacked

            return 1
        
        else:       # Hit

            return 1


    """ Function to update attack board

        @param position: position to attack
        @param hit: if attack hits a ship

    """
    def updateAttackBoard(self, position: tuple, hit: bool) -> None:

        # Declare fields
        col, row = self.adjustPosition(position)

        # Update attack board
        if hit:
            self.attackBoard[row][col] = " X "
        else:
            self.attackBoard[row][col] = " O "

    
    """ Function to update ship board
    
        @param position: position to attack

    """
    def updateShipBoard(self, position: tuple) -> None:

        # Declare fields
        col, row = self.adjustPosition(position)

        # Update ship board
        self.board[row][col] = " X "


    # Getter methods
    def getDirections(self):

        # Declare directions; structured (y, x)
        directions = {"up": (-1, 0),           # Inverse y values because positive values goes down 
                      "down": (1, 0), 
                      "left": (0, -1), 
                      "right": (0, 1)}
        
        # Return directions
        return directions




# AI class
class AI(Player):

    # Declare class attributes
    name = "AI"
    ships = {}    # {Ship id # : Ship}

    # AI object constructor with difficulty and ships position
        # Sets difficulty
    def __init__(self, difficulty: str) -> None:
        self.difficulty = difficulty    # Save the difficulty
        
        super().__init__(self.name)   # Call the parent class constructor

    # Function to choose ship positions based on diffiuclty
    def choose_ships(self) -> None:
        
        # Declare ships

        # Get difficulty
        if self.difficulty == "easy":
            pass
        
        elif self.difficulty == "medium":
            pass

        elif self.difficulty == "hard":
            pass

        else:
            print("Invalid difficulty")

    # Function to choose a random position to attack
    def choose_position(self) -> None:
        pass



    





