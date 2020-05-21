import select
import socket


class Server(object):

    def __init__(self, server_port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server_adress = ('0.0.0.0', server_port)
        self.server.bind(self.server_adress)
        self.server.listen(5)
        self.inputs = [self.server]

    def accept_client(self):
        connection, address = self.server.accept()
        print(str(address) + ' connected')
        connection.setblocking(0)
        self.inputs.append(connection)

    def readable_loop(self, readable):
        for request in readable:
                if request is self.server:
                    self.accept_client()
                else:
                    data = request.recv(1024)
                    if data:
                        print (data)

    def listen(self):
        while self.inputs:
            readable, _, exceptional = select.select(self.inputs, [], self.inputs)
            self.readable_loop(readable)
            for request in exceptional:
                self.inputs.remove(request)
                request.close()
                print(request + " disconnected")
