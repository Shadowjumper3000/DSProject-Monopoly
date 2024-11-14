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

    def buy_estate(self, estate):
        if self.balance >= estate.price:
            self.balance -= estate.price
            estate.owner = self
            self.insert_estate_sorted(estate)
        else:
            print(f"{self.name} does not have enough money to buy {estate.name}")

    def insert_estate_sorted(self, estate):
        # Use insertion sort to insert the estate in the correct position
        self.estates.append(estate)
        i = len(self.estates) - 1
        while i > 0 and self.estates[i - 1].name > estate.name:
            self.estates[i] = self.estates[i - 1]
            i -= 1
        self.estates[i] = estate

    def go_to_jail(self, game):
        self.position = game.get_estate_position_by_name("Jail")
        self.in_jail = True
        self.jail_turns = 0

    def get_out_of_jail(self):
        self.in_jail = False
        self.jail_turns = 0

    def handle_jail_turn(self):
        if self.in_jail:
            self.jail_turns += 1
            if self.jail_turns >= 3:
                self.get_out_of_jail()
                print(f"{self.name} is released from jail after 3 turns")
            else:
                print(f"{self.name} is in jail for {self.jail_turns} turns")

    def __str__(self):
        return f"Player {self.name}: Position {self.position}, Balance {self.balance}, Properties {len(self.estates)}, In Jail {self.in_jail}"
