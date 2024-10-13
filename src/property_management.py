"""
property_management.py

This module contains the Property class.
"""

class Property:
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


    def return_rent(self):
        """
        Returns the rent of the property.

        Returns
        -------
        int
            The rent of the property.
        """
        return self.rent


    def return_cost(self):
        """
        Returns the cost of the property.

        Returns
        -------
        int
            The cost of the property.
        """
        return self.cost


    def return_owner(self):
        """
        Returns the owner of the property.

        Returns
        -------
        str or None
            The owner of the property.
        """
        return self.owner


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
    properties.append(Property("Mediterranean Avenue", 60, 2, 1))
    properties.append(Property("Baltic Avenue", 60, 4, 1))
    properties.append(Property("Oriental Avenue", 100, 6, 2))
    properties.append(Property("Vermont Avenue", 100, 6, 2))
    properties.append(Property("Connecticut Avenue", 120, 8, 2))
    properties.append(Property("St. Charles Place", 140, 10, 3))
    properties.append(Property("States Avenue", 140, 10, 3))
    properties.append(Property("Virginia Avenue", 160, 12, 3))
    properties.append(Property("St. James Place", 180, 14, 4))
    properties.append(Property("Tennessee Avenue", 180, 14, 4))
    properties.append(Property("New York Avenue", 200, 16, 4))
    properties.append(Property("Kentucky Avenue", 220, 18, 5))
    properties.append(Property("Indiana Avenue", 220, 18, 5))
    properties.append(Property("Illinois Avenue", 240, 20, 5))
    properties.append(Property("Atlantic Avenue", 260, 22, 6))
    properties.append(Property("Ventnor Avenue", 260, 22, 6))
    properties.append(Property("Marvin Gardens", 280, 24, 6))
    properties.append(Property("Pacific Avenue", 300, 26, 7))
    properties.append(Property("North Carolina Avenue", 300, 26, 7))
    properties.append(Property("Pennsylvania Avenue", 320, 28, 7))
    properties.append(Property("Park Place", 350, 35, 8))
    properties.append(Property("Boardwalk", 400, 50, 8))
    return properties
