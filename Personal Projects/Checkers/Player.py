"""
    Thiago Schuck 25 February 2025
    This is a checkers game that implements a GUI
    This is the player class that represents a player in the game
    
"""

import Piece

class Player:

    # Declare global variables
    pieceCount = 12
    boardLength = 8

    """
        Constructor of the player class
        :param name: name of the player
        :param color: color of the player
    """
    def __init__(self, name, color) -> None:

        self.name = name
        self.color = color
        self.king_pieces = []

        # Determine the starting position of the pieces
        if color == "black":
            self.starting_row = 0
            self.starting_column = 0
        else:
            self.starting_row = 5
            self.starting_column = 0

        # Initialize pieces
        self.pieces = self.initializePieces()



    """
        Initialize the pieces of the player
        :param pieces: list of pieces
        :return: list of pieces
    """
    def initializePieces(self) -> list:

        row = self.starting_row
        col = self.starting_column
        pieces = []

        for i in range(3):          # 3 rows of pieces
            
            col = 1 if i % 2 == 0 else 0            # Row and column have an opposite parity

            for j in range(4):      # 4 pieces in each row
                
                position = (row, col)                   # Set position of piece
                piece = Piece.Piece(self.color, position)     # Create piece object
                col += 2                                # Update column
                pieces.append(piece)               # Add piece to list of pieces

            row += 1                                # Update row

        return pieces


    
    """ Getter methods """
    def getName(self) -> str:
        return self.name
    def getColor(self) -> str:
        return self.color
    def getPieces(self) -> list:
        return self.pieces
    