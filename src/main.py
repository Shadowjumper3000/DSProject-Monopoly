"""
main.py

This is the main file for the project and will contain Game logic.
"""
import random

import player_management
import estate_management


class Game:
    def __init__(self):
        self.players = []
        self.estates = estate_management.initialize_estates()
        self.current_player_index = 0

    def add_player(self):
        if not self.players:
            player_id = 0
        else:
            player_id = self.players[-1].player_id + 1
        name = input("Enter player name: ")
        player = player_management.Player(player_id, name)
        self.players.append(player)

    def roll_dice(self):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        print(f"You rolled: {d1} and {d2} for a total of {d1 + d2}")
        return d1 + d2

    def move_player(self, player, steps):
        player.position = (player.position + steps) % len(self.estates)
        if player.position + steps >= len(self.estates):
            player.money += 200
            print(f"{player.name} passed Go and collected $200")
        current_property = self.estates[player.position]
        print(f"{player.name} landed on {current_property.name}")

    def play_turn(self):
        player = self.players[self.current_player_index]
        print("-" * 20)
        print(f"{player.name}'s turn")
        self.move_player(player, self.roll_dice())
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"{player.name} has ${player.money}")
        action = input(f"Do you want to (B)uy {self.estates[player.position].name} for {self.estates[player.position].cost}, (T)rade, or (M)ortgage a property? (Enter to skip): ").upper()
        if action == 'B':
            player.buy_estate(self.estates[player.position])
        elif action == 'T':
            trade_action = input("Do you want to (B)uy or (S)ell a property? ").upper()
            if trade_action == 'B':
                player.sell_estate(player)
            elif trade_action == 'S':
                player.sell_estate(player)
        elif action == 'M':
            player.mortgage_property(player)
        print(f"{player.name} has ${player.money} left")
        print("-" * 20)

    def start_game(self):
        while not self.is_game_over():
            self.play_turn()

    def is_game_over(self):
        # Define game over condition
        return False


if __name__ == "__main__":
    game = Game()
    game.add_player()
    game.add_player()
    game.start_game()
