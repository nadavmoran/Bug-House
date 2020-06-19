from constants import *
import json


def connect(socket):
    socket.connect((server_ip, server_port))
    data = str(socket.recv(1024))
    color = data[10]
    return color


def send_move(socket, move):
    socket.send(json.dumps(move).encode())


def get_move(socket):
    move = socket.recv(1024)
    return json.loads(move)