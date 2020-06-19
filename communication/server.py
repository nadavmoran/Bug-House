import select
import socket
import json


class Server(object):

    def __init__(self, server_port):
        self.counter = 0
        self.players = {}
        self.readable = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server_address = ('0.0.0.0', server_port)
        self.server.bind(self.server_address)
        self.server.listen(4)
        self.inputs = [self.server]

    def accept_client(self):
        connection, address = self.server.accept()
        print(str(address) + ' connected')
        connection.setblocking(0)
        self.inputs.append(connection)
        color = 'white' if self.counter % 2 == 0 else 'black'
        self.counter += 1
        connection.send(('you are ' + color).encode())
        self.players[connection] = color

    def publish_move(self, move, client):
        client_num = self.players[client]
        for i in self.players:
            if i != client:
                message = move.copy()
                if (client_num > 1 and self.players[i] > 1) or (client_num <= 1 and self.players[i] <= 1):
                    message.append(True)
                else:
                    message.append(False)
                i.send(json.dumps(message).encode())

    def publish_transplant(self, transplant, client):
        client_num = self.players[client]
        for i in self.players:
            if i != client:
                message = transplant.copy()
                if client_num % 2 == self.players[i] % 2:
                    message.append('down')
                else:
                    message.append('up')
                if (client_num > 1 and self.players[i] > 1) or (client_num <= 1 and self.players[i] <= 1):
                    message.append('secondary')
                else:
                    message.append('main')
                i.send(json.dumps(message).encode())

    def readable_loop(self):
        for client in self.readable:
            if client is self.server:
                self.accept_client()
            else:
                data = client.recv(1024)
                if data:
                    data = json.loads(data)
                    if data[0] == 'm':
                        self.publish_move(data, client)
                    else:
                        self.publish_transplant(data, client)

    def listen(self):
        while self.inputs:
            self.readable, _, exceptional = select.select(self.inputs, [], self.inputs)
            self.readable_loop()
            for client in exceptional:
                self.inputs.remove(client)
                client.close()
                print(client + " disconnected")


s = Server(4320)
s.listen()
