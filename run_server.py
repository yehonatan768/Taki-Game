from Server import *


def main_server():
    print(
        "                TAKI MAIN SERVER IS ACTIVE                  \n                  SEARCHING FOR PLAYERS...                  "
        "\n\n")

    # accepting connection thread

    server.listen()
    clients_conn = Thread(target=server.accept_connections, args=())
    clients_conn.start()

    close_games = Thread(target=server.close_lobby, args=())
    close_games.start()

    game_activator = Thread(target=server.game_activator, args=())
    game_activator.start()

    clients_conn.join()
    close_games.join()
    game_activator.join()


if __name__ == '__main__':
    main_server()
