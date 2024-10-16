"""
main.py

This is the main file for the project and will contain Game logic.
"""
import os
import random

import player_management
import estate_management


class Game:
    """
    Class representing the Monopoly game.
    """

    def __init__(self):
        """
        Initialize the game with players, estates, and the current player index.
        """
        self.players = []
        self.estates = estate_management.initialize_estates()
        self.current_player_index = 0

    def add_player(self, name):
        """
        Add a player to the game.

        Args:
            name (str): The name of the player.
        """
        player_id = len(self.players) + 1
        player = player_management.Player(player_id, name)
        self.players.append(player)

    def roll_dice(self):
        """
        Roll two dice and return their sum.

        Returns:
            int: The sum of the two dice.
        """
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        print(f"You rolled: {d1} and {d2} for a total of {d1 + d2}")
        return d1 + d2

    def move_player(self, player, steps):
        """
        Move a player by a given number of steps.

        Args:
            player (Player): The player to move.
            steps (int): The number of steps to move the player.
        """
        player.position = (player.position + steps) % len(self.estates)
        if player.position + steps >= len(self.estates):
            player.money += 200
            print(f"{player.name} passed Go and collected $200")
        current_estate = self.estates[player.position]
        if current_estate.owner is not None and not current_estate.mortgaged:
            print(f"{current_estate.name} is owned by {current_estate.owner}")
            if current_estate.owner != player:
                rent = current_estate.rent
                print(f"{player.name} paid {current_estate.owner.name} ${rent}")
                player.money -= rent
                current_estate.owner.money += rent
        if current_estate.street_group == 15:
            print("You landed on Free Parking! You get $500!")
            player.money += 500
        elif current_estate.street_group == 11:
            print("You landed on a chance card! You get $100!")
        elif current_estate.street_group == 16:
            print("You landed on Go to Jail! You are now in Jail.")
            player.in_jail = True

    def play_turn(self):
        """
        Play a turn for the current player.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        player = self.players[self.current_player_index]
        print("-" * 20)
        print(f"{player.name}'s turn")

        self.move_player(player, self.roll_dice())
        while True:
            print("-" * 20)
            print(f"{player.name} is currently on {self.estates[player.position].name}")
            print(f"{player.name} has ${player.money}")
            print(f"{player.name} currently owns:")
            for estate in player.estates:
                status = "(Mortgaged)" if estate.mortgaged else ""
                print(f"  - {estate.name} {status}")
            action = input(
                f"Do you want to (B)uy {self.estates[player.position].name} for {self.estates[player.position].cost}, (T)rade, or (M)ortgage a property? (Enter to skip): ").upper()
            if action == 'B':
                player.buy_estate(self.estates[player.position])
            elif action == 'T':
                print("Players in the game:")
                for p in self.players:
                    print(f"  - {p.name}")
                trade_with = input("Enter the name of the player you want to trade with: ")
                trade_player = next((p for p in self.players if p.name == trade_with), None)
                if trade_player:
                    trade_action = input(f"Do you want to (B)uy or (S)ell an estate with {trade_player.name}? ").upper()
                    if trade_action == 'B':
                        print(f"{trade_player.name} currently owns:")
                        for estate in trade_player.estates:
                            status = "(Mortgaged)" if estate.mortgaged else ""
                            print(f"  - {estate.name} {status}")
                        trade_estate = input(f"Enter the name of the estate you want to buy from {trade_player.name}: ")
                        estate_to_trade = next((estate for estate in trade_player.estates if estate.name == trade_estate), None)
                        if estate_to_trade:
                            offer = int(input(f"How much money do you offer to {trade_player.name} for {estate_to_trade.name}? "))
                            if offer <= player.money:
                                trade_player.estates.remove(estate_to_trade)
                                player.estates.append(estate_to_trade)
                                player.money -= offer
                                trade_player.money += offer
                                print(f"{player.name} bought {estate_to_trade.name} from {trade_player.name} for ${offer}")
                            else:
                                print("You don't have enough money to make this offer.")
                        else:
                            print(f"{trade_player.name} doesn't own {trade_estate}.")
                    elif trade_action == 'S':
                        trade_estate = input(f"Enter the name of the estate you want to sell to {trade_player.name}: ")
                        estate_to_trade = next((estate for estate in player.estates if estate.name == trade_estate), None)
                        if estate_to_trade:
                            offer = int(input(f"How much money do you want from {trade_player.name} for {estate_to_trade.name}? "))
                            if offer <= trade_player.money:
                                player.estates.remove(estate_to_trade)
                                trade_player.estates.append(estate_to_trade)
                                trade_player.money -= offer
                                player.money += offer
                                print(f"{player.name} sold {estate_to_trade.name} to {trade_player.name} for ${offer}")
                            else:
                                print(f"{trade_player.name} doesn't have enough money to make this offer.")
                        else:
                            print(f"You don't own {trade_estate}.")
                    else:
                        print("Invalid action. Please choose (B)uy or (S)ell.")
                else:
                    print(f"No player named {trade_with} found.")
            elif action == 'M':
                if player.estates:
                    print("Properties you can mortgage:")
                    for i, estate in enumerate(player.estates, 1):
                        print(f"{i}. {estate.name} (Mortgage value: ${estate.cost // 2})")
                    choice = int(input("Enter the number of the property you want to mortgage: ")) - 1
                    if 0 <= choice < len(player.estates):
                        player.estates[choice].mortgage_estate()
                        print(f"{player.name} mortgaged {player.estates[choice].name} for ${player.estates[choice].cost // 2}")
                    else:
                        print("Invalid choice.")
                else:
                    print("You don't have any properties to mortgage.")
            elif action == '':
                break
            else:
                print("Invalid action. Please choose (B)uy, (T)rade, (M)ortgage, or press Enter to skip.")
        self.current_player_index = (self.current_player_index + 1) % len(self.players)


if __name__ == "__main__":
    game = Game()
    num_players = 0
    while num_players < 2 or num_players > 5:
        try:
            num_players = int(input("Enter the number of players (2-5): "))
            if num_players < 2 or num_players > 5:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 2 and 5.")

    for j in range(num_players):
        p_name = input(f"Enter the name for player {j + 1}: ")
        game.add_player(p_name)
    while True:
        game.play_turn()
