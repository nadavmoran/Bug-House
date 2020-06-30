import pygame
from pieces.chess_pieces import *
from constants import *


def set_board(start_pos):
    '''
    draws a 8X8 chess board
    :param start_pos:
    the position of the board
    :return:
    '''
    size = square_size
    boardLength = 8
    cnt = 0
    for i in range(boardLength):
        for j in range(boardLength):
            if cnt % 2 == 0:
                pygame.draw.rect(game_display, white, [size * j + start_pos[0], size * i + start_pos[1], size, size])
            else:
                pygame.draw.rect(game_display, black, [size * j + start_pos[0], size * i + start_pos[1], size, size])
            cnt += 1
        cnt -= 1
    pygame.draw.rect(game_display, black, [start_pos[0], start_pos[1], boardLength * size, boardLength * size], 3)
    board = []
    for y in range(8):
        board.append([])
        for x in range(8):
            board[y].append(None)
    return board

def set_pocket(start_pos):
    '''
    fills a pocket in white
    :param start_pos:
    the position of the board
    :return:
    '''
    for i in range(15):
        pygame.draw.rect(game_display, white, [start_pos[0] + i * transplant_square_size - corner_center_distance, start_pos[1] - corner_center_distance, square_size, square_size])


def set_two_boards(start_pos, start_pos2):
    '''
    sets two list of lists - two boards
    :param start_pos:
    the position of the left board
    :param start_pos2:
    the position of the right board
    :return:
    '''
    board = set_board(start_pos)
    board2 = set_board(start_pos2)
    transplant_pieces = []
    for i in range(16):
        transplant_pieces.append(None)
    transplant_pieces2 = []
    for i in range(16):
        transplant_pieces2.append(None)
    transplant_pieces3 = []
    for i in range(16):
        transplant_pieces3.append(None)
    transplant_pieces4 = []
    for i in range(16):
        transplant_pieces4.append(None)
    pygame.draw.line(game_display, black, (w // 2, 0), (w // 2, h), 5)
    return board, transplant_pieces, board2, transplant_pieces2, transplant_pieces3, transplant_pieces4


def set_tools_in_board(board, start_pos):
    '''
    sets pieces in a board
    :param board:
    the board
    :param start_pos:
    the position of the board
    :return:
    '''
    pos = start_pos[:]
    for i in board:
        pos[0] = start_pos[0]
        for j in i:
            if j != None:
                j.set_piece(pos[:], game_display)
                pos[0] += square_size
        pos[1] += square_size


def set_all_tools(board, start_pos, is_left_board):
    '''
    sets all the pieces in the two boards
    :param board:
    the board
    :param start_pos:
    the position of the board
    :param is_left_board:
    the location of the board
    :return:
    '''
    images = []
    if is_left_board:
        names = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']
        for name in names:
            images.append(pygame.image.load('gui/pieces_images/b' + name + '.png'))
        for name in names:
            images.append(pygame.image.load('gui/pieces_images/w' + name + '.png'))
        tools = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        color1 = black
        color2 = white
    else:
        names = ['rook', 'knight', 'bishop', 'king', 'queen', 'pawn']
        for name in names:
            images.append(pygame.image.load('gui/pieces_images/w' + name + '.png'))
        for name in names:
            images.append(pygame.image.load('gui/pieces_images/b' + name + '.png'))
        tools = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]
        color1 = white
        color2 = black
    cnt = 0
    pos = start_pos[:]
    for img in images[:5]:
        board[0][cnt] = tools[cnt](img, pos[:], color1)
        pos[0] += square_size
        cnt += 1
    for img in images[2::-1]:
        board[0][cnt] = tools[cnt](img, pos[:], color1)
        pos[0] += square_size
        cnt += 1
    pos = [75, 150]
    for i in range(8):
        board[1][i] = Pawn(images[5], pos[:], color1)
        pos[0] += square_size
    cnt = 0
    pos = [75, 450]
    for img in images[6:-1]:
        board[-1][cnt] = tools[cnt](img, pos[:], color2)
        pos[0] += square_size
        cnt += 1
    for img in images[8:5:-1]:
        board[-1][cnt] = tools[cnt](img, pos[:], color2)
        pos[0] += square_size
        cnt += 1
    pos = [75, 400]
    for i in range(8):
        board[-2][i] = Pawn(images[11], pos[:], color2)
        pos[0] += square_size
    set_tools_in_board(board, start_pos)
    return board


def get_square_under_mouse(board, start_pos):
    '''
    returns the position of a click on the board and what there is there
    :param board:
    :param start_pos:
    :return:
    '''
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - (
        start_pos[0] - corner_center_distance, start_pos[1] - corner_center_distance)
    x, y = [(int(i // square_size)) for i in mouse_pos]
    if x is not None and y is not None:
        if 0 <= x <= 7 and 0 <= y <= 7:
            return board[y][x], x, y
    return None, None, None


def get_transplant_piece_under_mouse(transplant_pieces, transplant_start_pos):
    '''
    returns the position of a click on the pocket and what there is there
    :param transplant_pieces:
    :param transplant_start_pos:
    the position of the pocket
    :return:
    '''
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - (
        transplant_start_pos[0] - corner_center_distance, transplant_start_pos[1] - corner_center_distance)
    x, y = [(int(i // transplant_square_size)) for i in mouse_pos]
    if x is not None and y is not None:
        if 0 <= x <= 15 and y == 0:
            return transplant_pieces[x], x
    return None, None


def set_board_while_game_tmp(board, map, start_pos):
    col, row = 0, 0
    for piece in map[::2]:
        if col == 8:
            col = 0
            row += 1
        if tools[piece] is not None:
            if piece.isupper():
                board[row][col] = tools[piece](
                    pygame.image.load('gui/pieces_images/w' + (tools[piece].__name__).lower() + '.png'), [0, 0], white)
            else:
                board[row][col] = tools[piece](
                    pygame.image.load('gui/pieces_images/b' + (tools[piece].__name__).lower() + '.png'), [0, 0], black)
        # board[row][col] = tools[piece]
        if board[row][col] is not None:
            board[row][col].set_piece([start_pos[0] + col * square_size, start_pos[1] + row * square_size],
                                      game_display)
        col += 1


def set_board_while_game(map, left):
    '''
    draws a board
    :param map:
    string of a Board object
    :param left:
    the location of the board
    :return:
    '''
    if left:
        board = set_board((start_pos[0] - corner_center_distance,
                           start_pos[1] - corner_center_distance))
        set_board_while_game_tmp(board, map, start_pos)
        return board
    else:
        board2 = set_board((start_pos2[0] - corner_center_distance,
                            start_pos2[1] - corner_center_distance))
        set_board_while_game_tmp(board2, map, start_pos2)
        return board2


def set_pocket_while_game_tmp(pocket, transplant_pieces, transplant_start_pos, color):
    set_pocket(transplant_start_pos)
    for i in range(len(transplant_pieces)):
        transplant_pieces[i] = None
    index = 0
    for piece in pocket:
        if color == [255, 255, 255]:
            transplant_pieces[index] = tools[piece.upper()](
                pygame.image.load('gui/pieces_images/w' + (tools[piece.upper()].__name__).lower() + '.png'), [0,0], white)
        else:
            transplant_pieces[index] = tools[piece.upper()](
                pygame.image.load('gui/pieces_images/b' + (tools[piece.upper()].__name__).lower() + '.png'), [0,0], black)
        if transplant_pieces[index] is not None:
            transplant_pieces[index].set_piece([transplant_start_pos[0] + index * transplant_square_size, transplant_start_pos[1]], game_display)
        index +=1


def set_pocket_while_game(pocket, left, up, color):
    '''
    draws a pocket from a string of a Pocket Object
    :param pocket:
    :param left:
    represents the pocket's board
    :param up:
    represents the location of the pocket
    :param color:
    the color the pieces color
    :return:
    '''
    if left and up:
        set_pocket_while_game_tmp(pocket, transplant_pieces, transplant_start_pos, color)
        return transplant_pieces
    elif left and not up:
        set_pocket_while_game_tmp(pocket, transplant_pieces3, transplant_start_pos3, color)
        return transplant_pieces3
    elif not left and up:
        set_pocket_while_game_tmp(pocket, transplant_pieces2, transplant_start_pos2, color)
        return transplant_pieces2
    else:
        set_pocket_while_game_tmp(pocket, transplant_pieces4, transplant_start_pos4, color)
        return transplant_pieces4

#calls the methods
pygame.init()
game_display = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption("Chess")
w, h = pygame.display.get_surface().get_size()
start_pos = [int(w // 24) + corner_center_distance, int(h // 5) + corner_center_distance]
start_pos2 = [int(w // 1.5) + corner_center_distance, int(h // 5) + corner_center_distance]
transplant_start_pos = [corner_center_distance, h // 7]
transplant_start_pos2 = [w // 2 + 33, h // 7]
transplant_start_pos3 = [corner_center_distance, start_pos[1] + square_size * 8]
transplant_start_pos4 = [w // 2 + 33, start_pos[1] + square_size * 8]
game_display.fill(white)
board, transplant_pieces, board2, transplant_pieces2, transplant_pieces3, transplant_pieces4 = set_two_boards(
    (start_pos[0] - corner_center_distance,
     start_pos[1] - corner_center_distance),
    (start_pos2[0] - corner_center_distance,
     start_pos2[1] - corner_center_distance))
tools = {'R': Rook,
         'N': Knight,
         'B': Bishop,
         'Q': Queen,
         'K': King,
         'P': Pawn,
         'r': Rook,
         'n': Knight,
         'b': Bishop,
         'q': Queen,
         'k': King,
         'p': Pawn,
         '.': None}
