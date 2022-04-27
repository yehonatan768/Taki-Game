from pygame import transform
from Const_params import *


class Client_Cards_Handler(object):

    def __init__(self, card_size, cards_distance, angle):
        self.card_size = card_size
        self.cards_distance = cards_distance
        self.angle = angle

        self.num_of_cards = None
        self.list_cards = []
        self.cards_list_index = None
        self.length = None
        self.cards = None
        self.middle_point_of_all_cards = []
        self.equal = None

    # Get and Set functions
    def set_cards(self, cards):
        del self.list_cards[:]
        try:
            self.num_of_cards = len(cards)

            if self.num_of_cards > 9:
                self.cards_list_index = 0
                self.list_divider(cards)
                self.cards = self.list_cards[self.cards_list_index]
                self.length = len(self.cards)

            else:
                self.cards = cards
                self.length = self.num_of_cards

            if self.length % 2 == 0:
                self.equal = True
            else:
                self.equal = False
        except:
            print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO SET THE CLIENT'S CARDS")

    def set_page(self):
        try:
            self.cards = self.list_cards[self.cards_list_index]
            self.length = len(self.cards)
            if self.length % 2 == 0:
                self.equal = True
            else:
                self.equal = False
        except:
            print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO SET THE CARD'S PAGE")

    # other functions
    def list_divider(self, cards):
        for i in range(0, self.num_of_cards, 9):
            self.list_cards.append(cards[i: i + 9])

    def not_equal_cards(self, middle_card_x, middle_card_y):
        try:
            dx = int(-self.cards_distance * (int(self.length / 2) + 1))
            dy = 8 * int(self.length / 2 + 1)
            if self.length == 9:
                dy += 7
            for i in range(self.length):

                if i == 1 and self.length == 9:
                    dy -= 15

                elif i == self.length - 1 and self.length == 9:
                    dy += 15

                if int(self.length / 2) + 1 > i:
                    dx += self.cards_distance
                    dy -= 8

                elif int(self.length / 2) + 1 < i:
                    dx += self.cards_distance
                    dy += 8
                else:
                    dx, dy = 100, 8
                    if self.length == 9:
                        dy -= 8
                screen.blit(transform.rotate(
                    transform.scale(search(self.cards[i]), (int(self.card_size[0]), int(self.card_size[1]))),
                    self.angle), (int(middle_card_x + dx), int(middle_card_y + dy)))

                self.middle_point_of_all_cards.append((int(middle_card_x + dx), int(middle_card_y + dy)))

        except:
            print('not equal cards printer')

    def equal_cards(self, middle_card_x, middle_card_y):
        try:
            dx, dy = - self.cards_distance * (self.length / 2) - self.cards_distance / 2, 8 * (self.length / 2)
            for i in range(self.length):
                if int(self.length / 2) > i:
                    dx += self.cards_distance
                    dy -= 8

                elif int(self.length / 2) == i:
                    dx = self.cards_distance / 2

                else:
                    dx += self.cards_distance
                    dy += 8

                screen.blit(
                    transform.rotate(
                        transform.scale(search(self.cards[i]), (int(self.card_size[0]), int(self.card_size[1]))),
                        self.angle), (int(middle_card_x + dx), int(middle_card_y + dy)))

                self.middle_point_of_all_cards.append((int(middle_card_x + dx), int(middle_card_y + dy)))
        except:
            pass

    def card_blit(self, middle_card_x, middle_card_y):  # blit the cards to the screen
        del self.middle_point_of_all_cards[:]
        try:
            if not self.equal:
                self.not_equal_cards(middle_card_x, middle_card_y)
            else:
                self.equal_cards(middle_card_x, middle_card_y)
        except:
            print('[ERROR] AN ERROR OCCURRED IN THE CARDS BLIT FUNCTION OF THE CLIENT')

    def check_navigation_buttons(self, mouse_position_x, mouse_position_y):
        if self.cards_list_index is not None:
            try:
                # navigation buttons for the cards
                if 0 <= self.cards_list_index < len(self.list_cards) - 1:
                    screen.blit(right_button_game, (0, 0))

                if self.cards_list_index > 0:
                    screen.blit(left_button_game, (0, 0))
            except Exception as error_code:
                print(error_code)

            if mouse_position_x is not None and mouse_position_y is not None:
                try:
                    if 1460 < mouse_position_x < 1529 and 823 < mouse_position_y < 882 and self.cards_list_index < len(
                            self.list_cards) - 1:
                        screen.blit(bold_right_button_game, (0, 0))

                    elif 384 < mouse_position_x < 503 and 823 < mouse_position_y < 882 and self.cards_list_index > 0:
                        screen.blit(bold_left_button_game, (0, 0))
                except Exception as error_code:
                    print(error_code)

    def game_handler(self, mouse_position_x=None, mouse_position_y=None):
        if self.cards is not None:
            try:
                self.check_navigation_buttons(mouse_position_x, mouse_position_y)
            except:
                print("[ERROR] AN ERROR OCCURRED WITH THE CLIENT'S CARDS NAVIGATION SYSTEM")
            try:
                self.card_blit_handler()
            except:
                print("[ERROR] AN ERROR OCCURRED WITH THE CLIENT'S CARDS BLIT FUNCTION")

    def card_blit_handler(self):
        try:
            px, py = screen.getScreen().get_width() * 0.46, screen.getScreen().get_height() * 0.735
            if type(self.cards) is list:

                try:
                    if self.length % 2 == 1:
                        self.card_blit(px, py)
                    else:
                        self.card_blit(px, py)
                except:
                    print('An error occurred with card blit')

            elif type(self.cards) is str:
                # only 1 card
                try:
                    screen.blit(transform.scale(search(self.cards), self.card_size), (px, py))
                    self.middle_point_of_all_cards.append((int(px), int(py)))
                except:
                    pass
        except:
            print('An error occurred with card sorter')

    def card_button_handler(self, mouse_position_x, mouse_position_y, event, click, turn):
        if self.cards is not None:
            try:
                # check for an events related to the cards
                if event.type == pygame.MOUSEBUTTONDOWN and click[0] == 1:
                    if self.cards_list_index is not None:
                        if self.cards_list_index < len(
                                self.list_cards) - 1 and 1460 < mouse_position_x < 1529 and 823 < mouse_position_y < 882:
                            self.cards_list_index += 1
                            self.set_page()

                        elif self.cards_list_index > 0 and 384 < mouse_position_x < 503 and 823 < mouse_position_y < 882:
                            self.cards_list_index -= 1
                            self.set_page()
                    if turn:
                        try:
                            for i in range(0, self.length):
                                if self.card_button_check(i, mouse_position_x, mouse_position_y):
                                    return self.cards[i]

                        except:
                            print("[ERROR] AN ERROR OCCURRED WITH THE CARD BUTTON HANDLER")
                return False
            except:
                print("[ERROR] AN ERROR OCCURRED WITH THE CARDS AND NAVIGATION BUTTON HANDLER 1")

    def card_surface(self, index, mouse_position_x, mouse_position_y):
        try:
            if self.middle_point_of_all_cards[index][0] < mouse_position_x < self.middle_point_of_all_cards[index][0] + \
                    self.card_size[0] and self.middle_point_of_all_cards[index][1] < mouse_position_y < 896:
                return True
            else:

                return False
        except:
            pass

    def card_button_check(self, index, mouse_position_x, mouse_position_y):
        try:

            if self.length != 1:

                if self.card_surface(index, mouse_position_x, mouse_position_y):
                    if index != self.length - 1:
                        if self.card_surface(index + 1, mouse_position_x, mouse_position_y):
                            return False
                        return True
                    return True
                return False

            else:

                if self.card_surface(index, mouse_position_x, mouse_position_y):
                    return True
                return False
        except:
            print('[ERROR] AN ERROR OCCURRED WITH THE CARD BUTTON CHECK')