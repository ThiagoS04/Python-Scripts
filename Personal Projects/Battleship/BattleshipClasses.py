# Thiago Schcuk 23 January 2024
# This script is the class file for the battleship game. It contains the classes for the player, AI, and ships.

# Ship class
class Ship:

    # Declare fields
    size = 0                # Size of ship
    position: tuple     # Position of top of ship (row, col)
    orientation: str        # Orientation of ship
    id: int                 # Ship id
    shipSegments: list       # List of ship segments
    sunk = False            # Whether ship is sunk or not

    # Constructor of ship object
    def __init__(self, size: int, orientation: str, position: tuple, id: int) -> None:
        self.size = size
        self.position = position
        self.orientation = orientation
        self.id = id
        self.shipSegments = []        # Initialize ship segments list

        # Get row and col
        col, row = Player.adjustPosition(position)

        # Get row and column changes
        rowChange, colChange = Player.getDirections().get(orientation)

        # Create ship segments
        for i in range(size):

            # Update position
            position = (col + i * colChange, row + i * rowChange)
            
            # Create ship segment object
            segment = self.ShipSegment(position, id)

            # Store ship segment
            self.shipSegments.append(segment)

    # Class to hold whether ship segment is hit or not
    class ShipSegment:
        
        # Declare fields
        position: tuple         # Position of ship segment
        id: int                 # Ship id segment belongs to
        hit = False             # Whether ship segment is hit or not

        # Constructor of ship segment object
        def __init__(self, position: tuple, id: int) -> None:
            self.position = position

        # Function to set ship segment as hit
        def markHit(self) -> None:
            self.hit = True

        # Getter methods
        def getPosition(self) -> tuple:
            return self.position
        def getId(self) -> int:
            return self.id
        def getHit(self) -> bool:
            return self.hit

    # Function to determine if ship is sunk (All segments are hit)
    def isSunk(self) -> bool:

        # Loop through all ship segments
        for segment in self.shipSegments:
            
            # If any segment is not hit, return False
            if not segment.getHit():
                return False

        # If all segments are hit, return True
        return True
    
    # Fucntion to hit ship segment
    def hitSegment(self, position: tuple) -> None:

        # Loop through all ship segments
        for segment in self.shipSegments:
            
            # If segment is at position, set it as hit
            if segment.getPosition() == position:
                segment.markHit()
                
        # Check if ship is sunk
        self.sunk = self.isSunk()

    # Getter methods
    def getSize(self) -> int:
        return self.size
    
    def getPosition(self) -> list:
        return self.position
    
    def getOrientation(self) -> int:
        return self.orientation
    
    def getSunk(self) -> bool:
        return self.sunk
    
    def getShipId(self) -> int:
        return self.id
    

# Player class
class Player:

    # Declare class attributes
    boardSize = 10
    numShips = 5
    ships: dict    # {Ship id # : Ship object}
    shipLocations: list
    columnLetters = [chr(65 + i) for i in range(boardSize)]    # List of column letters
    allShips = [2, 3, 3, 4, 5]            # List of all ships

    """ Player object constructor with name and ships position
    
    Sets name and creates board
    " - " is empty space and ship size is ship
    " X " is a hit, " O " is a miss
    
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.board = [[" - " for i in range(self.boardSize)] for i in range(self.boardSize)]            # Board to keep track of ships
        self.attackBoard = [[" - " for i in range(self.boardSize)] for i in range(self.boardSize)]      # Board to keep track of attacks
        self.shipLocations = [[None for i in range(self.boardSize)] for i in range(self.boardSize)]    # Board to keep track of ship locations
        self.ships = {}


    # Function to choose ship positions
    def placeShips(self) -> None:

        # Declare fields
        availableShips = self.allShips[:]          # List of ships user hasn't placed yet

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
                    confirmation = input("Are you sure you want to place a ship of size "
                                        f"{shipSize} at position {position} with orientation {orientation}? (y/n)\t")
                    if confirmation.upper()[0] == "Y":
                        verifiedShip = True

            # Remove ship from available ships
            availableShips.remove(shipSize)

            # Create ship id
            shipId = self.allShips.index(shipSize)
            if shipId == 1:         # Distinguish between the two 3 size ships
                shipId = 11 if shipSize in availableShips else 12

            # Create ship object
            ship = Ship(shipSize, orientation, position, shipId)

            # Call method to place ship
            self.placeShip(ship)

            # Show board
            self.printBoard()


    """ Function to place ship
    @param ship: ship to place
    
    """
    def placeShip(self, ship:Ship) -> None:
        
        # Store ship information
        self.storeShipInfo(ship, ship.getShipId())

        # Place ship on board
        self.placeShipOnBoard(ship)


    """ Function to store ship information

    @param ship: ship to place
    @param shipId: id of ship to place

    """
    def storeShipInfo(self, ship: Ship, shipId: int) -> None:

        # Get row and col
        col, row = Player.adjustPosition(ship.getPosition())
        orientation = ship.getOrientation()

         # Get row and column changes
        rowChange, colChange = Player.getDirections().get(orientation)

        # Add ship to dictionary
        self.ships[shipId] = ship

        # Add ship to ship locations
        for i in range(ship.size):
            self.shipLocations[row + i * rowChange][col + i * colChange] = shipId      


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
            userInput = input(f"Which size ship would you like to place?\n"
                    f"The sizes available are {' '.join(map(str, availableShips))}\t")
            
            # Try to convert input to int
            try:

                shipSize = int(userInput)

            except ValueError:         # Catch invalid input

                print("Invalid input. Please try again.")
                continue        # Skip rest of while block
            
            # Note which ship was selected
            print("You chose the ship with a size of", shipSize)

            # Return if ship size is valid
            if not self.verifyShipSize(shipSize) or shipSize not in availableShips:

                print("Invalid ship size. Please try again.")       # Catch invalid input

            else:
                return shipSize
    

    """ Function to select position

    @return position: position of ship selected
    
    """
    def selectPosition(self) -> tuple:
        
        # Create invalid position flags
        invalidColumn = True
        invalidRow = True

        # Create verification loop
        while invalidColumn:

            # Ask user for position of ship
            col = input("Select column:\t").upper()

            # Verify column input
            if not self.verifyColumn(col):
                print("Invalid column. Please try again.")
            else:
                invalidColumn = False

        while invalidRow:

            userInput = input("Select row:\t")

            # Try to convert input to int
            try:

                row = int(userInput)

                # Verify row input
                if not self.verifyRow(row):
                    raise ValueError
                
                invalidRow = False

            except ValueError:         # Catch invalid input

                print("Invalid input. Please try again.")

        # Return position
        return (col,row)
    

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

        # Note which position was selected
        print("You chose the position", position)

        # Get user confirmation
        confirmation = input("Are you sure you want to attack this position? (y/n)\t")
        return confirmation.upper()[0] == "Y"
    
    def verifyColumn(self, column: str) -> bool:
        return column in Player.columnLetters
    
    def verifyRow(self, row: int) -> bool:
        return row in range(self.boardSize + 1)
    
    def verifyOrientation(self, orientation: str) -> bool:
        return orientation in ["up", "down", "left", "right"]
    
    # Function to adjust position for 0 index and convert column letter to number
    def adjustPosition(position: tuple) -> tuple:

        # Declare fields
        col, row = position
        row -= 1                                    # Adjust for 0 index
        colIndex = Player.columnLetters.index(col)         # Convert to number

        return (colIndex, row)
    

    # Function checks if all spaces the ship would occupy are empty
    def checkSpace(self, shipSize: int, position: tuple, orientation: str):

        # Declare fields
        col, row = Player.adjustPosition(position)
        direction = Player.getDirections().get(orientation)
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
        col, row = Player.adjustPosition(ship.getPosition())
        orientation = ship.getOrientation()
        size = ship.getSize()
        
        # Get row and column changes
        rowChange, colChange = Player.getDirections().get(orientation)
        
        # Place ship on board
        for i in range(size):
            self.board[row + i * rowChange][col + i * colChange] = " " + str(size) + " "

    """ Function to print board with ships

        Grid is printed with " - " as empty space and ship size as ship    

    """
    def printBoard(self) -> None:
        
        # Notify which board is being printed
        print(f"Your ship board {self.name}:")

        # Print column letters
        print("\n\n\n")         # Add separation
        print("     ", end="")    # Add space for row numbers

        for i in range(self.boardSize):
            print(f"{Player.columnLetters[i]:^6}", end="")

        for row in range(self.boardSize):
            
            print(f"\n{row + 1:^4}", end="")     # Print row number
            print (f"| {" | ".join(self.board[row])} |")   # Print row
        
        print("\n\n\n")


    """ Function to print attack board
    
        Grid is printed with " - " as unattacked space, " X " as hit, and " O " as miss
    
    """
    def printAttackBoard(self) -> None:

        # Notify user which board is being printed
        print(f"Your attack board {self.name}:")
        
        # Print column letters
        print("\n\n\n")         # Add separation
        print("     ", end="")    # Add space for row numbers

        for i in range(self.boardSize):
            print(f"{Player.columnLetters[i]:^6}", end="")

        for row in range(self.boardSize):
            
            print(f"\n{row + 1:^4}", end="")     # Print row number
            print (f"| {" | ".join(self.attackBoard[row])} |")   # Print row
        
        print("\n\n\n")


    """ Function to attack a position

        Get position and verifies it hasn't been attacked yet
        @return position: position to attack

    """
    def getAttack(self) -> tuple:

        # Print attack board for player to see
        self.printAttackBoard()

        # Call method to get position to attack
        print(f"{self.name}, choose a position to attack.")
        position = self.selectPosition()

        # Confirm attack
        if not self.verifyPosition(position):
            position = self.getAttack()
        
        # Return attack coordinates
        return position


    """ Function to check if attack hits a ship
    
    @param position: position to attack
    @return int: 0 = miss, 1 = already attacked, 2 = hit

    """
    def checkAttack(self, position: tuple, defendingPlayer: "Player") -> int:

        # Declare fields
        col, row = Player.adjustPosition(position)

        # Check if position has a ship
        if defendingPlayer.board[row][col] == " - ":       # Miss

            # Print miss message
            print("Miss!")

            return 0
        
        elif self.attackBoard[row][col] in [" X "," O "]:      # Already attacked
            
            return 1
        
        else:       # Hit

            # Print hit message
            print("Hit!")

            # Get ship id
            shipId = defendingPlayer.shipLocations[row][col]
            
            # Get ship object
            ship = defendingPlayer.ships[shipId]

            # Hit ship segment
            ship.hitSegment(Player.adjustPosition(position))

            # Check if ship is sunk
            if ship.isSunk():

                # Print sunk message
                print("You sunk my BattleShip!")

                # Remove ship from ships list
                del defendingPlayer.ships[shipId]

                # Check if all ships are sunk
                if len(defendingPlayer.ships) == 0:

                    # Print game over message
                    print("You sunk all my ships!")

            return 2


    """ Function to update attack board

        @param position: position to attack
        @param hit: if attack hits a ship

    """
    def updateAttackBoard(self, position: tuple, hit: bool) -> None:

        # Declare fields
        col, row = Player.adjustPosition(position)

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
        col, row = Player.adjustPosition(position)

        # Update ship board
        self.board[row][col] = " X "


    # Getter methods
    def getDirections() -> tuple:

        # Declare directions; structured (y, x)
        directions = {"up": (-1, 0),           # Inverse y values because positive values goes down 
                      "down": (1, 0), 
                      "left": (0, -1), 
                      "right": (0, 1)}
        
        # Return directions
        return directions
    
    def getShips(self) -> dict:
        return self.ships




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



    





