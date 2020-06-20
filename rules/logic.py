import chess
import chess.variant
from pieces.piece import *
from pieces.chess_pieces import *


def is_legal(board, row1, row2, col1, col2, piece='P', promotion=None):
    print(type(board))
    print(promotion)
    try:
        if promotion is not None:
            move = chr(col1 + 97) + str(row1 + 1) + chr(col2 + 97) + str(row2 + 1) + '=' + promotion
        else:
            if piece == 'P':
                move = chr(col1 + 97) + str(row1 + 1) + chr(col2 + 97) + str(row2 + 1)
            elif piece == 'K' and 3 > abs(col2 - col1) > 1 and row1 == row2 and 0 != col2 != 7:
                move = 'O-O' if col2 > col1 else 'O-O-O'
            else:
                move = piece + chr(col1 + 97) + str(row1 + 1) + chr(col2 + 97) + str(row2 + 1)
        print(move)
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


def is_transplant_legal(board, square, piece, color):
    if not board.turn == color:
        return False
    if piece == 'P':
        piece = 1
    elif piece == 'N':
        piece = 2
    elif piece == 'B':
        piece = 3
    elif piece == 'R':
        piece = 4
    elif piece == 'Q':
        piece = 5
    if not board.is_check():
        board.set_piece_at(square, chess.Piece(piece, color))
        board.push(chess.Move.null())
        return True
    board.set_piece_at(square, chess.Piece(piece, color))
    if board.is_check():
        board.remove_piece_at(square)
        return False
    board.push(chess.Move.null())
    return True
