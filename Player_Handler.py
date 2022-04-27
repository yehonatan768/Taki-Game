from Other_Players_Card_Handler import Other_Players_Card_Handler
from Client_Cards_Handler import Client_Cards_Handler
from Const_params import *


class Player_Handler(object):
    def __init__(self, nickname, mode):
        self.nickname = nickname
        self.mode = mode

        self.card_handler = None
        self.nickname_drawer = None
        self.cards = None
        self.num_of_cards = None

        self.player_card_handler()

    def client_button_check(self, mouse_position_x, mouse_position_y, event, click, turn):
        card_button = self.card_handler.card_button_handler(mouse_position_x, mouse_position_y, event, click, turn)
        return card_button

    def player_card_handler(self):
        if self.mode == 'front':
            self.card_handler = Other_Players_Card_Handler((110, 160), 70, 180,
                                                           (screen.getScreen().get_width() * 0.4765,
                                                            screen.getScreen().get_height() * 0), 'front')
        elif self.mode == 'right side':
            self.card_handler = Other_Players_Card_Handler((110, 170), 70, 270,
                                                           (0, screen.getScreen().get_height() * 0.3765), 'right side')
        elif self.mode == 'left side':
            self.card_handler = Other_Players_Card_Handler((110, 170), 70, 90, (screen.getScreen().get_width() * 0.92,
                                                                                screen.getScreen().get_height() * 0.3765),
                                                           'left side')
        elif self.mode == 'me':
            self.card_handler = Client_Cards_Handler((150, 210), 100, 0)

    def player_cards_blit(self, mouse_position_x=None, mouse_position_y=None):
        try:
            if self.mode == 'me':
                try:
                    self.card_handler.game_handler(mouse_position_x, mouse_position_y)
                except:
                    print('[ERROR] AN ERROR OCCURRED WITH ONE OF THE CLIENT CARD HANDLER')

            elif self.mode == 'front' or 'right side' or 'left side':
                try:
                    self.card_handler.card_handler()
                except:
                    print('1111111111111111111')
        except:
            print('[ERROR] AN ERROR OCCURRED WHILE TRYING TO BLIT THE CARDS ON THE SCREEN')

    def set_cards_or_num_of_cards(self, cards):
        if self.mode == 'me':
            self.card_handler.set_cards(cards)
        else:
            self.card_handler.set_num_of_cards(cards)

    def get_nickname(self):
        return self.nickname

    def get_mode(self):
        return self.mode