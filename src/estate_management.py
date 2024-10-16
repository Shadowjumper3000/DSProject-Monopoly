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
        return -1

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
        return -1


def initialize_estates():
    """
    Initializes the estates for the Monopoly game.

    Returns
    -------
    list
        A list containing all the estates.
    """
    estates = []
    estates.append(Estate("Mediterranean Avenue", 60, 2, 1))
    estates.append(Estate("Baltic Avenue", 60, 4, 1))
    estates.append(Estate("Oriental Avenue", 100, 6, 2))
    estates.append(Estate("Vermont Avenue", 100, 6, 2))
    estates.append(Estate("Connecticut Avenue", 120, 8, 2))
    estates.append(Estate("St. Charles Place", 140, 10, 3))
    estates.append(Estate("States Avenue", 140, 10, 3))
    estates.append(Estate("Virginia Avenue", 160, 12, 3))
    estates.append(Estate("St. James Place", 180, 14, 4))
    estates.append(Estate("Tennessee Avenue", 180, 14, 4))
    estates.append(Estate("New York Avenue", 200, 16, 4))
    estates.append(Estate("Kentucky Avenue", 220, 18, 5))
    estates.append(Estate("Indiana Avenue", 220, 18, 5))
    estates.append(Estate("Illinois Avenue", 240, 20, 5))
    estates.append(Estate("Atlantic Avenue", 260, 22, 6))
    estates.append(Estate("Ventnor Avenue", 260, 22, 6))
    estates.append(Estate("Marvin Gardens", 280, 24, 6))
    estates.append(Estate("Pacific Avenue", 300, 26, 7))
    estates.append(Estate("North Carolina Avenue", 300, 26, 7))
    estates.append(Estate("Pennsylvania Avenue", 320, 28, 7))
    estates.append(Estate("Park Place", 350, 35, 8))
    estates.append(Estate("Boardwalk", 400, 50, 8))
    return estates
