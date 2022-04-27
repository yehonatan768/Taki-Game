from Const_params import *
from pygame import transform


class Discarded_Deck_Interface(object):
    def __init__(self, card_size, location):
        self.last_card = None

        self.location = location
        self.card_size = card_size

    def set_last_card(self, card):
        self.last_card = card

    def get_top_card(self):
        return self.last_card

    def blit_discarded_deck(self):
        if self.last_card is not None:
            try:
                screen.blit(transform.scale(search(self.last_card), (int(self.card_size[0]), int(self.card_size[1]))),
                            (int(self.location[0]), int(self.location[1])))
            except:
                pass
