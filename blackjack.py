import random


class BasePlayer:
    def __init__(self):
        self.chips = 500
        self.current_score = {}

    def clear_score(self):
        self.current_score = {}

    def add_to_score(self, card):
        if card in self.current_score:
            self.current_score[card] += 1
        else:
            self.current_score[card] = 1

    def win(self, amount):
        self.chips += amount

    def bet(self, amount):
        self.chips -= amount
        return amount

    def calculate_score(self):
        points = 0

        for card in self.current_score.keys():
            if card in ['J', 'Q', 'K']:
                points += 10 * self.current_score[card]
            elif card == 'A':
                points += 11 * self.current_score[card]
            else:
                points += int(card) * self.current_score[card]

        return points


class Player(BasePlayer):

    def __init__(self, name):
        super().__init__()
        self.name = name


class Dealer(BasePlayer):

    def __init__(self):
        super().__init__()
        self.chips = 5000
        self.__cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.__deck = {card: 4 for card in self.__cards}

    def deal_card(self):
        random_card = random.choice(list(self.__deck.keys()))
        self.__deck[random_card] -= 1
        if self.__deck[random_card] == 0:
            del self.__deck[random_card]
        return random_card

    def reset_deck(self):
        self.__deck = {card: 4 for card in self.__cards}


def conclude_game(dealer_instance):
    while dealer_instance.calculate_score() < 17:
        card = dealer_instance.deal_card()
        dealer_instance.add_to_score(card)
    return dealer_instance.calculate_score()
