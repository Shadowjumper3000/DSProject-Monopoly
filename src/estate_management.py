"""
estate_management.py

This module contains the estate class.
"""


class Estate:
    """
    A class to represent an estate in the Monopoly game.

    Attributes
    ----------
    name : str
        The name of the estate.
    cost : int
        The cost to purchase the estate.
    rent : int
        The rent charged when another player lands on the estate.
    street_group : int
        The group to which the estate belongs.
    owner : str or None
        The owner of the estate.
    mortgaged : bool
        Indicates if the estate is mortgaged.
    """

    def __init__(self, name, cost, rent, street_group):
        """
        Constructs all the necessary attributes for the estate object.

        Parameters
        ----------
        name : str
            The name of the estate.
        cost : int
            The cost to purchase the estate.
        rent : int
            The rent charged when another player lands on the estate.
        street_group : int
            The group to which the estate belongs.
        """
        self.name = name
        self.cost = cost
        self.rent = rent
        self.street_group = street_group
        self.owner = None
        self.mortgaged = False

    def change_owner(self, new_owner):
        """
        Changes the owner of the estate.

        Parameters
        ----------
        new_owner : str
            The new owner of the estate.
        """
        self.owner = new_owner

    def mortgage_esta(self):
        """
        Mortgages the estate if it is not already mortgaged.

        Returns
        -------
        int
            Half the cost of the estate if it is not mortgaged, otherwise -1.
        """
        if not self.mortgaged:
            self.mortgaged = True
            return self.cost // 2
        return None

    def unmortgage_estate(self):
        """
        Unmortgages the estate if it is mortgaged.

        Returns
        -------
        int
            The cost to unmortgage the estate if it is mortgaged, otherwise -1.
        """
        if self.mortgaged:
            self.mortgaged = False
            return self.cost // 2
        return None


def initialize_estates():
    """
    Initializes the estates for the Monopoly game.

    Returns
    -------
    list
        A list containing all the estates.

    Groups
    ------
        0: Go
        1: Brown
        2: Light Blue
        3: Pink
        4: Orange
        5: Red
        6: Yellow
        7: Green
        8: Blue
        9: Railroads
        10: Utilities
        11: Chance
        12: Community Chest
        13: Tax
        14: Jail
        15: Free Parking
        16: Go to Jail
    """
    estates = []
    estates.append(Estate("Go", 0, 0, 0))
    estates.append(Estate("Old Kent Road", 60, 2, 1))
    estates.append(Estate("Community Chest", 0, 0, 12))
    estates.append(Estate("Whitechapel Road", 60, 4, 1))
    estates.append(Estate("Income Tax", 200, 0, 13))
    estates.append(Estate("Kings Cross Station", 200, 25, 9))
    estates.append(Estate("The Angel Islington", 100, 6, 2))
    estates.append(Estate("Chance", 0, 0, 11))
    estates.append(Estate("Euston Road", 100, 6, 2))
    estates.append(Estate("Pentonville Road", 120, 8, 2))
    estates.append(Estate("Jail", 0, 0, 14))
    estates.append(Estate("Pall Mall", 140, 10, 3))
    estates.append(Estate("Electric Company", 150, 0, 10))
    estates.append(Estate("Whitehall", 140, 10, 3))
    estates.append(Estate("Northumberland Avenue", 160, 12, 3))
    estates.append(Estate("Marylebone Station", 200, 25, 9))
    estates.append(Estate("Bow Street", 180, 14, 4))
    estates.append(Estate("Marlborough Street", 180, 14, 4))
    estates.append(Estate("Vine Street", 200, 16, 4))
    estates.append(Estate("Free Parking", 0, 0, 15))
    estates.append(Estate("Strand", 220, 18, 5))
    estates.append(Estate("Chance", 0, 0, 11))
    estates.append(Estate("Fleet Street", 220, 18, 5))
    estates.append(Estate("Trafalgar Square", 240, 20, 5))
    estates.append(Estate("Fenchurch St. Station", 200, 25, 9))
    estates.append(Estate("Leicester Square", 260, 22, 6))
    estates.append(Estate("Coventry Street", 260, 22, 6))
    estates.append(Estate("Water Works", 150, 0, 10))
    estates.append(Estate("Piccadilly", 280, 24, 6))
    estates.append(Estate("Go to Jail", 0, 0, 16))
    estates.append(Estate("Regent Street", 300, 26, 7))
    estates.append(Estate("Oxford Street", 300, 26, 7))
    estates.append(Estate("Community Chest", 0, 0, 12))
    estates.append(Estate("Bond Street", 320, 28, 7))
    estates.append(Estate("Liverpool St. Station", 200, 25, 9))
    estates.append(Estate("Chance", 0, 0, 11))
    estates.append(Estate("Park Lane", 350, 35, 8))
    estates.append(Estate("Super Tax", 100, 0, 13))
    estates.append(Estate("Mayfair", 400, 50, 8))
    return estates
