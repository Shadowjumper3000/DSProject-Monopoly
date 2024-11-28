"""
Card management module
"""

import random
from utils import Queue


class Card:
    def __init__(
        self, description, value=0, is_get_out_of_jail=False, move_to=None, multiplier=1
    ):
        self.description = description
        self.value = value
        self.is_get_out_of_jail = is_get_out_of_jail
        self.move_to = move_to
        self.multiplier = multiplier

    def __str__(self):
        return self.description


class CardDeck:
    def __init__(self):
        self.deck = Queue()

    def add_card(self, card):
        self.deck.enqueue(card)

    def draw_card(self):
        if not self.deck.is_empty():
            return self.deck.dequeue()
        else:
            raise IndexError("The deck is empty")

    def shuffle(self):
        cards = self.deck.display()
        random.shuffle(cards)
        self.deck = Queue()
        for card in cards:
            self.deck.enqueue(card)

    def __len__(self):
        return len(self.deck)


def initialize_chance_cards():
    return [
        Card("Advance to Go. Collect $200", 0, False, "Go"),
        Card(
            "Advance to Pentonville Rd. If you pass Go, collect $200",
            0,
            False,
            "Pentonville Rd",
        ),
        Card(
            "Advance to Bond Street. If you pass Go, collect $200",
            0,
            False,
            "Bond Street",
        ),
        Card(
            "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times the amount thrown.",
            0,
            False,
            "nearest Utility",
        ),
        Card(
            "Advance token to the nearest Railroad and pay owner twice the rental to which they are otherwise entitled. If Railroad is unowned, you may buy it from the Bank.",
            0,
            False,
            "nearest Railroad",
        ),
        Card("Bank pays you dividend of $50", 50, False, None),
        Card("Get out of Jail Free", 0, True, None),
        Card("Go Back 3 Spaces", 0, False, "back 3 spaces"),
        Card("Go to Jail", 0, False, "Jail"),
        Card(
            "Make general repairs on all your property: For each house pay $25, For each hotel $100",
            0,
            False,
            None,
        ),
        Card("Pay poor tax of $15", -15, False, None),
        Card(
            "Take a trip to Kings Cross Station. If you pass Go, collect $200",
            0,
            False,
            "Kings Cross Station",
        ),
        Card(
            "Take a walk on the Vine Street. Advance token to Vine Street",
            0,
            False,
            "Vine Street",
        ),
        Card(
            "You have been elected Chairman of the Board. Pay each player $50",
            -50,
            False,
            None,
        ),
        Card("Your building loan matures. Collect $150", 150, False, None),
        Card("You have won a crossword competition. Collect $100", 100, False, None),
    ]


def create_chance_deck():
    chance_deck = CardDeck()
    for card in initialize_chance_cards():
        chance_deck.add_card(card)
    chance_deck.shuffle()
    return chance_deck


def initialize_community_chest_cards():
    return [
        Card("Advance to Go.", 0, False, "Go"),
        Card("Bank error in your favor. Collect $200", 200, False, None),
        Card("Doctor's fees. Pay $50", -50, False, None),
        Card("From sale of stock you get $50", 50, False, None),
        Card("Get Out of Jail Free", 0, True, None),
        Card("Go to Jail", 0, False, "Jail"),
        Card(
            "Grand Opera Night. Collect $50 from every player for opening night seats",
            0,
            False,
            None,
        ),
        Card("Holiday Fund matures. Receive $100", 100, False, None),
        Card("Income tax refund. Collect $20", 20, False, None),
        Card("It is your birthday. Collect $10 from every player", 0, False, None),
        Card("Life insurance matures – Collect $100", 100, False, None),
        Card("Hospital Fees. Pay $50", -50, False, None),
        Card("School fees. Pay $50", -50, False, None),
        Card("Receive $25 consultancy fee", 25, False, None),
        Card(
            "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own",
            0,
            False,
            None,
        ),
        Card(
            "You have won second prize in a beauty contest. Collect $10",
            10,
            False,
            None,
        ),
    ]


def create_community_chest_deck():
    community_chest_deck = CardDeck()
    for card in initialize_community_chest_cards():
        community_chest_deck.add_card(card)
    community_chest_deck.shuffle()
    return community_chest_deck
