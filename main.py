from gui.gui_code import *
from rules.logic import *
from constants import *
from communication.client import *
import socket


def main(color, board, transplant_pieces, transplant_pieces2, start_pos, transplant_start_pos, transplant_start_pos2,
         client):
    map = chess.Board()
    if color == black:
        map = map.transform(chess.flip_vertical)
    stop = False
    moving = False
    transplant_moving = False
    prev_pos = [0, 0]
    prev_pos_logic = [0, 0]
    transplant_pos = transplant_start_pos[:]
    transplant_pos2 = transplant_start_pos2[:]
    prev_color = None
    current_color = None
    tool = None
    transplant_tool = None
    legal = False
    enemy_move = []
    while not stop:
        enemy_move = get_move(client)
        set_board_while_game(enemy_move[0], enemy_move[1])
        for event in pygame.event.get():
            if event.type == QUIT:
                stop = True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                print(transplant_pos, transplant_pos2)
                piece, x, y = get_square_under_mouse(board, start_pos[:])
                transplant_piece, index = get_transplant_piece_under_mouse(transplant_pieces, transplant_start_pos[:])
                transplant_piece2, index2 = get_transplant_piece_under_mouse(transplant_pieces2,
                                                                             transplant_start_pos2[:])
                if not moving and not transplant_moving and piece != None and piece.rect.collidepoint(
                        event.pos) and piece.color == color:
                    prev_color = set_color(x, y)
                    moving = True
                    prev_pos = [start_pos[0] + (x * square_size), start_pos[1] + (y * square_size)]
                    prev_pos_logic = [x, y]
                    tool = piece
                    pygame.draw.rect(game_display, blue, piece.rect, 1)
                elif moving:
                    if x != None and y != None:
                        if tool.__str__() == 'P' and (y == 7 or y == 0):
                            legal = is_legal(map, 7 - prev_pos_logic[1], 7 - y, prev_pos_logic[0], x, 'P', 'Q')
                        elif tool.__str__() == 'K' and abs(x - prev_pos_logic[0]) > 1:
                            legal = is_legal(map, 7 - prev_pos_logic[1], 7 - y, prev_pos_logic[0], x, 'K')
                        else:
                            legal = is_legal(map, 7 - prev_pos_logic[1], 7 - y, prev_pos_logic[0], x, tool.__str__())
                        if legal:
                            if piece != None and tool != piece:
                                if not map.turn:
                                    board[y][x].set_piece(transplant_pos, game_display)
                                    transplant_pieces[
                                        (transplant_pos[0] - transplant_start_pos[0]) // transplant_square_size] = \
                                    board[y][x]
                                    transplant_pos[0] += transplant_square_size
                                    while transplant_pieces[
                                        (transplant_pos[0] - transplant_start_pos[
                                            0]) // transplant_square_size] is not None:
                                        transplant_pos[0] += transplant_square_size
                                else:
                                    board[y][x].set_piece(transplant_pos2, game_display)
                                    transplant_pieces2[
                                        (transplant_pos2[0] - transplant_start_pos2[0]) // transplant_square_size] = \
                                        board[y][x]
                                    transplant_pos2[0] += transplant_square_size
                                    while transplant_pieces2[
                                        (transplant_pos2[0] - transplant_start_pos2[
                                            0]) // transplant_square_size] is not None:
                                        transplant_pos2[0] += transplant_square_size
                            board = set_board_while_game(str(map), True)
                            send_move(client, [str(map)])
                        else:
                            pygame.draw.rect(game_display, black, tool.rect, 1)
                        moving = False
                        '''if tool.__str__() == 'P' and (y == 7 or y == 0):
                            legal = is_legal(map, 7 - prev_pos_logic[1], 7 - y, prev_pos_logic[0], x, 'P', 'Q')
                            if legal == True:
                                promotion_color = 'w' if not map.turn else 'b'
                                tool = Queen(pygame.image.load('gui/pieces_images/' + promotion_color + 'queen.png'),
                                             tool.pos, tool.color)
                        elif tool.__str__() == 'K' and abs(x - prev_pos_logic[0]) > 1:
                            legal = is_legal(map, 7 - prev_pos_logic[1], 7 - y, prev_pos_logic[0], x, 'K')
                            if x > 7 - prev_pos_logic[0] and legal:
                                rook_castle_color = 'w' if not map.turn else 'b'
                                square_castle_color = white if not map.turn else black
                                if not map.turn:
                                    draw_castle([start_pos[0] + (7 * square_size), start_pos[1] + (7 * square_size)],
                                                square_castle_color)
                                    board[7][5] = (
                                        Rook(pygame.image.load('gui/pieces_images/' + rook_castle_color + 'rook.png'),
                                             [tool.pos[0] + square_size, tool.pos[1]], tool.color))
                                    game_display.blit(board[7][5].img, board[7][5].rect)
                                    board[7][7] = None
                                else:
                                    draw_castle([start_pos[0] + (7 * square_size), start_pos[1]],
                                                square_castle_color)
                                    board[0][5] = (
                                        Rook(pygame.image.load('gui/pieces_images/' + rook_castle_color + 'rook.png'),
                                             [tool.pos[0] + square_size, tool.pos[1]], tool.color))
                                    game_display.blit(board[0][5].img, board[0][5].rect)
                                    board[0][7] = None
                                moving = False
                            if x < 7 - prev_pos_logic[0]:
                                rook_castle_color = 'w' if not map.turn else 'b'
                                square_castle_color = white if map.turn else black
                                if not map.turn:
                                    draw_castle([start_pos[0], start_pos[1] + (7 * square_size)],
                                                square_castle_color)
                                    board[7][3] = (
                                        Rook(pygame.image.load('gui/pieces_images/' + rook_castle_color + 'rook.png'),
                                             [tool.pos[0] - square_size, tool.pos[1]], tool.color))
                                    game_display.blit(board[7][3].img, board[7][3].rect)
                                    board[7][0] = None
                                else:
                                    draw_castle([start_pos[0], start_pos[1]],
                                                square_castle_color)
                                    board[0][3] = (
                                        Rook(pygame.image.load('gui/pieces_images/' + rook_castle_color + 'rook.png'),
                                             [tool.pos[0] - square_size, tool.pos[1]], tool.color))
                                    game_display.blit(board[0][3].img, board[0][3].rect)
                                    board[0][7] = None
                                moving = False

                        else:
                            legal = is_legal(map, 7 - prev_pos_logic[1], 7 - y, prev_pos_logic[0], x, tool.__str__())
                    if legal:
                        if x != None and y != None:
                            current_color = set_color(x, y)
                            if piece != None and tool != piece:
                                board[y][x].set_piece(transplant_pos, game_display)
                                transplant_pieces[
                                    (transplant_pos[0] - transplant_start_pos[0]) // transplant_square_size] = board[y][
                                    x]
                                transplant_pos[0] += transplant_square_size
                                while transplant_pieces[
                                    (transplant_pos[0] - transplant_start_pos[0]) // transplant_square_size] != None:
                                    transplant_pos[0] += transplant_square_size
                            draw(prev_pos, prev_color, current_color, x, y)
                            tool.set_piece([start_pos[0] + (x * square_size), start_pos[1] + (y * square_size)],
                                           game_display)
                            board[int((prev_pos[1] - start_pos[1]) // square_size)][
                                int((prev_pos[0] - start_pos[0]) // square_size)] = None
                            board[y][x] = tool
                            moving = False
                    else:
                        pygame.draw.rect(game_display, black, tool.rect, 1)
                        moving = False'''
                elif not transplant_moving and ((transplant_piece != None and transplant_piece.rect.collidepoint(
                        event.pos)) or (transplant_piece2 != None and transplant_piece2.rect.collidepoint(
                    event.pos))) and transplant_piece2 is not None and transplant_piece2.color == color:
                    if not map.turn and index is not None:
                        prev_pos = [transplant_start_pos[0] + (index * transplant_square_size), transplant_start_pos[1]]
                        transplant_tool = transplant_piece
                        pygame.draw.rect(game_display, blue, transplant_piece.rect, 1)
                    else:
                        prev_pos = [transplant_start_pos2[0] + (index2 * transplant_square_size),
                                    transplant_start_pos2[1]]
                        transplant_tool = transplant_piece2
                        pygame.draw.rect(game_display, blue, transplant_piece2.rect, 1)
                    transplant_moving = True
                elif transplant_moving:
                    if str(type(transplant_tool)) == "<class 'pieces.chess_pieces.Pawn'>" and (y == 0 or y == 7):
                        break
                    if x != None and y != None and piece == None:
                        transplant_color = True if map.turn else False
                        legal = is_transplant_legal(map, chess.square(x, 7 - y), transplant_tool.__str__(),
                                                    transplant_color)
                        if legal:
                            current_color = set_color(x, y)
                            draw(prev_pos, white, current_color, x, y)
                            board = set_board_while_game(str(map), True)
                            if map.turn:
                                transplant_pieces[
                                    (prev_pos[0] - transplant_start_pos[0]) // transplant_square_size] = None
                                print(transplant_pieces[
                                          (prev_pos[0] - transplant_start_pos[0]) // transplant_square_size])
                                board[y][x] = transplant_tool
                                transplant_pos[0] = find_first_none(transplant_pieces) * transplant_square_size + \
                                                    transplant_start_pos[0]
                            else:
                                transplant_pieces2[
                                    (prev_pos[0] - transplant_start_pos2[0]) // transplant_square_size] = None
                                board[y][x] = transplant_tool
                                transplant_pos2[0] = find_first_none(transplant_pieces2) * transplant_square_size + \
                                                     transplant_start_pos2[0]
                    elif transplant_piece == transplant_tool:
                        pygame.draw.rect(game_display, white, transplant_piece.rect, 1)
                    elif transplant_piece2 == transplant_tool:
                        pygame.draw.rect(game_display, white, transplant_piece2.rect, 1)
                    transplant_moving = False
                    '''current_color = set_color(x, y)
                    draw(prev_pos, white, current_color, x, y)
                    transplant_tool.set_piece([start_pos[0] + (x * square_size), start_pos[1] + (y * square_size)],
                                              game_display)
                    transplant_pieces[(prev_pos[0] - transplant_start_pos[0]) // transplant_square_size] = None
                    board[y][x] = transplant_tool
                    transplant_moving = False
                    transplant_pos[0] = find_first_none(transplant_pieces) * transplant_square_size + \
                                        transplant_start_pos[0]
            elif transplant_piece == transplant_tool:
                pygame.draw.rect(game_display, white, transplant_piece.rect, 1)
                transplant_moving = False'''
        pygame.display.update()


client = socket.socket()
color = connect(client)
side = color == 'w'
board = set_all_tools(board, start_pos[:], side)
board2 = set_all_tools(board2, start_pos2[:], not side)
main(white if side else black, board, transplant_pieces, transplant_pieces3, start_pos, transplant_start_pos,
     transplant_start_pos3)
pygame.quit()
