import pygame
from pygame.locals import *
from pieces.chess_pieces import *
from constants import *


def set_board(start_pos):
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


def set_two_boards(start_pos, start_pos2):
    board = []
    board2 = []
    for y in range(8):
        board.append([])
        for x in range(8):
            board[y].append(None)
    for y in range(8):
        board2.append([])
        for x in range(8):
            board2[y].append(None)
    transplant_pieces = []
    for i in range(16):
        transplant_pieces.append(None)
    transplant_pieces2 = []
    for i in range(16):
        transplant_pieces2.append(None)
    set_board(start_pos)
    set_board(start_pos2)
    pygame.draw.line(game_display, black, (w // 2, 0), (w // 2, h), 5)
    return board, transplant_pieces, board2, transplant_pieces2


def set_tools_in_board(board, start_pos):
    pos = start_pos[:]
    for i in board:
        pos[0] = start_pos[0]
        for j in i:
            if j != None:
                j.set_piece(pos[:],game_display)
                pos[0] += square_size
        pos[1] += square_size


def set_all_tools(board, start_pos, is_left_board):
    images = []
    if is_left_board:
        names = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']
        for name in names:
            images.append(pygame.image.load('gui/pieces_images/b' + name + '.png'))
        for name in names:
            images.append(pygame.image.load('gui/pieces_images/w' + name + '.png'))
        tools = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        color1=black
        color2=white
    else:
        names = ['rook', 'knight', 'bishop', 'king', 'queen', 'pawn']
        for name in names:
            images.append(pygame.image.load('gui/pieces_images/w' + name + '.png'))
        for name in names:
            images.append(pygame.image.load('gui/pieces_images/b' + name + '.png'))
        tools = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]
        color1=white
        color2=black
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
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - (start_pos[0] - corner_center_distance, start_pos[1] - corner_center_distance)
    x, y = [(int(i // square_size)) for i in mouse_pos]
    if x is not None and y is not None:
        if 0 <= x <= 7 and 0 <= y <= 7:
            return board[y][x], x, y
    return None, None, None


def get_transplant_piece_under_mouse(transplant_pieces, transplant_start_pos):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - (transplant_start_pos[0] - corner_center_distance, transplant_start_pos[1] - corner_center_distance)
    x, y = [(int(i // transplant_square_size)) for i in mouse_pos]
    if x is not None and y is not None:
        if 0 <= x <= 15 and y == 0:
            return transplant_pieces[x], x
    return None, None


def find_first_none(lst):
    for i in range(len(lst)):
        if lst[i] is None:
            return i


def set_color(x, y):
    if x % 2 == y % 2:
        return white
    else:
        return black


def draw(prev_pos, prev_color, current_color, x, y):
    pygame.draw.rect(game_display, prev_color,
                     [prev_pos[0] - corner_center_distance, prev_pos[1] - corner_center_distance, square_size,
                      square_size])
    pygame.draw.rect(game_display, current_color,
                     [start_pos[0] - corner_center_distance + (x * square_size),
                      start_pos[1] - corner_center_distance + (y * square_size), square_size, square_size])
    pygame.draw.rect(game_display, black,
                     [start_pos[0] - corner_center_distance, start_pos[1] - corner_center_distance, 400, 400], 3)

def draw_castle(prev_pos, prev_color):
    pygame.draw.rect(game_display, prev_color,
                     [prev_pos[0] - corner_center_distance, prev_pos[1] - corner_center_distance, square_size,
                      square_size])
    #pygame.draw.rect(game_display, black,
     #                [start_pos[0] - corner_center_distance, start_pos[1] - corner_center_distance, 400, 400], 3)

def game(board, transplant_pieces, start_pos, transplant_start_pos, color):
    stop = False
    moving = False
    transplant_moving = False
    prev_pos = [0, 0]
    prev_pos_logic=[0,0]
    transplant_pos = transplant_start_pos[:]
    prev_color = None
    current_color = None
    tool = None
    transplant_tool = None
    while not stop:
        for event in pygame.event.get():
            if event.type == QUIT:
                stop = True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                piece, x, y = get_square_under_mouse(board, start_pos[:])
                transplant_piece, index = get_transplant_piece_under_mouse(transplant_pieces, transplant_start_pos[:])
                if not moving and not transplant_moving and piece != None and piece.color==color and piece.rect.collidepoint(event.pos):
                    prev_color=set_color(x,y)
                    moving = True
                    prev_pos = [start_pos[0] + (x * square_size), start_pos[1] + (y * square_size)]
                    prev_pos_logic=[y,x]
                    tool = piece
                    pygame.draw.rect(game_display, blue, piece.rect, 1)
                elif moving:
                    if x != None and y != None:
                        current_color=set_color(x,y)
                        if piece != None and tool != piece:
                            board[y][x].set_piece(transplant_pos,game_display)
                            transplant_pieces[(transplant_pos[0] - transplant_start_pos[0]) // transplant_square_size] = board[y][x]
                            transplant_pos[0] += transplant_square_size
                            while transplant_pieces[(transplant_pos[0] - transplant_start_pos[0]) // transplant_square_size] != None:
                                transplant_pos[0] += transplant_square_size
                        draw(prev_pos, prev_color, current_color, x, y)
                        tool.set_piece([start_pos[0] + (x * square_size), start_pos[1] + (y * square_size)],game_display)
                        board[int((prev_pos[1] - start_pos[1]) // square_size)][int((prev_pos[0] - start_pos[0]) // square_size)] = None
                        board[y][x] = tool
                        moving = False
                elif not transplant_moving and transplant_piece != None and transplant_piece.color==color and transplant_piece.rect.collidepoint(
                        event.pos):
                    transplant_moving = True
                    prev_pos = [transplant_start_pos[0] + (index * transplant_square_size), transplant_start_pos[1]]
                    transplant_tool = transplant_piece
                    pygame.draw.rect(game_display, blue, transplant_piece.rect, 1)
                elif transplant_moving:
                    if str(type(transplant_tool)) == "<class 'pieces.chess_pieces.Pawn'>" and (y==0 or y==7):
                        break
                    if x != None and y != None and piece == None:
                        current_color=set_color(x,y)
                        draw(prev_pos, white, current_color, x, y)
                        transplant_tool.set_piece([start_pos[0] + (x * square_size), start_pos[1] + (y * square_size)],game_display)
                        transplant_pieces[(prev_pos[0] - transplant_start_pos[0]) // transplant_square_size] = None
                        board[y][x] = transplant_tool
                        transplant_moving = False
                        transplant_pos[0] = find_first_none(transplant_pieces) * transplant_square_size + transplant_start_pos[0]
                    elif transplant_piece == transplant_tool:
                        pygame.draw.rect(game_display, white, transplant_piece.rect, 1)
                        transplant_moving = False
        pygame.display.update()


pygame.init()
game_display = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption("Chess")
w, h = pygame.display.get_surface().get_size()
start_pos = [int(w // 24) + corner_center_distance, int(h // 5) + corner_center_distance]
start_pos2 = [int(w // 1.5) + corner_center_distance, int(h // 5) + corner_center_distance]
transplant_start_pos = [corner_center_distance, h // 7]
transplant_start_pos2 = [w // 2 + 33, h // 7]
game_display.fill(white)
board, transplant_pieces, board2, transplant_pieces2 = set_two_boards((start_pos[0] - corner_center_distance,
                                                                       start_pos[1] - corner_center_distance),
                                                                      (start_pos2[0] - corner_center_distance,
                                                                       start_pos2[1] - corner_center_distance))
board = set_all_tools(board, start_pos[:], True)
board2 = set_all_tools(board2, start_pos2[:], False)
'''t1 = threading.Thread(target=game, args=(board, transplant_pieces, start_pos[:], transplant_start_pos[:]))
t2 = threading.Thread(target=game, args=(board2, transplant_pieces2, start_pos2[:], transplant_start_pos2[:]))
t1.start()
t2.start()'''
#game(board, transplant_pieces, start_pos[:], transplant_start_pos[:],white)
#game(board2, transplant_pieces2, start_pos2[:], transplant_start_pos2[:],black)
#pygame.quit()