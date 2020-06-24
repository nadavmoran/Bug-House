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
    prev_pos_logic = [0, 0]
    tool = None
    transplant_tool = None
    legal = False
    enemy_move = []
    fix_row, fix_col = 0, 0
    if color == white:
        fix_row = 7
    else:
        fix_col = 7
    while not stop:#the main loop
        enemy_move = get_move(client)#gets the other players moves from the server
        if enemy_move:
            for i in enemy_move:
                if i[board_side_index]:
                    map = chess.Board(i[board_fen_index])
                    board = set_board_while_game(i[string_board_index], i[board_side_index])
                else:
                    set_board_while_game(i[string_board_index], i[board_side_index])
                if 't' in i[move_type_index]:
                    if i[transplant_board_side_index] and not i[pocket_side_index]:
                        my_pocket = chess.variant.CrazyhousePocket(i[pocket_index])
                        transplant_pieces = set_pocket_while_game(i[pocket_index],
                                                                  i[transplant_board_side_index],
                                                                  i[pocket_side_index],
                                                                  i[taken_piece_color_index])
                    elif not i[transplant_board_side_index] and not i[pocket_side_index]:
                        other_pocket = chess.variant.CrazyhousePocket(i[pocket_index])
                    set_pocket_while_game(i[pocket_index],
                                          i[transplant_board_side_index],
                                          i[pocket_side_index],
                                          i[taken_piece_color_index])
        for event in pygame.event.get():#runs on the pygame events
            if event.type == QUIT:
                stop = True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:#close the program if the player clicks on the close button
                piece, x, y = get_square_under_mouse(board, start_pos[:])
                transplant_piece, index = get_transplant_piece_under_mouse(transplant_pieces, transplant_start_pos[:])
                if not moving and not transplant_moving and piece != None and piece.rect.collidepoint(
                        event.pos) and piece.color == color:#checks if a player clicks on a piece in the board
                    moving = True
                    prev_pos_logic = [x, y]
                    tool = piece
                    pygame.draw.rect(game_display, blue, piece.rect, 1)
                elif moving:#sets a move if its legal
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
                            else:
                                tmp = str(map) if color == white else str(map)[::-1]
                                board = set_board_while_game(tmp, True)
                                stop = send_move(client, [str(map), 'm', map.fen()])
                        else:
                            pygame.draw.rect(game_display, black, tool.rect, 1)
                        moving = False
                elif not transplant_moving and transplant_piece != None and transplant_piece.rect.collidepoint(event.pos):#checks if a player clicks on a piece in the pocket
                    transplant_tool = transplant_piece
                    pygame.draw.rect(game_display, blue, transplant_piece.rect, 1)
                    transplant_moving = True
                elif transplant_moving:#sets a transplant if its legal
                    if str(type(transplant_tool)) == "<class 'pieces.chess_pieces.Pawn'>" and (y == 0 or y == 7):
                        break
                    if x != None and y != None and piece == None and map.turn == (True if color == white else False):
                        legal = is_transplant_legal(map, my_pocket, chess.square(abs(fix_col - x), abs(fix_row - y)), transplant_tool.__str__(),)
                        print(legal)
                        if legal:
                            tmp = str(map) if color == white else str(map)[::-1]
                            board = set_board_while_game(tmp, True)
                            stop = send_move(client, [str(map), 't', map.fen(), str(my_pocket), transplant_tool.color])
                    elif transplant_piece == transplant_tool:
                        pygame.draw.rect(game_display, white, transplant_piece.rect, 1)
                    transplant_moving = False
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