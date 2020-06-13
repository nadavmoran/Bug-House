import chess


def is_not_transplant_legal(board, move):
    try:
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
    if board.piece_type_at(list(squares)[0])==2:
        return True
    return False

