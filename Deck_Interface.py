from pygame import transform
from Const_params import *


class Deck_Interface(object):
    def __init__(self, card_size, location):
        self.card_size = card_size
        self.location = location
        self.last_position = (self.location[0] + 4 * 4, self.location[1])

    def deck_button_check(self, mouse_position_x, mouse_position_y):
        try:
            if self.last_position[0] < mouse_position_x < self.last_position[0] + self.card_size[0] and \
                    self.last_position[1] < mouse_position_y < self.last_position[1] + self.card_size[1]:
                return True
            else:
                return False
        except:
            pass

    def game_handler(self, mouse_position_x, mouse_position_y, event, click):
        try:
            if event.type == pygame.MOUSEBUTTONDOWN and click[0] == 1:
                if self.deck_button_check(mouse_position_x, mouse_position_y):
                    return True
                return False
        except:
            print('[ERROR] AN ERROR OCCURRED WITH GAME HANDLER')

    def blit(self):
        for i in range(5):
            screen.blit(transform.scale(card_back, self.card_size), (self.location[0] + i * 4, self.location[1]))