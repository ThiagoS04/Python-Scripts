"""
    Thiago Schuck 25 February 2025
    This is a checkers game that implements a GUI
    This is the piece class that represents a piece in the game

"""

class Piece:

    def __init__(self, color, position) -> None:

        self.color = color
        self.position = position
        self.king = False



    """
        This method is used to crown a piece as a king
        :return: None
    """
    def kingPiece(self) -> None:
        self.king = True



    """ Getter Methods """
    def getColor(self) -> str:
        return self.color
    def getPosition(self) -> tuple:
        return self.position
    def getKing(self) -> bool:
        return self.king
    def __str__(self) -> str:
        return f"Piece(color={self.color}, position={self.position}, king={self.king})"
    
    """ Setter Methods """
    def setPosition(self, position) -> None:
        self.position = position
    def setKing(self, king) -> None:
        self.king = king
    