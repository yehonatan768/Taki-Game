import time
from Player import Player
from Client import Client
from Game import Game
from threading import Thread
import socket


IP = '127.0.0.1'
PORT = 8080


class Server(object):
    # Constructor

    def __init__(self, address):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.server.bind(address)

        self.clients = []
        self.clients_threads = []
        self.lobby_list = []
        self.lobby_index_thread = []

        self.active_connections = 0
        self.lobby_count = 0

    # Data handler functions
    @staticmethod
    def recieve(client):
        try:
            try:
                return client.recieve()
            except:
                print('client error at getting the message')
        except:
            pass

    @staticmethod
    def send(client, message):
        try:
            try:
                client.send(message)
            except:
                print('An error at sending the message')
        except:
            pass

    def handle_client(self, client):
        while True:
            try:
                message = ''
                try:
                    message = self.recieve(client)
                except:
                    pass

                if 'DISCONNECT' == message:
                    self.send(client, "DISCONNECTED")
                    break

                elif "FIND_GAME" == message:
                    nickname = ''
                    try:
                        self.send(client, 'NICK')
                        nickname = self.recieve(client)
                        client.set_Nickname(nickname)

                        self.enter_lobby(client, nickname)
                    except:
                        print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO JOIN A GAME")

                elif client.get_in_game():
                    if 'GIVE_CARD' == message[0] or message[
                        0] == 'PLAY_TURN' or message == 'yellow' or message == 'red' or message == 'blue' or message == 'green':
                        try:
                            self.lobby_list[client.get_lobby()].set_info(message)
                        except Exception as er:
                            print('new function problem, type: ' + str(er))

            except:
                break

        self.quit_progress(client)

    # Get and Set functions
    def get_Address(self):
        return self.address

    # broadcast info to players functions
    def broadcast_info_players(self, index, request):
        for player in self.lobby_list[index].get_players():
            try:
                player.get_client().send(request)
            except:
                print('[ERROR] AN ERROR OCCURRED WHILE TRYING TO SEND INFO TO ' + (player.get_nickname()).upper())

    def broadcast_cards(self, lobby_index, nickname, request):
        for player in self.lobby_list[lobby_index].get_players():
            if player.get_nickname() == nickname:
                player.send(request)
            else:
                player.send((request[0], (request[1][0], len(request[1][1]))))

    def send_lobby_nicknames(self, lobby):
        try:
            players = lobby.get_players()

            if players is not None:
                for player in players:
                    try:
                        self.send(player.get_client(),
                                  ('NEW_NICK_LIST', self.get_nickname_list(self.lobby_list.index(lobby))))
                    except:
                        print(
                            f'[ERROR] AN ERROR OCCURRED WHILE TRYING TO SEND NICKNAME LIST TO: [{player.get_client().get_Address()[0]}:{player.get_client().get_Address()[1]}]')
            else:
                return None
        except:
            print(
                f'[ERROR] AN ERROR OCCURRED WHILE TRYING TO STREAM THE NICKNAME LIST OF LOBBY: {self.lobby_list.index(lobby)}')

    def get_nickname_list(self, lobby_index):
        players = self.lobby_list[lobby_index].get_players()
        nick_l = []
        for player in players:
            nick_l.append(player.get_nickname())
        return nick_l

    def game_info_handler(self, lobby_thread_index):
        index = self.lobby_index_thread[lobby_thread_index][1]
        try:
            while self.lobby_list[index].get_is_active() and self.lobby_list[index].get_players() is not None:
                try:
                    request = self.lobby_list[index].get_request()
                    if request is not None:
                        # need to divide the requests to groups like send cards and num of cards or send top card
                        if request[0] == 'SEND_CARDS':
                            self.broadcast_cards(index, request[1][0], request)
                            self.lobby_list[index].set_request(None)

                        elif request[0] == 'WINNER' or 'TURN' or 'TOP_CARD':
                            self.broadcast_info_players(index, request)
                            self.lobby_list[index].set_request(None)
                        elif request == 'START_GAME' or 'END_GAME':
                            self.broadcast_info_players(index, request)
                            self.lobby_list[index].set_request(None)
                        else:
                            print('AN VALID REQUEST')
                except:
                    pass
                index = self.lobby_index_thread[lobby_thread_index][1]
        except:
            pass

    # lobby handlers functions

    def create_new_lobby(self, client, nickname):
        try:
            client.set_lobby(self.lobby_count)
            self.lobby_count += 1
            self.lobby_list.append(Game(Player(client, nickname)))
            print(f"[NEW LOBBY] A NEW LOBBY HAS BEEN FORMED | Lobby {self.lobby_count}")
            self.send_lobby_nicknames(self.lobby_list[self.lobby_count - 1])
        except:
            print('[ERROR] AN ERROR OCCURRED WILE TRYING TO FORM A NEW LOBBY')

    def enter_lobby(self, client, nickname):
        try:
            if self.lobby_count == 0:
                self.create_new_lobby(client, nickname)
                return None
            else:
                for lobby in self.lobby_list:
                    if not lobby.get_is_full():
                        client.set_lobby(self.lobby_list.index(lobby))
                        if nickname in lobby.get_players_nickname_list():
                            i = 1
                            new_nick = nickname + str(i)
                            while new_nick in lobby.get_players_nickname_list():
                                i += 1
                                new_nick = nickname + str(i)
                            nickname = new_nick
                            self.send(client, ('CHANGE_NICKNAME', nickname))
                            time.sleep(2)

                        print(
                            f'[JOINED LOBBY]: PLAYER: {nickname} HAS ENTERED A ROOM | ROOM {self.lobby_list.index(lobby) + 1}')
                        lobby.add_player(Player(client, nickname))
                        self.send_lobby_nicknames(lobby)
                        return None
                self.create_new_lobby(client, nickname)
                return None
        except:
            print('[ERROR] AN ERROR OCCURRED WHILE CLIENT TRIED TO ENTER TO A LOBBY')

    def leave_lobby(self, client):
        lobby = client.get_lobby() - 1
        self.lobby_list[lobby].remove_player(client)
        self.send_lobby_nicknames(self.lobby_list[lobby])

    def find_lobby_thread(self, index):
        for l in self.lobby_index_thread:
            if l[1] == index:
                return self.lobby_index_thread.index(l)

    def close_lobby(self):
        while True:
            try:
                for lobby in self.lobby_list:
                    if lobby.get_players() is None:
                        index = self.lobby_list.index(lobby)
                        self.lobby_list.remove(lobby)

                        print(f"\n[LOBBY CLOSED] lobby {index + 1} has been closed | Lobby {self.lobby_count}")
                        self.lobby_count -= 1
                        for _lobby in self.lobby_list:
                            if index < self.lobby_list.index(_lobby):
                                i = self.lobby_list.index(_lobby)
                                for player in _lobby.get_players():
                                    player.get_client().set_lobby(i - 1)
                                    c = self.clients.index(player.get_client())
                                    self.clients[c].set_lobby(i - 1)

                        for _lobby in self.lobby_index_thread:
                            if self.find_lobby_thread(index) < _lobby[1]:
                                _lobby[1] -= 1
                        for _lobby in self.lobby_index_thread:
                            if self.find_lobby_thread(index) == _lobby[1]:
                                self.lobby_index_thread.remove(_lobby)
                                break
            except:
                pass

    def game_activator(self):
        while True:
            for lobby in self.lobby_list:
                if lobby.get_is_full() == True and lobby.get_is_active() == False:
                    index = self.lobby_list.index(lobby)
                    self.lobby_list[index].set_is_active()
                    t = Thread(target=self.game_info_handler, args=(len(self.lobby_index_thread),))
                    self.lobby_index_thread.append((t, index))
                    print(f'[GAME ROOM] A NEW GAME HAS BEEN ACTIVATED | Room {index + 1}')
                    t.start()

    # connection functions
    def accept_connections(self):
        for c in self.clients:
            c.close()
        del self.clients[:]
        while True:
            try:
                # client connection
                client, address = self.server.accept()
                self.clients.append(Client(client, address))
                self.active_connections += 1
                print(
                    f"[NEW CONNECTION] CONNECTION HAS BEEN ESTABLISH WITH: [{str(address[0])}:{str(address[1])}] | CONNECTION STATUS: Stable | ACTIVE CONNECTIONS: {self.active_connections} ")
                # thread operation
                try:
                    t = Thread(target=self.handle_client, args=(self.clients[len(self.clients) - 1],))
                    t.start()
                    self.clients_threads.append(t)
                except:
                    print("[NEW CONNECTION] AN ERROR OCCURRED WITH THE THREAD OF THE CLIENT HANDLER")
            except:
                print("[ERROR] AN ERROR OCCURRED WITH THE ACCEPT CONNECTIONS")

    def quit_progress(self, client):
        index = self.clients.index(client)
        self.leave_lobby(client)
        self.active_connections -= 1
        print(
            f"[CONNECTION CLOSED] CONNECTION STATUS OF: [{str(client.get_Address()[0])}:{str(client.get_Address()[1])}] HAS BEEN CHANGED| CONNECTION STATUS: Disconnected | ACTIVE CONNECTIONS: {self.active_connections} ")
        client.close()
        self.clients.remove(client)
        self.clients_threads.remove(self.clients_threads[index])

    def listen(self):
        self.server.listen()

    def close(self):
        self.server.close()


ADDRESS = (IP, PORT)
server = Server(ADDRESS)
