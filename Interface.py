from Const_params import *
from Discarded_Deck_Interface import Discarded_Deck_Interface
from Player_Handler import Player_Handler
from Deck_Interface import Deck_Interface
from InputBox import InputBox
from Nickname_Drawer import Nickname_Drawer
from Slider import Slider
from Client import Client
import socket
import sys
from threading import Thread

# parameters
FONT = 'Arial'
MAX_TXT_SIZE = 138
CLOSE = False
RUN = True
MUSIC = True
WIN_LOSE = False
WHO_WON = ''
DONE = False

# nickname parameters
nickname = ''
input_box = InputBox(25, 925, 400, 60, None, 70)
players_nickname_drawers = []

# card handler parameters
discarded_cards_handler = Discarded_Deck_Interface((150, 210), (
    screen.getScreen().get_width() * 0.4555, screen.getScreen().get_height() * 0.335))
deck_interface = Deck_Interface((150, 210),
                                (screen.getScreen().get_width() * 0.25, screen.getScreen().get_height() * 0.21))

players_handlers = []
# game music parameters
Volume = 0

# connection parameters
IP = '127.0.0.1'
PORT = 8080
ADDRESS = (IP, PORT)

# GAME parameters
IN_GAME = False
TURN = False
PICK_COLOR_TO_CHANGE = False
GAME_SCREEN = game_screen


def reaset_parameters():
    global IN_GAME, TURN, PICK_COLOR_TO_CHANGE, GAME_SCREEN, Volume, players_handlers, CLOSE

    CLOSE = False
    players_handlers = []
    IN_GAME = False
    TURN = False
    PICK_COLOR_TO_CHANGE = False
    GAME_SCREEN = game_screen
    discarded_cards_handler.set_last_card(None)
    Volume = 0


def create_dict_client_responses():
    return {'NEW_NICK_LIST': update_players, 'TOP_CARD': discarded_cards_handler.set_last_card,
            'TURN': identify_turn, 'SEND_CARDS': update_player_cards, 'WINNER': announce_winner, 'CHANGE_NICKNAME': change_nickname}


"""___________________________________________________________________________________________________________________________________"""


# In game information handlers functions
def client_in_game_info_handler(client):
    global IN_GAME, GAME_SCREEN, WIN_LOSE

    response_dict = create_dict_client_responses()

    while not CLOSE:
        try:
            msg = client.recieve()

            if msg == 'START_GAME':
                IN_GAME = True
            elif msg[0] in response_dict.keys():
                response_dict[msg[0]](msg[1])
        except:
            pass


def announce_winner(nick):
    global WIN_LOSE, WHO_WON

    WHO_WON = nick
    WIN_LOSE = True


def change_nickname(nick):
    global nickname

    nickname = nick


def get_nick_list():
    new_nick_list = []
    for p in players_handlers:
        new_nick_list.append(p.get_nickname())
    return new_nick_list


def create_client_handler():
    global players_handlers, players_nickname_drawers
    try:
        players_handlers.append(Player_Handler(nickname, 'me'))
    except:
        print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO DETERMINE MY CARD HANDLER")
    try:
        players_nickname_drawers.append(
            Nickname_Drawer(FONT, (868, 890), (310, 97), MAX_TXT_SIZE, nickname))
    except:
        print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO DETERMINE MY NICKNAME DRAWER")


def create_player_handler(nick, mode, location, surface_size):
    global players_handlers, players_nickname_drawers

    try:
        players_handlers.append(Player_Handler(nick, mode))
    except:
        print(f"[ERROR] AN ERROR OCCURRED WHILE TRYING TO DETERMINE {mode.upper()} CARD HANDLER")
    try:
        players_nickname_drawers.append(Nickname_Drawer(FONT, location, surface_size, MAX_TXT_SIZE, nick))
    except:
        print(f"[ERROR] AN ERROR OCCURRED WHILE TRYING TO DETERMINE {mode.upper()} NICKNAME DRAWER")


def update_players(nick_list):
    global players_handlers, players_nickname_drawers

    players_nickname_drawers = []
    players_handlers = []

    create_client_handler()
    nick_list.remove(nickname)
    if not nick_list:
        reaset_parameters()
    elif nick_list is not None:
        try:
            for i in range(len(nick_list)):
                if i == 0 and len(nick_list) == 1 or i == 1 and len(nick_list) > 1:
                    create_player_handler(nick_list[i], 'front', (131, 8), (189, 57))

                elif i == 0 and len(nick_list) > 1:
                    create_player_handler(nick_list[i], 'left side', (126, 827), (189, 57))

                elif i == 2 and len(nick_list) > 1:
                    create_player_handler(nick_list[i], 'right side', (1602, 8), (189, 57))

                else:
                    print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO ADD A PLAYER")
        except:
            print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO ADD PLAYERS")


def update_player_cards(info):
    for p in players_handlers:
        if p.get_nickname() == info[0]:
            p.set_cards_or_num_of_cards(info[1])


def identify_turn(nick):
    global TURN, GAME_SCREEN
    mode = ''
    for p in players_handlers:
        if p.get_nickname() == nick:
            mode = p.get_mode()
    if mode == 'me':
        TURN = True
        GAME_SCREEN = client_turn_screen
    elif mode == 'front':
        GAME_SCREEN = front_turn_screen
        TURN = False
    elif mode == 'left_side':
        TURN = False
        GAME_SCREEN = left_side_turn_screen
    elif mode == 'right_side':
        TURN = False
        GAME_SCREEN = right_side_turn_screen


def my_turn(client, px, py, event, click):
    global PICK_COLOR_TO_CHANGE
    try:
        if len(players_handlers) > 1:
            card_selected = players_handlers[0].client_button_check(px, py, event, click, TURN)
            take_card = deck_interface.game_handler(px, py, event, click)
            if card_selected is not False and card_selected is not None:
                client.send(('PLAY_TURN', (nickname, card_selected)))
                if card_selected == 'change_colorful':
                    PICK_COLOR_TO_CHANGE = True
                    discarded_cards_handler.set_last_card('choose_color')

            elif take_card is True and take_card is not None:
                client.send(('GIVE_CARD', nickname))
    except:
        pass


"""___________________________________________________________________________________________________________________________________"""


# game screen functions
def print_players_nicknames():
    if players_nickname_drawers is not None:
        for i in range(len(players_nickname_drawers)):
            try:
                players_nickname_drawers[i].draw(screen)
            except:
                print("[ERROR] AN ERROR OCCURRED WITH THE NICKNAME BLIT OF THE PLAYERS IN THE GAME SCREEN")


def blit_the_game_background(slider):
    if IN_GAME:
        for i in range(len(players_handlers)):
            try:
                players_handlers[i].player_cards_blit()
            except:
                print(
                    f"[ERROR] AN ERROR OCCURRED WITH THE CARD BLIT OF THE {players_handlers[i].get_nickname()} PLAYER")

        screen.blit(GAME_SCREEN, (0, 0))

    else:
        screen.blit(game_screen, (0, 0))
    slider.draw(screen.getScreen())

    print_players_nicknames()

    if IN_GAME:
        try:
            discarded_cards_handler.blit_discarded_deck()
        except:
            print("[ERROR] AN ERROR OCCURRED WITH THE DISCARDED CARDS HANDLER")

    try:
        deck_interface.blit()
    except:
        print("[ERROR] AN ERROR OCCURRED WITH THE DECK HANDLER")


def game_buttons_blit(slider, px, py):
    try:
        music_icon_blit(slider)

        if check_chat_button(px, py):
            screen.blit(chat_button, (0, 0))
        elif check_return_button_game_screen(px, py):
            screen.blit(return_button_game, (0, 0))
    except:
        print("[ERROR] AN ERROR OCCURRED WITH THE GAME SCREEN BUTTONS BLIT")


def game_screen_blit(slider):
    px, py = pygame.mouse.get_pos()
    # card bar first
    try:
        screen.blit(card_bar, (0, 0))
        # player card handler second
        blit_the_game_background(slider)
    except:
        pass
    game_buttons_blit(slider, px, py)


def game_event_handler(slider, event, click, px, py, client, hold_volume_slider):
    try:
        game_buttons_blit(slider, px, py)
        deck_interface.game_handler(px, py, event, click)
        my_turn(client, px, py, event, click)
        if hold_volume_slider:
            slider.handle_event(screen.getScreen(), px)
    except:
        print("[ERROR] AN ERROR OCCURRED WITH EVENT HANDLER OF THE GAME")


def game_broad(client):
    global CLOSE, DONE

    t = Thread(target=client_in_game_info_handler, args=(client,))
    start_thread = True

    slider = Slider(140, 942, 140, 8)
    DONE = True

    hold_volume_slider = False
    music_loader('music\\Game_background_music.mp3', -1, Volume)

    while DONE:
        if start_thread:
            t.start()
            start_thread = False
        game_screen_blit(slider)
        if WIN_LOSE:
            if WHO_WON == nickname:
                win_screen()
            else:
                lose_screen()
        for event in pygame.event.get():

            game_music(slider)
            px, py = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            game_event_handler(slider, event, click, px, py, client, hold_volume_slider)

            if event.type == pygame.QUIT:
                CLOSE = True
                return 'exit'
            elif event.type == pygame.MOUSEBUTTONDOWN and click[0] == 1:
                if PICK_COLOR_TO_CHANGE:
                    check_change_color(px, py, client)
                if slider.on_slider(px, py) and slider.on_slider_hold(px, py):
                    hold_volume_slider = True
                try:
                    if check_chat_button(px, py):
                        buttons_s.play()
                    elif check_return_button_game_screen(px, py):
                        buttons_s.play()
                        CLOSE = True
                        DONE = False
                except:
                    print('An error occurred with the events handler at the game broad')

            elif event.type == pygame.MOUSEBUTTONUP:
                hold_volume_slider = False

        screen.update()


"""___________________________________________________________________________________________________________________________________"""


# input box handler function
def input_box_handler(e, mouse_click):
    try:
        global nickname

        input_box.handle_event_save(e, mouse_click, screen)
        input_box.draw(screen.getScreen())
        input_box.update()

        if input_box.getActive():
            screen.blit(nickname_clicked, (0, 0))
            nickname = input_box.getText()
    except:
        print("[ERROR] AN ERROR OCCURRED WITH THE INPUT BOX HANDLER")


# buttons function
def check_chat_button(px, py):
    if 1672 < px < 1760 and 900 < py < 985 or 1690 < px < 1720 and 980 < py < 995 and (px - 1690) * (
            px - 980) / 2 > 0:
        return True
    return False


def check_return_button_game_screen(px, py):
    if 1805 < px < 1890 and 910 < py < 990 or 1788 < px < 1837 and 896 < py < 955 and (py - 896) * (
            px - 1788) / 2 > 0:
        return True
    return False


def music_icon_blit(slider):
    if slider.get_volume() == 0:
        screen.blit(muted_vol, (0, 0))
    elif 80 <= slider.get_volume() <= 100:
        screen.blit(high_vol, (0, 0))
    elif 50 <= slider.get_volume() < 80:
        screen.blit(med_vol, (0, 0))
    else:
        screen.blit(low_vol, (0, 0))


def check_return_button__rules_screen(px, py):
    if 1770 < px < 1890 and 32 < py < 138:
        return True
    return False


def check_music_button(px, py):
    if 86 < px < 239 and 24 < py < 174:
        return True
    return False


def check_start_button(px, py):
    if 774 < px < 1085 and 460 < py < 530:
        return True
    return False


def check_how_to_play_button(px, py):
    if 581 < px < 1280 and 595 < py < 662:
        return True
    return False


def check_exit_button(px, py):
    if 823 < px < 1035 and 740 < py < 810:
        return True
    return False


def check_change_color(px, py, client):
    global PICK_COLOR_TO_CHANGE
    if int(screen.getScreen().get_width() * 0.4555) < px < int(screen.getScreen().get_width() * 0.4555) + 75:
        if int(screen.getScreen().get_height() * 0.335) < py < int(screen.getScreen().get_height() * 0.335) + 105:
            PICK_COLOR_TO_CHANGE = False
            client.send('red')
        elif int(screen.getScreen().get_height() * 0.335) + 105 < py < int(
                screen.getScreen().get_height() * 0.335) + 210:
            PICK_COLOR_TO_CHANGE = False
            client.send('blue')
    elif int(screen.getScreen().get_width() * 0.4555) + 75 < px < int(screen.getScreen().get_width() * 0.4555) + 150:
        if int(screen.getScreen().get_height() * 0.335) < py < int(screen.getScreen().get_height() * 0.335) + 105:
            PICK_COLOR_TO_CHANGE = False
            client.send('yellow')
        elif int(screen.getScreen().get_height() * 0.335) + 105 < py < int(
                screen.getScreen().get_height() * 0.335) + 210:
            PICK_COLOR_TO_CHANGE = False
            client.send('green')


def check_win_lose_exit_button(px, py):
    if 37 < px < 240 and 893 < py < 975:
        return True
    return False


def check_play_again_button(px, py):
    if 1402 < px < 1891 and 896 < py < 975:
        return True
    return False


"""___________________________________________________________________________________________________________________________________"""


# music functions
def game_music(slider):
    global Volume

    if slider.get_volume() != Volume:
        Volume = slider.get_volume()
        mixer.music.set_volume(Volume * 0.0025)


def music_loader(file, number, volume):
    mixer.music.unload()
    mixer.music.set_volume(volume)
    mixer.music.load(file)
    mixer.music.play(number)


def music_turn_off_on():
    global MUSIC
    if MUSIC:
        MUSIC = False
        mixer.music.pause()

    else:
        MUSIC = True
        mixer.music.unpause()


"""___________________________________________________________________________________________________________________________________"""


# rules screen functions
def how_to_play_screen():
    global MUSIC
    Done = True
    while Done:
        # events
        rules_screen_blit()
        try:
            for e in pygame.event.get():
                px, py = pygame.mouse.get_pos()
                left_click = pygame.mouse.get_pressed()

                if e.type == pygame.QUIT:
                    return 'exit'

                elif e.type == pygame.MOUSEBUTTONDOWN and left_click[0] == 1:
                    if check_return_button__rules_screen(px, py):  # return button
                        buttons_s.play()
                        Done = False

                    elif check_music_button(px, py):  # music buttons
                        buttons_s.play()
                        music_turn_off_on()

                screen.update()
        except:
            print("[ERROR] AN ERROR OCCURRED WITH THE EVENT HANDLER OF THE RULES SCREEN")


def rules_screen_blit():
    px, py = pygame.mouse.get_pos()
    try:
        screen.blit(rules_screen, (0, 0))

        if MUSIC:
            screen.blit(music_on_main_button, (0, 0))

        else:
            screen.blit(music_off_main_button, (0, 0))

        if check_return_button__rules_screen(px, py):
            screen.blit(return_button_rules, (0, 0))

        elif check_music_button(px, py):

            if MUSIC:
                screen.blit(bold_music_on_main_button, (0, 0))

            else:
                screen.blit(bold_music_off_main_button, (0, 0))
    except:
        print("[ERROR] AN ERROR OCCURRED WITH THE RULES SCREEN BUTTONS")


"""___________________________________________________________________________________________________________________________________"""


# OPEN CONNECTION WITH THE SERVER
def open_game_broad():
    global RUN, players_nickname_drawers, players_handlers
    try:
        client = Client(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        client.connect(ADDRESS)

        client.send('FIND_GAME')
        if client.recieve() == 'NICK':

            client.send(input_box.getText())
            mixer.music.fadeout(880)

            if game_broad(client) == 'exit':
                client.close_connection()
                RUN = False

            else:
                client.close_connection()
                music_loader('Music\\Client_background_Music.mp3', -1, 0.11)  # 0.11
                reaset_parameters()
                try:
                    players_nickname_drawers = []
                except Exception as error_code:
                    print(error_code)
    except:
        print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO GET TO THE MAIN SCREEN")


# main screen functions
def main_screen_event_handler(px, py):
    global RUN, players_handlers, players_nickname_drawers
    if check_start_button(px, py):
        buttons_s.play()

        if input_box.getText() != '':
            open_game_broad()

    elif check_how_to_play_button(px, py):
        buttons_s.play()

        

        if how_to_play_screen() == 'exit':
            RUN = False

    elif check_exit_button(px, py):  # exit button
        buttons_s.play()
        RUN = False

    elif check_music_button(px, py):
        buttons_s.play()
        music_turn_off_on()


def main_screen():
    global RUN, MUSIC
    # music
    music_loader('Music\\Client_background_Music.mp3', -1, 0.11)  # volume = 0.11
    while RUN:
        main_screen_blit()
        # events
        try:
            for event in pygame.event.get():
                px, py = pygame.mouse.get_pos()
                # buttons
                # other events
                click = pygame.mouse.get_pressed()

                if event.type == pygame.QUIT:
                    RUN = False

                # nickname input box
                input_box_handler(event, click)

                if event.type == pygame.MOUSEBUTTONDOWN and click[0] == 1:
                    main_screen_event_handler(px, py)
                screen.update()
        except:
            print("[ERROR] AN ERROR OCCURRED WITH THE EVENT HANDLER OF THE MAIN SCREEN")

    pygame.quit()
    sys.exit()


def main_screen_blit():
    px, py = pygame.mouse.get_pos()
    try:
        screen.blit(menu, (0, 0))
        screen.blit(screen.update_fps(pygame.font.SysFont("Arial", 45)), (1874, 0))

        if MUSIC:
            screen.blit(music_on_main_button, (0, 0))

        else:
            screen.blit(music_off_main_button, (0, 0))

        if check_start_button(px, py):
            screen.blit(bold_start_button, (0, 0))

        elif check_how_to_play_button(px, py):
            screen.blit(how_to_play_button, (0, 0))

        elif check_exit_button(px, py):
            screen.blit(exit_button, (0, 0))

        elif check_music_button(px, py):

            if MUSIC:
                screen.blit(bold_music_on_main_button, (0, 0))

            else:
                screen.blit(bold_music_off_main_button, (0, 0))
    except:
        print("[ERROR] AN ERROR OCCURRED WITH THE MAIN SCREEN BUTTONS")


"""___________________________________________________________________________________________________________________________________"""


def win_lose_buttons_screen(background):
    px, py = pygame.mouse.get_pos()
    try:
        screen.blit(background, (0, 0))
        screen.blit(screen.update_fps(pygame.font.SysFont("Arial", 45)), (1874, 0))

        if MUSIC:
            screen.blit(music_on_main_button, (0, 0))

        else:
            screen.blit(music_off_main_button, (0, 0))

        if check_win_lose_exit_button(px, py):  # sss
            screen.blit(exit_button_win_lose_screen, (0, 0))

        elif check_play_again_button(px, py):  # sss
            screen.blit(play_again_button_win_lose_screen, (0, 0))

        elif check_music_button(px, py):
            if MUSIC:
                screen.blit(bold_music_on_main_button, (0, 0))

            else:
                screen.blit(bold_music_off_main_button, (0, 0))
    except:
        print("[ERROR] AN ERROR OCCURRED WITH THE MAIN SCREEN BUTTONS")


def win_lose_event_handler(px, py):
    global RUN, WIN_LOSE, DONE

    if check_play_again_button(px, py):
        buttons_s.play()
        WIN_LOSE = False
        DONE = False

    elif check_win_lose_exit_button(px, py):  # exit button
        buttons_s.play()
        RUN = False
        WIN_LOSE = False
        DONE = False

    elif check_music_button(px, py):
        buttons_s.play()
        music_turn_off_on()


def nick_organizer():
    global WHO_WON

    nick = WHO_WON + ' WIN'
    size = 190
    size -= int(7.6 * len(nick))
    screen.draw_text(nick, (0, 0, 0), 'fonts\\Reglisse.otf', size, 695, 614)


def lose_screen():
    global RUN, WIN_LOSE, DONE

    music_loader('Music\\Client_background_Music.mp3', -1, 0)  # volume = 0.11

    while WIN_LOSE:
        # buttons
        win_lose_buttons_screen(lose_screen_background)
        nick_organizer()
        #  events
        try:
            for event in pygame.event.get():
                px, py = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                # other events
                if event.type == pygame.QUIT:
                    RUN = False
                    WIN_LOSE = False
                    DONE = False

                if event.type == pygame.MOUSEBUTTONDOWN and click[0] == 1:
                    win_lose_event_handler(px, py)

                screen.update()
        except:
            print("[ERROR] AN ERROR OCCURRED WITH THE EVENT HANDLER OF THE LOSE SCREEN")


def win_screen():
    global RUN, WIN_LOSE, DONE

    music_loader('Music\\Client_background_Music.mp3', -1, 0)  # volume = 0.11

    while WIN_LOSE:
        # buttons
        win_lose_buttons_screen(win_screen_background)
        #  events
        try:
            for event in pygame.event.get():
                px, py = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                # other events
                if event.type == pygame.QUIT:
                    RUN = False
                    DONE = False
                    WIN_LOSE = False

                if event.type == pygame.MOUSEBUTTONDOWN and click[0] == 1:
                    win_lose_event_handler(px, py)

                screen.update()
        except:
            print("[ERROR] AN ERROR OCCURRED WITH THE EVENT HANDLER OF THE WIN SCREEN")


