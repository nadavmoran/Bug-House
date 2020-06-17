import select
import socket


class Server(object):

    def __init__(self, server_port):
        self.counter = 0
        self.players = {}
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

    def readable_loop(self):
        for client in self.readable:
            if client is self.server:
                self.accept_client()
            else:
                data = client.recv(1024)
                if data:
                    for i in self.players:
                        if i != client:
                            i.send(data)

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
