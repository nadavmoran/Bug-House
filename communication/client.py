from constants import *
import json


def connect(socket):#connects to the server
    socket.connect((server_ip, server_port))
    data = str(socket.recv(1024))
    socket.recv(1024)
    socket.settimeout(0.01)
    color = data[10]
    return color


def send_move(socket, move):#sends a move to the server
    try:
        socket.send(json.dumps(move).encode())
    except:
        socket.close()
        return True
    return False


def get_move(socket):#gets a move from the server
    try:
        move = socket.recv(1024)
    except:
        return None
    if move:
        return load_string(move)
    return None

def load_string(data):
    string = text = ''
    string = data.decode()
    string = ''.join(('[', string, ']'))
    for i in range(len(string) - 2):
        text += string[i]
        if string[i] == ']' and string[i + 1] != ',':
            text +=','
    text += ']]'
    return json.loads(text)