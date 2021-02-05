from tkinter import *

from blackjack import Player, Dealer, conclude_game


class SetupGame:

    def __init__(self):

        # game logic related
        self.pot = 0
        self.player = Player()
        self.dealer = Dealer()

        # interface related - add interface elements here
        self.root = Tk()
        self.root.title('Casino')
        self.root.iconbitmap('C:/Users/SavSamuShaman/Desktop/blackjack/pkc2.ico')
        # labels
        self.header_label = Label(self.root, text="You walk to the table and the dealer ask for your name")
        self.message_label = Label(self.root, text='Best of luck a the blackjack table ;)')
        self.error_message_label = Label(self.root)
        self.player_money_label = Label(self.root, text=f'Your money : {self.player.chips}')
        self.dealer_money_label = Label(self.root, text=f'Dealer money : {self.dealer.chips}')
        self.pot_label = Label(self.root, text=f'Pot : 0')
        self.current_score_label = Label(self.root, text=f'Current score : 0')
        # buttons
        self.hit_me_button = Button(self.root, text='Hit me', command=self.hit_me)
        self.stay_button = Button(self.root, text='Stay', command=self.stay)
        self.bet_button = Button(self.root, text='Bet', command=self.bet)
        self.start_button = Button(self.root, text='Tell the dealer your name', command=self.set_up_environ)
        # input box
        self.entry = Entry(self.root, width=30)

        # element placement
        self.header_label.grid(row=0, column=1)
        self.entry.grid(row=1, column=1, columnspan=3)
        self.start_button.grid(row=2, column=1, padx=15, pady=20)

        self.root.mainloop()

    def set_up_environ(self):

        name_input = self.entry.get()
        if name_input:
            self.player.name = name_input
        self.entry.delete(0, END)

        self.entry.grid_forget()
        self.start_button.grid_forget()

        # reusing existing elements
        self.header_label['text'] = 'The Red Sparrow welcomes you, {name}'.format(name=self.player.name)
        self.start_button['text'] = 'Begin'
        self.start_button['command'] = self.new_round

        self.start_button.grid(row=4, column=1)
        self.message_label.grid(row=2, column=1)
        self.player_money_label.grid(row=3, column=2)
        self.dealer_money_label.grid(row=3, column=0)
        self.pot_label.grid(row=3, column=1)
        return

    def bet(self):
        """Clears variables and starts a new round on valid bet"""
        try:
            amount = int(self.entry.get())
            if amount > self.player.chips:
                self.error_message_label['text'] = 'Not enough money'
                self.error_message_label.grid(row=6, column=1)
                return

            self.clear_game()
            self.pot += self.player.bet(amount) + self.dealer.bet(amount)

            self.entry.grid_forget()
            self.bet_button.grid_forget()
            self.error_message_label.grid_forget()
            self.entry.delete(0, END)

            self.current_score_label['text'] = 'Current score : 0'
            self.message_label['text'] = 'Best of luck a the blackjack table ;)'
            self.pot_label['text'] = 'Pot :{pot}'.format(pot=self.pot)
            self.update_money_labels()

            self.current_score_label.grid(row=4, column=1)
            self.stay_button.grid(row=4, column=0)
            self.hit_me_button.grid(row=4, column=2)

        except ValueError:
            self.error_message_label['text'] = 'Invalid bet'
            self.error_message_label.grid(row=6, column=1)

        return

    def hit_me(self):
        # hit me --> deal me a card in blackjack
        card = self.dealer.deal_card()
        self.player.add_to_score(card)
        player_score = self.player.current_score

        if player_score < 21:
            pass
        elif player_score == 21:
            self.player.win(self.pot)
            self.message_label['text'] = f'{self.player.name} has Blackjack !'
            self.conclude_round()
        else:
            self.dealer.win(self.pot)
            self.message_label['text'] = f'{self.player.name} busted out'
            self.conclude_round()

        self.current_score_label['text'] = 'Current score : {score}'.format(score=player_score)
        return

    def stay(self):
        player_score = self.player.current_score
        player_points = abs(21 - player_score)
        dealer_points = abs(21 - conclude_game(self.dealer))

        if dealer_points < player_points:
            self.dealer.win(self.pot)
            self.message_label['text'] = f'The dealer was closer to 21. You lose'
        elif dealer_points == player_points:
            self.dealer.win(self.pot / 2)
            self.player.win(self.pot / 2)
            self.message_label['text'] = "It's a tie"
        else:
            self.player.win(self.pot)
            self.message_label[
                'text'] = f"You win ${self.pot}"

        self.current_score_label['text'] = f'Your score : {player_score} \nDealer score {self.dealer.current_score}'

        self.conclude_round()
        return

    def new_round(self):
        self.start_button.grid_forget()

        self.entry.grid(row=5, column=1)
        self.bet_button.grid(row=5, column=2)
        return

    def conclude_round(self):
        self.update_money_labels()
        self.hit_me_button.grid_forget()
        self.stay_button.grid_forget()
        self.new_round()
        return

    def clear_game(self):
        self.dealer.clear_score()
        self.player.clear_score()
        self.pot = 0
        return

    def update_money_labels(self):
        self.dealer_money_label['text'] = f'Dealer money : {self.dealer.chips}'
        self.player_money_label['text'] = f'Player money : {self.player.chips}'
        return


if __name__ == "__main__":
    new_game = SetupGame()
