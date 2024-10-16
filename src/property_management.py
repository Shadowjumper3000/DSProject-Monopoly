"""
property_management.py

This module contains the Property class.
"""


class Estate:
    """
    A class to represent a property in the Monopoly game.

    Attributes
    ----------
    name : str
        The name of the property.
    cost : int
        The cost to purchase the property.
    rent : int
        The rent charged when another player lands on the property.
    street_group : int
        The group to which the property belongs.
    owner : str or None
        The owner of the property.
    mortgaged : bool
        Indicates if the property is mortgaged.
    """

    def __init__(self, name, cost, rent, street_group):
        """
        Constructs all the necessary attributes for the Property object.

        Parameters
        ----------
        name : str
            The name of the property.
        cost : int
            The cost to purchase the property.
        rent : int
            The rent charged when another player lands on the property.
        street_group : int
            The group to which the property belongs.
        """
        self.name = name
        self.cost = cost
        self.rent = rent
        self.street_group = street_group
        self.owner = None
        self.mortgaged = False

    def change_owner(self, new_owner):
        """
        Changes the owner of the property.

        Parameters
        ----------
        new_owner : str
            The new owner of the property.
        """
        self.owner = new_owner

    def mortgage_property(self):
        """
        Mortgages the property if it is not already mortgaged.

        Returns
        -------
        int
            Half the cost of the property if it is not mortgaged, otherwise -1.
        """
        if not self.mortgaged:
            self.mortgaged = True
            return self.cost // 2
        return -1

    def unmortgage_property(self):
        """
        Unmortgages the property if it is mortgaged.

        Returns
        -------
        int
            The cost to unmortgage the property if it is mortgaged, otherwise -1.
        """
        if self.mortgaged:
            self.mortgaged = False
            return self.cost // 2
        return -1


def initialize_properties():
    """
    Initializes the properties for the Monopoly game.

    Returns
    -------
    list
        A list containing all the properties.
    """
    properties = []
    properties.append(Estate("Mediterranean Avenue", 60, 2, 1))
    properties.append(Estate("Baltic Avenue", 60, 4, 1))
    properties.append(Estate("Oriental Avenue", 100, 6, 2))
    properties.append(Estate("Vermont Avenue", 100, 6, 2))
    properties.append(Estate("Connecticut Avenue", 120, 8, 2))
    properties.append(Estate("St. Charles Place", 140, 10, 3))
    properties.append(Estate("States Avenue", 140, 10, 3))
    properties.append(Estate("Virginia Avenue", 160, 12, 3))
    properties.append(Estate("St. James Place", 180, 14, 4))
    properties.append(Estate("Tennessee Avenue", 180, 14, 4))
    properties.append(Estate("New York Avenue", 200, 16, 4))
    properties.append(Estate("Kentucky Avenue", 220, 18, 5))
    properties.append(Estate("Indiana Avenue", 220, 18, 5))
    properties.append(Estate("Illinois Avenue", 240, 20, 5))
    properties.append(Estate("Atlantic Avenue", 260, 22, 6))
    properties.append(Estate("Ventnor Avenue", 260, 22, 6))
    properties.append(Estate("Marvin Gardens", 280, 24, 6))
    properties.append(Estate("Pacific Avenue", 300, 26, 7))
    properties.append(Estate("North Carolina Avenue", 300, 26, 7))
    properties.append(Estate("Pennsylvania Avenue", 320, 28, 7))
    properties.append(Estate("Park Place", 350, 35, 8))
    properties.append(Estate("Boardwalk", 400, 50, 8))
    return properties
