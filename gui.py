from tkinter import *
from tkinter import Label

from blackjack import Player, Dealer, conclude_game


class SetUpTable:

    def __init__(self):

        self.pot = 0

        self.root = Tk()
        self.root.title('Casino')
        self.root.iconbitmap('C:/Users/SavSamuShaman/Desktop/blackjack/pkc2.ico')

        self.player = Player('Unknown')
        self.dealer = Dealer()

        self.question_label = Label(self.root, text="You walk to the table and the dealer ask for your name")
        self.question_label.grid(row=0, column=1)

        self.start_button = Button(self.root, text='Tell the dealer your name', command=self.set_up_environ)
        self.start_button.grid(row=2, column=1, padx=15, pady=20)

        self.entry = Entry(self.root, width=30)
        self.entry.grid(row=1, column=1, columnspan=3)

        self.error_message = Label(self.root)

        self.message = Label(self.root, text='Best of luck a the blackjack table ;)')
        self.player_money = Label(self.root, text=f'Your money : {self.player.chips}')
        self.dealer_money = Label(self.root, text=f'Dealer money : {self.dealer.chips}')
        self.pot_label = Label(self.root, text=f'Pot : 0')
        self.current_score = Label(self.root, text=f'Current score : 0')

        self.hit_me_button = Button(self.root, text='Hit me', command=self.hit_me)
        self.stay_button = Button(self.root, text='Stay', command=self.stay)

        self.bet_button = Button(self.root, text='Bet', command=self.bet)
        self.root.mainloop()

    def set_up_environ(self):
        self.question_label['text'] = 'The Red Sparrow welcomes you, {name}'.format(name=self.entry.get())
        self.entry.grid_forget()
        self.start_button.grid_forget()

        self.player.name = self.entry.get()
        self.entry.delete(0, END)

        self.message.grid(row=2, column=1)
        self.player_money.grid(row=3, column=2)
        self.dealer_money.grid(row=3, column=0)
        self.pot_label.grid(row=3, column=1)

        self.start_button = Button(self.root, text='New Round', command=self.new_round)
        self.start_button.grid(row=4, column=1)
        return

    def new_round(self):
        self.start_button.grid_forget()
        self.entry.grid(row=5, column=1)
        self.bet_button.grid(row=5, column=2)
        return

    def bet(self):
        self.dealer.clear_score()
        self.player.clear_score()
        self.pot = 0
        self.current_score['text'] = 'Current score : 0'
        self.message['text'] = 'Best of luck a the blackjack table ;)'
        try:
            amount = int(self.entry.get())
            if amount > self.player.chips:
                self.error_message['text'] = 'Not enough money'
                self.error_message.grid(row=6, column=1)
                return
            self.pot += self.player.bet(amount) + self.dealer.bet(amount)
            self.entry.grid_forget()
            self.bet_button.grid_forget()
            self.pot_label['text'] = 'Pot :{pot}'.format(pot=self.pot)
            self.error_message.grid_forget()
            self.current_score.grid(row=4, column=1)
            self.stay_button.grid(row=4, column=0)
            self.hit_me_button.grid(row=4, column=2)
            self.update_money_labels()
            self.entry.delete(0, END)
        except ValueError:
            self.error_message['text'] = 'Invalid bet'
            self.error_message.grid(row=6, column=1)

    def hit_me(self):
        card = self.dealer.deal_card()
        self.player.add_to_score(card)
        player_score = self.player.calculate_score()
        if player_score == 21:
            self.player.win(self.pot)
            self.pot = 0
            self.current_score['text'] = 'Current score : {score}'.format(score=player_score)
            self.message['text'] = f'{self.player.name} has Blackjack !'
            self.hit_me_button.grid_forget()
            self.stay_button.grid_forget()
            self.new_round()
            self.update_money_labels()
        elif player_score < 21:
            self.current_score['text'] = 'Current score : {score}'.format(score=player_score)
        else:
            self.dealer.win(self.pot)
            self.pot = 0
            self.pot_label['text'] = 'Pot : 0'
            self.message['text'] = f'{self.player.name} busted out'
            self.current_score['text'] = 'Current score: {score}'.format(score=player_score)

            self.update_money_labels()
            self.hit_me_button.grid_forget()
            self.stay_button.grid_forget()
            self.new_round()

    def stay(self):
        player_score = self.player.calculate_score()
        player_points = abs(21 - player_score)
        dealer_points = abs(21 - conclude_game(self.dealer))
        if dealer_points < player_points:
            self.dealer.win(self.pot)
            self.message[
                'text'] = f'Your score : {player_score} \nDealer score {self.dealer.calculate_score()} \nThe dealer was closer to 21. You lose.'
        elif dealer_points == player_points:
            self.dealer.win(self.pot / 2)
            self.player.win(self.pot / 2)
            self.message[
                'text'] = f"Your score : {player_score} \nDealer score {self.dealer.calculate_score()} \nIt's a tie"
        else:
            self.player.win(self.pot)
            self.message[
                'text'] = f"Your score : {player_score} \nDealer score {self.dealer.calculate_score()} \nYou won ${self.pot}"

        self.update_money_labels()
        self.hit_me_button.grid_forget()
        self.stay_button.grid_forget()
        self.new_round()

    def update_money_labels(self):
        self.dealer_money['text'] = f'Dealer money : {self.dealer.chips}'
        self.player_money['text'] = f'Player money : {self.player.chips}'


new_game = SetUpTable()
