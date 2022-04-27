import random
from Card import Card

class Deck(object):

    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        for color in ['red', 'blue', 'green', 'yellow']:
            for value in ['1', 'plus_2', '3', '4', '5', '6', '7', '8', '9', 'taki', 'plus', 'stop', 'change_direction']:
                self.cards.append(Card(value, color, 1))
                self.cards.append(Card(value, color, 2))
        for n in range(6):
            if n > 3:
                self.cards.append(Card('taki', 'colorful', n + 1))
            else:
                self.cards.append(Card('change', 'colorful', n - 3))

    def show(self):
        for card in self.cards:
            card.show()

    def shuffle(self):
        for n in range(3):
            for i in range(0, len(self.cards)):
                r = random.randint(0, len(self.cards) - 1)
                self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def give_Card(self):
        if self.cards is None:
            self.build()
            self.shuffle()
        return self.cards.pop()

    def give_first_card_to_discarded(self):
        for i in range(len(self.cards) - 1):
            if self.cards[i].get_value() != 'taki' and self.cards[i].get_value() != 'plus' and self.cards[
                i].get_value() != 'stop' \
                    and self.cards[i].get_value() != 'change_direction' and self.cards[i].get_value() != 'plus_2' \
                    and self.cards[i].get_value() != 'change':
                return self.cards.pop(i)