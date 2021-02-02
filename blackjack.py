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


def start_game():
    player = Player('John Doe')
    dealer = Dealer()
    while True:
        player_choice = input('Press a key + enter to start another round > ')
        if player_choice:
            current_bet = int(input('You want to bet : '))
            pot = player.bet(current_bet) + dealer.bet(current_bet)

            while player.calculate_score() < 21:
                deal = input('Leave blank to deal, type anything to stop : ')
                if not deal:
                    card = dealer.deal_card()
                    player.add_to_score(card)
                    print(f'You got dealt a {card} \nCurrent points : {player.calculate_score()}')
                else:
                    break

            player_points = player.calculate_score()

            if player_points > 21:
                print(f'{player.name} busted out')
                dealer.win(pot)
                print(f'The dealer won {pot}')
            elif player_points == 21:
                print(f'{player.name} has Blackjack')
                player.win(pot)
                print(f'{player.name} won {pot}')
            else:
                dealer_final_points = abs(21-conclude_game(dealer))
                player_points = abs(21-player_points)
                if dealer_final_points < player_points:
                    dealer.win(pot)
                    print(f'Dealer score : {dealer_final_points} \nPlayer score : {player_points}')
                    print(f'The dealer won {pot}')
                elif dealer_final_points == player_points:
                    dealer.win(pot / 2)
                    player.win(pot / 2)
                    print(f'Dealer score : {dealer_final_points} \nPlayer score : {player_points}')
                    print("It's a tie")
                else:
                    player.win(pot)
                    print(f'Dealer score : {dealer_final_points} \nPlayer score : {player_points}')
                    print(f'{player.name} won {pot}')

            pot = 0
            dealer.clear_score()
            player.clear_score()
        else:
            print('Thank you for playing BlackJack')
            break


start_game()
