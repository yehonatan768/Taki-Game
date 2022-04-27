
class Discarded_Cards(object):
    def __init__(self, first_Card):
        self.card_stack = []
        self.recieve_Card(first_Card)

    def get_top_Card(self):
        return self.card_stack[len(self.card_stack) - 1]

    def change_card_color(self, color=None):
        top_card = self.card_stack[len(self.card_stack) - 1]
        if top_card.show() == 'taki_colorful':
            top_card.set_color(self.card_stack[len(self.card_stack) - 2].get_color())
        elif top_card.show() == 'change_colorful':
            top_card.set_color(color)

    def get_value_of_top_card(self):
        return self.get_top_Card().show()

    def recieve_Card(self, card):
        self.card_stack.append(card)
