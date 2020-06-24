import chess
import chess.variant

def is_legal(board, row1, row2, col1, col2, piece='P', promotion=None):
    print('the turn is '+str(board.turn))
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


def is_transplant_legal(board, pocket, square, piece,):
    piece = piece_letter_to_piece_type(piece)
    if not board.is_check():
        board.set_piece_at(square, chess.Piece(piece, board.turn))
        pocket.remove(piece)
        board.push(chess.Move.null())
        return True
    board.set_piece_at(square, chess.Piece(piece, board.turn))
    if board.is_check():
        board.remove_piece_at(square)
        return False
    pocket.remove(piece)
    board.push(chess.Move.null())
    return True

def piece_letter_to_piece_type(piece):
    if piece == 'P':
        return 1
    elif piece == 'N':
        return 2
    elif piece == 'B':
        return 3
    elif piece == 'R':
        return 4
    elif piece == 'Q':
        return 5
    return 6
