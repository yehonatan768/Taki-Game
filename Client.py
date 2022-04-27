import pickle

class Client(object):

    # Constructor

    def __init__(self, client, address=None):
        self.client = client
        self.nickname = ''
        self.lobby = None
        if address is not None:
            self.address = address

    # Data handler functions

    def send(self, data):
        try:
            try:
                msg = pickle.dumps(data)
                self.client.send(msg)
            except:
                print("[ERROR] An error occurred while trying to 'send'")
        except:
            pass

    def recieve(self):
        try:
            try:
                data = pickle.loads(self.client.recv(1024))
                return data
            except:
                pass
        except:
            print("[ERROR] An error occurred while trying to 'recieve'")

    # Get and Set functions
    def set_Client(self, client):
        self.client = client

    def set_Nickname(self, new_nickname):
        self.nickname = new_nickname

    def set_lobby(self, lobby):
        self.lobby = lobby

    def get_lobby(self):
        return self.lobby

    def get_Nickname(self):
        return self.nickname

    def get_Client(self):
        return self.client

    def get_Address(self):
        return self.address

    def get_in_game(self):
        return True if self.lobby is not None else False

    # Connection handler functions

    def close_connection(self):
        try:
            self.send('DISCONNECT')
            message = self.recieve()
            if message == 'DISCONNECTED':
                self.close()
        except:
            print("An error occurred with disconnection from the server")

    def connect(self, address):
        self.client.connect(address)

    def close(self):
        self.client.close()