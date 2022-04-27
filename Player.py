
class Player(object):

    def __init__(self, client, nickname):
        self.cards_In_Hand = []
        self.nickname = nickname
        self.client = client

    def set_cards_in_hand(self, cards):
        self.cards_In_Hand = cards

    def set_nickname(self, nickname):
        self.nickname = nickname

    def set_client(self, client):
        self.client = client

    def send(self, message):
        self.client.send(message)

    def recieve(self):
        return self.client.recieve()

    def get_client(self):
        return self.client

    def get_cards_in_hand(self):
        return self.cards_In_Hand

    def get_Number_Of_Cards_In_Hand(self):
        return len(self.cards_In_Hand)

    def get_nickname(self):
        return self.nickname

    def get_New_Cards(self, deck, number):
        for i in range(number):
            self.cards_In_Hand.append(deck.give_Card())

    def throw_Card_To_Discarded_Cards(self, card):
        return self.cards_In_Hand.pop(self.cards_In_Hand.index(card))

    def send_card_in_hands(self):
        card_lst = []
        for card in self.cards_In_Hand:
            card_lst.append(card.get_value() + '_' + card.get_color())

        return card_lst