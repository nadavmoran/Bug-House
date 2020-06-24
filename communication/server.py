import select
import socket
import json
import chess


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

    def accept_client(self):#accepts a client
        connection, address = self.server.accept()
        print(str(address) + ' connected')
        connection.setblocking(0)
        self.inputs.append(connection)
        color = 'white' if self.counter % 2 == 0 else 'black'
        self.players[connection] = self.counter
        self.send(connection, 'you are ' + color)
        self.counter += 1
        self.matched_start()

    def matched_start(self):#starts the game at the same moment for all the players
        if self.counter == 4:
            for player in self.players:
                self.send(player, 'game started')

    def publish_move(self, move, client):#publishes a move for all the players
        client_num = self.players[client]
        for i in self.players:
            message = move.copy()
            player_num = self.players[i]
            if (client_num > 1 and player_num > 1) or (client_num <= 1 and player_num <= 1):
                message.append(True)
            else:
                message.append(False)
            if (player_num % 2 == 1 and message[-1]) or (player_num % 2 == 0 and not message[-1]):
                message[0] = message[0][::-1]
            self.send(i, json.dumps(message))


    def publish(self, transplant, client):#publishes a capture and a transplant
        client_num = self.players[client]
        for i in self.players:
            message = transplant.copy()
            player_num = self.players[i]
            if client_num == player_num or player_num + client_num == 3:
                message.append(False)
            else:
                message.append(True)
            if (client_num > 1 and player_num > 1) or (client_num <= 1 and player_num <= 1):
                message.append('c' not in message[1])
            else:
                message.append('c' in message[1])
            if (client_num > 1 and player_num > 1) or (client_num <= 1 and player_num <= 1):
                message.append(True)
            else:
                message.append(False)
            if (player_num % 2 == 1 and message[-1]) or (player_num % 2 == 0 and not message[-1]):
                message[0] = message[0][::-1]
            print(client_num, player_num)
            print(message[-2], message[-1])
            self.send(i, json.dumps(message))


    def send(self, client, data):#sends data to the server
        try:
            client.send(data.encode())
        except:
            client.close()


    def readable_loop(self):#runs on the readable list
        for client in self.readable:
            if client is self.server:
                self.accept_client()
            else:
                try:
                    data = client.recv(1024)
                except:
                    data = None
                    self.inputs.remove(client)
                    client.close()
                if data:
                    data = json.loads(data)
                    print(data[0])
                    if data[1] == 'm':
                        self.publish_move(data, client)
                    else:
                        self.publish(data, client)


    def listen(self):#The main loop
        while self.inputs:
            self.readable, _, exceptional = select.select(self.inputs, [], self.inputs)
            self.readable_loop()
            for client in exceptional:
                self.inputs.remove(client)
                client.close()
                print(client + " disconnected")


s = Server(4320)
s.listen()
