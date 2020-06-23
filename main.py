from gui.gui_code import *
from rules.logic import *
from communication.client import *
import socket
from pygame.locals import *


def main(color, board, transplant_pieces, start_pos, transplant_start_pos, client):
    map = chess.Board()
    my_pocket = chess.variant.CrazyhousePocket()
    other_pocket = chess.variant.CrazyhousePocket()
    if color == black:
        map = map.transform(chess.flip_horizontal).transform(chess.flip_vertical)
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
    fix_row, fix_col = 0, 0
    if color == white:
        fix_row = 7
    else:
        fix_col = 7
    while not stop:
        enemy_move = get_move(client)
        if enemy_move:
            if enemy_move[board_side_index]:
                map = chess.Board(enemy_move[board_fen_index])
                board = set_board_while_game(enemy_move[string_board_index], enemy_move[board_side_index])
            else:
                set_board_while_game(enemy_move[string_board_index], enemy_move[board_side_index])
            if 't' in enemy_move[move_type_index]:
                print(enemy_move)
                if enemy_move[transplant_board_side_index] and not enemy_move[pocket_side_index]:
                    my_pocket = chess.variant.CrazyhousePocket(enemy_move[pocket_index])
                    transplant_pieces = set_pocket_while_game(enemy_move[pocket_index],
                                                              enemy_move[transplant_board_side_index],
                                                              enemy_move[pocket_side_index],
                                                              enemy_move[taken_piece_color_index])
                elif not enemy_move[transplant_board_side_index] and not enemy_move[pocket_side_index]:
                    other_pocket = chess.variant.CrazyhousePocket(enemy_move[pocket_index])
                set_pocket_while_game(enemy_move[pocket_index],
                                      enemy_move[transplant_board_side_index],
                                      enemy_move[pocket_side_index],
                                      enemy_move[taken_piece_color_index])
        for event in pygame.event.get():
            if event.type == QUIT:
                stop = True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                piece, x, y = get_square_under_mouse(board, start_pos[:])
                transplant_piece, index = get_transplant_piece_under_mouse(transplant_pieces, transplant_start_pos[:])
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
                            legal = is_legal(map, abs(fix_row - prev_pos_logic[1]), abs(fix_row - y), abs(fix_col - prev_pos_logic[0]),abs(fix_col - x), 'P', 'Q')
                        elif tool.__str__() == 'K' and abs(x - prev_pos_logic[0]) > 1:
                            legal = is_legal(map, abs(fix_row - prev_pos_logic[1]), abs(fix_row - y), abs(fix_col - prev_pos_logic[0]), abs(fix_col - x), 'K')
                        else:
                            legal = is_legal(map, abs(fix_row - prev_pos_logic[1]), abs(fix_row - y), abs(fix_col - prev_pos_logic[0]), abs(fix_col - x), tool.__str__())
                        print(map)
                        if legal:
                            if piece != None and tool != piece:
                                tmp = str(map) if color == white else str(map)[::-1]
                                board = set_board_while_game(tmp, True)
                                other_pocket.add(piece_letter_to_piece_type(piece.__str__()))
                                stop = send_move(client, [str(map), 'tc', map.fen(), str(other_pocket), piece.color])
                                '''if not map.turn:
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
                                        transplant_pos2[0] += transplant_square_size'''
                            else:
                                tmp = str(map) if color == white else str(map)[::-1]
                                board = set_board_while_game(tmp, True)
                                stop = send_move(client, [str(map), 'm', map.fen()])
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
                elif not transplant_moving and transplant_piece != None and transplant_piece.rect.collidepoint(event.pos):
                    prev_pos = [transplant_start_pos[0] + (index * transplant_square_size), transplant_start_pos[1]]
                    transplant_tool = transplant_piece
                    pygame.draw.rect(game_display, blue, transplant_piece.rect, 1)
                    transplant_moving = True
                elif transplant_moving:
                    if str(type(transplant_tool)) == "<class 'pieces.chess_pieces.Pawn'>" and (y == 0 or y == 7):
                        break
                    if x != None and y != None and piece == None:
                        transplant_color = True if map.turn else False
                        legal = is_transplant_legal(map, my_pocket, chess.square(abs(fix_col - x), abs(fix_row - y)), transplant_tool.__str__(),
                                                    transplant_color)
                        print(legal)
                        if legal:
                            tmp = str(map) if color == white else str(map)[::-1]
                            board = set_board_while_game(tmp, True)
                            stop = send_move(client, [str(map), 't', map.fen(), str(my_pocket), transplant_tool.color])
                            '''current_color = set_color(x, y)
                            draw(prev_pos, white, current_color, x, y)
                            board = set_board_while_game(str(map), True)
                            if map.turn:
                                transplant_pieces[
                                    (prev_pos[0] - transplant_start_pos[0]) // transplant_square_size] = None
                                board[y][x] = transplant_tool
                                transplant_pos[0] = find_first_none(transplant_pieces) * transplant_square_size + \
                                                    transplant_start_pos[0]
                            else:
                                transplant_pieces2[
                                    (prev_pos[0] - transplant_start_pos2[0]) // transplant_square_size] = None
                                board[y][x] = transplant_tool
                                transplant_pos2[0] = find_first_none(transplant_pieces2) * transplant_square_size + \
                                                     transplant_start_pos2[0]'''
                    elif transplant_piece == transplant_tool:
                        pygame.draw.rect(game_display, white, transplant_piece.rect, 1)
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
pygame.display.update()
main(white if side else black, board, transplant_pieces3, start_pos, transplant_start_pos3, client)
pygame.quit()
client.close()