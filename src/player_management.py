"""
Player class to manage player information and actions
"""


class Player:
    """
    Player class to manage player information and actions
    """

    def __init__(self, name, color, initial_balance=1500):
        self.name = name
        self.color = color
        self.balance = initial_balance
        self.position = 0
        self.estates = []
        self.in_jail = False
        self.jail_turns = 0
        self.community_chest_cards = []  # List to store picked-up Community Chest cards

    def update_balance(self, amount):
        self.balance += amount

    def add_community_chest_card(self, card):
        self.community_chest_cards.append(card)

    def insert_estate_sorted(self, estate, game):
        # Use insertion sort to insert the estate in the correct position based on index in the game's estates list
        estate_index = game.estates.index(estate)
        self.estates.append(estate)
        i = len(self.estates) - 1
        while i > 0 and game.estates.index(self.estates[i - 1]) > estate_index:
            self.estates[i] = self.estates[i - 1]
            i -= 1
        self.estates[i] = estate

    def get_total_repair_cost(self, house_cost, hotel_cost):
        total_cost = 0
        for estate in self.estates:
            if estate.hotel:
                total_cost += hotel_cost
            else:
                total_cost += estate.houses * house_cost
        return total_cost

    def __str__(self):
        return f"Player {self.name}: Position {self.position}, Balance {self.balance}, Properties {len(self.estates)}, In Jail {self.in_jail}"
