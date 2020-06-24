#inherits classes of the piece class
from pieces.piece import Piece


class Rook(Piece):
    def __init__(self, img, pos, color):
        super().__init__(img, pos, color)
    def __str__(self):
        return 'R'


class Knight(Piece):
    def __init__(self, img, pos, color):
        super().__init__(img, pos, color)
    def __str__(self):
        return 'N'

class Bishop(Piece):
    def __init__(self, img, pos, color):
        super().__init__(img, pos, color)
    def __str__(self):
        return 'B'

class Queen(Piece):
    def __init__(self, img, pos, color):
        super().__init__(img, pos, color)
    def __str__(self):
        return 'Q'

class King(Piece):
    def __init__(self, img, pos, color):
        super().__init__(img, pos, color)
    def __str__(self):
        return 'K'

class Pawn(Piece):
    def __init__(self, img, pos, color):
        super().__init__(img, pos, color)
    def __str__(self):
        return 'P'