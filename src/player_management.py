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
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.community_chest_cards = []  # List to store picked-up Community Chest cards

    def update_balance(self, amount):
        self.balance += amount

    def add_community_chest_card(self, card):
        self.community_chest_cards.append(card)

    def buy_property(self, property):
        if self.balance >= property.price:
            self.balance -= property.price
            self.properties.append(property)
            property.owner = self
        else:
            print(f"{self.name} does not have enough money to buy {property.name}")

    def go_to_jail(self):
        self.position = 10  # Jail position
        self.in_jail = True
        self.jail_turns = 0

    def get_out_of_jail(self):
        self.in_jail = False
        self.jail_turns = 0

    def __str__(self):
        return f"Player {self.name}: Position {self.position}, Balance {self.balance}, Properties {len(self.properties)}, In Jail {self.in_jail}"
