from constants import *
import json


def connect(pocket):
    pocket.connect((server_ip, server_port))
    data = str(pocket.recv(1024))
    color = data[10]
    return color


def send_move(pocket, move):
    pocket.send(json.dumps(move).encode())


def get_move(pocket):
    move = pocket.recv(1024)
    return json.loads(move)
