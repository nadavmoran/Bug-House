from constants import *
import json


def connect(socket):
    '''
    connects to the server
    :param socket:
    a socket object that connects to the server
    :return:
    the color the of the player
    '''
    socket.connect((server_ip, server_port))
    data = str(socket.recv(1024))
    socket.recv(1024)
    socket.settimeout(0.01)
    color = data[10]
    return color


def send_move(socket, move):
    '''
    sends a move to the server
    :param socket:
    a socket object that connects to the server
    :param move:
    data need to be sent
    :return:
    '''
    try:
        socket.send(json.dumps(move).encode())
    except:
        socket.close()
        return True
    return False


def get_move(socket):
    '''
    gets a move from the server
    :param socket:
    a socket object
    :return:
    '''
    try:
        move = socket.recv(1024)
    except:
        return None
    if move:
        return load_string(move)
    return None

def load_string(data):
    '''
    gets a data and decode it
    :param data:
    encoded lists of data
    :return:
    a list of lists of the data needed
    '''
    text = ''
    string = data.decode()
    string = ''.join(('[', string, ']'))
    for i in range(len(string) - 2):
        text += string[i]
        if string[i] == ']' and string[i + 1] != ',':
            text +=','
    text += ']]'
    return json.loads(text)