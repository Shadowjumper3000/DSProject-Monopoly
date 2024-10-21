"""
card_management.py

This module contains the Card class.
"""


class Card:
    """
    A class to represent a card in the Monopoly game.

    Attributes
    ----------
    card_type : str
        The type of the card.
    description : str
        The description of the card.
    value : int
        The value of the card.
    """

    def __init__(self, card_type, description, value):
        """
        Constructs all the necessary attributes for the Card object.

        Parameters
        ----------
        card_type : str
            The type of the card.
        description : str
            The description of the card.
        value : int
            The value of the card.
        """
        self.card_type = card_type
        self.description = description
        self.value = value

    def return_value(self):
        """
        Returns the value of the card.

        Returns
        -------
        int
            The value of the card.
        """
        return self.value

    def return_description(self):
        """
        Returns the description of the card.

        Returns
        -------
        str
            The description of the card.
        """
        return self.description


def initialize_chance_cards():
    """
    Initializes the Chance cards.

    Returns
    -------
    list
        A list of Chance cards.
    """
    chance_cards = [
        Card("Chance Card", "Advance to Go. Collect $200.", 200),
        Card(
            "Chance Card",
            "Advance to Illinois Avenue. If you pass Go, collect $200.",
            0,
        ),
        Card(
            "Chance Card",
            "Advance to St. Charles Place. If you pass Go, collect $200.",
            0,
        ),
        Card(
            "Chance Card",
            """Advance to nearest Utility. If unowned, you may buy it from the Bank.
             If owned, throw dice and pay owner a total ten times the amount thrown.""",
            0,
        ),
    ]
    return chance_cards


def initialize_community_chest_cards():
    """
    Initializes the Community Chest cards.

    Returns
    -------
    list
        A list of Community Chest cards.
    """
    community_chest_cards = [
        Card("Community Chest Card", "Advance to Go. Collect $200.", 200),
        Card("Community Chest Card", "Bank error in your favor. Collect $200.", 200),
        Card("Community Chest Card", "Doctor's fees. Pay $50.", -50),
        Card("Community Chest Card", "From sale of stock you get $50.", 50),
    ]
    return community_chest_cards
