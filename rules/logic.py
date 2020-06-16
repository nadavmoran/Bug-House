import chess
from pieces.piece import *
from pieces.chess_pieces import *


def is_legal(board, row1, row2, col1, col2, piece='P', promotion=None):
    try:
        if promotion is not None:
            move = chr(col1 + 97) + str(row1 + 1) + chr(col2 + 97) + str(row2 + 1) + '=' + promotion
        else:
            if piece == 'P':
                move = chr(col1 + 97) + str(row1 + 1) + chr(col2 + 97) + str(row2 + 1)
            elif piece == 'K' and abs(col2 - col1) > 1:
                move = 'O-O' if col2 > col1 else 'O-O-O'
            else:
                move = piece + chr(col1 + 97) + str(row1 + 1) + chr(col2 + 97) + str(row2 + 1)
        board.push_san(move)
        return True
    except:
        return False


def is_mate(board, color):
    if not board.is_checkmate():
        return False
    squares = board.checkers()
    if len(squares) == 2:
        return True
    if chess.square_distance(list(squares)[0], board.king(color)) == 1:
        return True
    if board.piece_type_at(list(squares)[0]) == 2:
        return True
    return False
