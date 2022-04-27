import random
from Discarded_Cards import Discarded_Cards
from Deck import Deck
from threading import Thread
import time


class Game(object):

    def __init__(self, player):
        self.players = [player]
        self.deck = Deck()
        self.discarded_cards = Discarded_Cards(self.deck.give_first_card_to_discarded())

        self.active = False
        self.is_full = False
        self.turn_over = True
        self.playing = None
        self.waiting_for_request = False

        self.taki = False
        self.active_card = None
        self.plus_2_counter = 0
        self.request = None
        self.info = None

        try:
            self.game_thread = Thread(target=self.lobby, args=())
            self.game_thread.start()
        except:
            print('error with thread')

    def reaset_parameters(self):
        self.deck = Deck()
        self.discarded_cards = Discarded_Cards(self.deck.give_first_card_to_discarded())

        self.active = False
        self.is_full = False
        self.turn_over = True
        self.playing = None
        self.waiting_for_request = False

        self.taki = False
        self.active_card = None
        self.plus_2_counter = 0
        self.request = None
        self.info = None

    # lobby activation function
    def lobby(self):
        while True:
            try:
                if self.players is None:
                    break
                elif 0 == len(self.players) or len(self.players) == 2:
                    break
            except:
                pass

        if self.players is None:
            pass

        elif len(self.players) >= 2:
            self.is_full = True
            time.sleep(5)
            self.play()

    def enough_players(self):
        if len(self.players) == 1 or len(self.players) == 0:
            return False
        else:
            return True

    # main function of the game
    def play(self):
        self.game_start_action()
        self.playing = True
        # parameters
        round_direction = True
        i = 1
        plus_2 = (False, None)

        # starting the game
        while self.playing and self.turn_over and self.enough_players():
            self.turn(self.players[i - 1])
            try:
                if self.check_for_win(i - 1):
                    self.send_request(('WINNER', self.players[i - 1].get_nickname()))  # 4
                    break
                else:
                    if self.active_card == 'change_direction':
                        if round_direction:
                            round_direction = False
                        else:
                            round_direction = True
                        self.active_card = None
                    if self.taki:
                        pass
                    elif self.active_card == 'stop':
                        if round_direction:
                            i += 2
                        else:
                            i -= 2
                        self.active_card = None
                    elif self.active_card == 'plus':
                        self.active_card = None
                    else:
                        if round_direction:
                            i += 1
                        else:
                            i -= 1

                    if i > len(self.players) and round_direction:
                        i -= len(self.players)
                    elif i < 1 and not round_direction:
                        i += len(self.players)
            except:
                pass
        if len(self.players) == 1:
            self.send_request(('WINNER', self.players[0].get_nickname()))

    # start and end game functions
    def game_start_action(self):
        # determine who is the starts
        self.send_request('START_GAME')

        self.who_starts()
        self.send_request(('TOP_CARD', self.discarded_cards.get_value_of_top_card()))  # 1

        # giving all players 8 cards
        for player in self.players:
            player.get_New_Cards(self.deck, 8)
            self.send_request(('SEND_CARDS', (player.get_nickname(), player.send_card_in_hands())))

    # get and set functions
    def get_players(self):
        return self.players

    def get_request(self):
        return self.request

    def set_request(self, request):
        self.request = request

    def get_new_deck_and_discarded(self):
        self.deck = Deck()
        self.discarded_cards = Discarded_Cards(self.deck.give_first_card_to_discarded())

    def get_players_nickname_list(self):
        nick_l = []
        for p in self.players:
            nick_l.append(p.get_nickname())

        return nick_l

    def get_is_full(self):
        return self.is_full

    def get_is_active(self):
        return self.active

    def set_is_active(self):
        self.active = True

    def set_info(self, msg):
        self.info = msg

    # send and get information from/to players
    def send_request(self, request):
        if request is not None:
            self.set_request(request)
            r = request
            while r is not None:
                r = self.request

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, client):
        if len(self.players) == 1:
            self.players = None

        else:
            for player in self.players:
                if player.get_client() == client:
                    self.players.remove(player)
                    break

            if len(self.players) == 1 and self.playing == True:
                self.is_full = False
                self.playing = False

    # determine who starts
    def who_starts(self):
        r = random.randint(0, len(self.players))
        if len(self.players) == 2:
            if r == 1:
                self.players[0], self.players[1] = self.players[1], self.players[0]

        elif len(self.players) == 3:
            if r == 1:
                self.players[0], self.players[2] = self.players[2], self.players[0]
                self.players[0], self.players[1] = self.players[1], self.players[0]
            elif r == 2:
                self.players[0], self.players[2] = self.players[2], self.players[0]
                self.players[2], self.players[1] = self.players[1], self.players[2]

        elif len(self.players) == 4:
            if r == 3:
                for i in range(2):
                    self.players[i], self.players[2 + i] = self.players[2 + i], self.players[i]

            else:
                for i in range(3):
                    if r == 1:
                        self.players[i], self.players[i + 1] = self.players[i + 1], self.players[i]

                    elif r == 3:
                        self.players[3 - i], self.players[2 - i] = self.players[2 - i], self.players[3 - i]

    # win check
    def check_for_win(self, n):
        if self.players[n].get_Number_Of_Cards_In_Hand() == 0:
            if self.active_card == 'plus':
                self.players[n].get_New_Cards(self.deck, 1)
            else:
                return True
        return False

    # time check function
    def check_time(self, t_start, t_end):
        if t_end - t_start < 30:
            return True
        self.waiting_for_request = False
        self.turn_over = True
        return False

    # check if made a legal move functions
    @staticmethod
    def check_for_action_card(card):
        if card[:6] == 'plus_2' or card[:16] == 'change_direction':
            return True
        else:
            value, color = card.split('_')
            if value == 'taki' or value == 'plus' or value == 'stop' or value == 'change':
                return True
        return False

    def have_legal_move(self, player):
        for card in player.get_cards_in_hand():
            if self.taki:
                if self.discarded_cards.get_top_Card().get_color() == card.get_color() or\
                        card.get_value() == 'change' and card.get_color() == 'colorful' or\
                        card.get_value() == 'taki' and card.get_color() == 'colorful':
                    return True
            elif self.active_card == 'plus_2':
                if card.get_value() == 'plus_2':
                    return True
            elif self.active_card is None:
                if self.discarded_cards.get_top_Card().get_value() == card.get_value() or \
                        self.discarded_cards.get_top_Card().get_color() == card.get_color() or\
                        card.get_value() == 'change' and card.get_color()== 'colorful' or\
                        card.get_value() == 'taki' and card.get_color() == 'colorful':
                    return True
        return False

    def check_if_legal_move(self, card):
        if card[:6] == 'plus_2':
            value, color = card[:6], card[7:]
        elif card[:16] == 'change_direction':
            value, color = card[:16], card[17:]
        else:
            value, color = card.split('_')
        if self.active_card == 'plus_2':
            if value == 'plus_2':
                return True

        elif self.taki:
            if self.discarded_cards.get_top_Card().get_color() == color or value == 'change' and \
                    color == 'colorful' or value == 'taki' and color == 'colorful':
                return True

        elif self.active_card is None:
            if self.discarded_cards.get_top_Card().get_value() == value or \
                    self.discarded_cards.get_top_Card().get_color() == color or value == 'change' and \
                    color == 'colorful' or value == 'taki' and color == 'colorful':
                return True

        return False

    def active_card_played(self, card):
        if card[:6] == 'plus_2':
            value = 'plus_2'
        elif card[:16] == 'change_direction':
            value = 'change_direction'
        else:
            value, color = card.split('_')

        if value == 'stop':  # DONE
            self.active_card = 'stop'
        elif value == 'change_direction':  # DONE
            self.active_card = 'change_direction'
        elif value == 'plus_2':  # DONE
            self.active_card = 'plus_2'
            self.plus_2_counter += 1
        elif value == 'plus':  # DONE
            self.active_card = 'plus'
        elif value == 'taki':  # DONE
            self.taki = True

    # play the card
    def check_in_player_cards(self, player, card_selected):
        for c in player.get_cards_in_hand():
            card = str(c.get_value()) + '_' + str(c.get_color())
            if card == card_selected:
                self.discarded_cards.recieve_Card(player.throw_Card_To_Discarded_Cards(c))
                if card == 'taki_colorful':
                    self.discarded_cards.change_card_color()
                    self.send_request(('TOP_CARD', self.discarded_cards.get_value_of_top_card()))
                elif card == 'change_colorful':
                    self.change_colorful()
                    self.send_request(('TOP_CARD', self.discarded_cards.get_value_of_top_card()))
                return card
        return None

    def change_colorful(self):
        while not self.turn_over:
            try:
                if self.info is not None:
                    if self.info == 'yellow' or self.info == 'red' or self.info == 'green' or self.info == 'blue':
                        self.discarded_cards.change_card_color(self.info)
                        self.info = None
                        return None
            except:
                print('change_colorful error')

        if self.discarded_cards.get_top_Card().show() == 'change_colorful':
            r = random.randint(0, 4)
            colors = ['yellow', 'red', 'green', 'blue']
            self.discarded_cards.change_card_color(colors[r])

    def give_card_function(self, response, player):
        if response[0] == 'GIVE_CARD' and response[1] == player.get_nickname():
            if self.active_card == 'plus_2' and not self.taki:
                player.get_New_Cards(self.deck, self.plus_2_counter * 2)
                self.plus_2_counter = 0
                self.active_card = None
            elif not self.taki:
                player.get_New_Cards(self.deck, 1)
                self.active_card = None
            elif self.taki:
                self.taki = False
            self.send_request(('SEND_CARDS', (player.get_nickname(), player.send_card_in_hands())))
            self.waiting_for_request = False
            return 'return_none'

    def play_turn_function(self, response, player):
        if response[0] == 'PLAY_TURN' and response[1][0] == player.get_nickname():
            if self.check_if_legal_move(response[1][1]):
                card = self.check_in_player_cards(player, response[1][1])
                if self.check_for_action_card(card):
                    self.active_card_played(card)
                    self.send_request(('SEND_CARDS', (player.get_nickname(), player.send_card_in_hands())))
                    self.send_request(('TOP_CARD', self.discarded_cards.get_value_of_top_card()))
                    self.waiting_for_request = False
                    return 'return_none'
                elif card is not None:
                    self.send_request(('TOP_CARD', self.discarded_cards.get_value_of_top_card()))
                    self.send_request(('SEND_CARDS', (player.get_nickname(), player.send_card_in_hands())))
                    self.waiting_for_request = False
                    return 'return_none'

    # turn manage functions
    def check_for_player_response(self, player):  # the function only runs once
        self.waiting_for_request = True
        while not self.turn_over and self.enough_players():
            try:
                if self.info is not None:
                    response = self.info
                    self.info = None
                    if self.give_card_function(response, player) == 'return_none':
                        return None
                    elif self.play_turn_function(response, player) == 'return_none':
                        return None

            except Exception as er:
                print(er)

    def turn(self, player):  # create turn function
        self.turn_over = False
        self.send_request(('TURN', player.get_nickname()))  # 3
        if self.have_legal_move(player):
            t_start = time.time()
            t_end = 0
            player_response = Thread(target=self.check_for_player_response, args=(player,))
            player_response.start()
            while self.check_time(t_start, t_end) and self.waiting_for_request and self.enough_players():
                t_end = time.time()
            player_response.join()
        else:
            if self.plus_2_counter == 0 and not self.taki:
                player.get_New_Cards(self.deck, 1)
                self.active_card = None
            elif not self.taki:
                player.get_New_Cards(self.deck, self.plus_2_counter * 2)
                self.plus_2_counter = 0
                self.active_card = None
            self.taki = False
            self.send_request(('SEND_CARDS', (player.get_nickname(), player.send_card_in_hands())))

        self.turn_over = True
