from pygame import transform
from Const_params import *


class Other_Players_Card_Handler(object):
    def __init__(self, card_size, cards_distance, angle, location, mode):
        self.location = location
        self.mode = mode  # there is only 3 (sides or front)

        self.num_of_cards = 0
        self.length = 0

        self.card_size = card_size
        self.cards_size = []
        self.cards_distance = cards_distance
        self.equal = None
        self.angle = angle

    def set_num_of_cards(self, num_of_cards):
        try:
            self.num_of_cards = num_of_cards
            if self.num_of_cards >= 13 and self.mode == 'front':
                self.length = 13
            elif self.num_of_cards >= 9 and self.mode == 'right side' or self.mode == 'left side' and self.num_of_cards >= 9:
                self.length = 9
            else:
                self.length = num_of_cards

            if self.num_of_cards % 2 == 0:
                self.equal = True
            else:
                self.equal = False
            if self.num_of_cards > 1:
                self.determine_cards_sizes()
        except:
            print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO SET THE NUMBER OF THE OTHER PLAYER'S CARDS")

    def card_handler(self):
        try:
            if 1 < self.num_of_cards:
                try:
                    self.cards_blit()
                except:
                    print('card blit problem of other players')
            elif self.num_of_cards == 1:
                self.blit_card(self.card_size[0], self.card_size[1], self.location[0], self.location[1])

        except:
            pass

    def determine_not_equal_cards_sizes(self):
        d = 8 * (int(self.length / 2) + 1)

        for i in range(self.length):
            if int(self.length / 2) > i:
                d -= 8

            elif int(self.length / 2) < i:
                d += 8

            else:
                d = 0
            self.cards_size.append((self.card_size[0], self.card_size[1] - d))

    def determine_equal_cards_sizes(self):
        if self.num_of_cards > 2:
            d = (int(self.length / 2)) * 8
            for i in range(self.length):
                if int(self.length / 2) - 1 > i:
                    d -= 8

                elif int(self.length / 2) < i:
                    d += 8

                else:
                    d = 0

                self.cards_size.append((self.card_size[0], self.card_size[1] - d))

        else:
            self.cards_size.append(self.card_size)
            self.cards_size.append(self.card_size)

    def determine_cards_sizes(self):
        del self.cards_size[:]
        if not self.equal:
            self.determine_not_equal_cards_sizes()
        else:
            self.determine_equal_cards_sizes()

    def blit_card(self, card_width, card_height, x_location, y_location):
        try:
            screen.blit(transform.rotate(transform.scale(half_card_back, (card_width, card_height)), self.angle),
                        (x_location, y_location))
        except:
            pass

    def blit_not_equal_cards(self):
        try:
            dx = -self.cards_distance * (int(self.length / 2) + 1)

            for i in range(self.length):

                if int(self.length / 2) + 1 > i or int(self.length / 2) + 1 < i:
                    dx += self.cards_distance
                else:
                    dx = self.cards_distance

                try:
                    if self.mode == 'front':
                        self.blit_card(int(self.cards_size[i][0]), int(self.cards_size[i][1]),
                                       int(self.location[0] + dx), int(self.location[1]))

                    elif self.mode == 'left side':
                        self.blit_card(int(self.cards_size[i][0]), int(self.cards_size[i][1]),
                                       int(self.location[0] + self.card_size[1] - self.cards_size[i][1]),
                                       int(self.location[1] + dx))

                    elif self.mode == 'right side':
                        self.cards_blit(int(self.cards_size[i][0]), int(self.cards_size[i][1]),
                                        int(self.location[0]), int(self.location[1] + dx))

                except:
                    pass
        except:
            print('loop exception')

    def blit_equal_cards(self):
        dx = - self.cards_distance * (self.length / 2) - self.cards_distance / 2
        for i in range(self.length):
            dx += self.cards_distance
            if self.mode == 'front':
                self.blit_card(int(self.cards_size[i][0]), int(self.cards_size[i][1]),
                               int(self.location[0]) + dx, int(self.location[1]))

            elif self.mode == 'left side':
                self.blit_card(int(self.cards_size[i][0]), int(self.cards_size[i][1]),
                               int(self.location[0] + self.card_size[1] - self.cards_size[i][1]),
                               int(self.location[1] + dx))
            elif self.mode == 'right side':
                self.blit_card(int(self.cards_size[i][0]), int(self.cards_size[i][1]),
                               int(self.location[0] - self.card_size[1] + self.cards_size[i][1]),
                               int(self.location[1] + dx))

    def blit_two_cards(self):
        try:
            if self.mode == 'front':
                self.blit_card(int(self.card_size[0]), int(self.card_size[1]),
                               int(self.location[0] - self.cards_distance / 2), int(self.location[1]))
                self.blit_card(int(self.card_size[0]), int(self.card_size[1]),
                               int(self.location[0] + self.cards_distance / 2), int(self.location[1]))

            elif self.mode == 'left side' or 'right side':

                self.blit_card(int(self.card_size[0]), int(self.card_size[1]), int(self.location[0]),
                               int(self.location[1] - self.cards_distance / 2))
                self.blit_card(int(self.card_size[0]), int(self.card_size[1]), int(self.location[0]),
                               int(self.location[1] + self.cards_distance / 2))
        except:
            pass

    def cards_blit(self):
        if not self.equal:
            self.blit_not_equal_cards()
        else:
            try:
                if self.num_of_cards == 2:
                    self.blit_two_cards()
                else:
                    self.blit_equal_cards()
            except:
                print("[ERROR] AN ERROR OCCURRED WHILE TRYING TO BLIT THE EQUAL CARDS OF " + str(self.mode).upper() + " PLAYER")