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

    def add_player(self, name):
        player_id = len(self.players) + 1
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
        current_estate = self.estates[player.position]
        print(f"{player.name} landed on {current_estate.name}")
        if current_estate.owner is not None:
            print(f"{current_estate.name} is owned by {current_estate.owner}")
            if current_estate.owner != player:
                rent = current_estate.rent
                print(f"{player.name} paid {current_estate.owner.name} ${rent}")
                player.money -= rent
                current_estate.owner.money += rent
        if current_estate.street_group == 15:
            print("You landed on Free Parking! You get $500!")
            player.money += 500
        elif current_estate.street_group == 16:
            print("You landed on Jail! You are now in Jail.")
            player.in_jail = True
        elif current_estate.street_group == 16:
            print("You landed on Go to Jail! You are now in Jail.")
            player.in_jail = True

    def play_turn(self):
        player = self.players[self.current_player_index]
        print("-" * 20)
        print(f"{player.name}'s turn")

        self.move_player(player, self.roll_dice())

        print(f"{player.name} has ${player.money}")
        print(f"{player.name} currently owns: {[estate.name for estate in player.properties]}")

        while True:
            action = input(f"Do you want to (B)uy {self.estates[player.position].name} for {self.estates[player.position].cost}, (T)rade, or (M)ortgage a property? (Enter to skip): ").upper()
            if action == 'B':
                player.buy_estate(player, self.estates[player.position])
            elif action == 'T':
                trade_with = input("Enter the name of the player you want to trade with: ")
                trade_player = next((p for p in self.players if p.name == trade_with), None)
                if trade_player:
                    trade_property = input(f"Enter the name of the property you want to trade with {trade_player.name}: ")
                    property_to_trade = next((estate for estate in player.properties if estate.name == trade_property), None)
                    if property_to_trade:
                        offer = int(input(f"How much money do you offer to {trade_player.name} for {property_to_trade.name}? "))
                        if offer <= player.money:
                            trade_player.properties.append(property_to_trade)
                            player.properties.remove(property_to_trade)
                            player.money -= offer
                            trade_player.money += offer
                            print(f"{player.name} traded {property_to_trade.name} with {trade_player.name} for ${offer}")
                        else:
                            print("You don't have enough money to make this offer.")
                    else:
                        print(f"You don't own {trade_property}.")
                else:
                    print(f"No player named {trade_with} found.")
            elif action == 'M':
                if player.properties:
                    print("Properties you can mortgage:")
                    for i, estate in enumerate(player.properties, 1):
                        print(f"{i}. {estate.name} (Mortgage value: ${estate.mortgage_value})")
                    choice = int(input("Enter the number of the property you want to mortgage: ")) - 1
                    if 0 <= choice < len(player.properties):
                        property_to_mortgage = player.properties[choice]
                        player.money += property_to_mortgage.mortgage_value
                        property_to_mortgage.is_mortgaged = True
                        print(f"{player.name} mortgaged {property_to_mortgage.name} for ${property_to_mortgage.mortgage_value}")
                    else:
                        print("Invalid choice.")
                else:
                    print("You don't have any properties to mortgage.")
            elif action == '':
                break
            else:
                print("Invalid action. Please choose (B)uy, (T)rade, (M)ortgage, or press Enter to skip.")


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
