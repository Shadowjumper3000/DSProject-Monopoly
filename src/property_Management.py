from utils import LinkedList, Node

class Property:
    """
    Property Class.
    Attributes:
    ----------
    name : str
        The name of the property.
    cost : int
        The cost to purchase the property.
    rent : int
        The rent charged when another player lands on the property.
    street_group : str
        The group or color set to which the property belongs.
    owner : str or None
        The owner of the property. None if the property is not owned.
    mortgaged : bool
        Indicates whether the property is mortgaged.
    Methods:
    -------
    return_rent():
        Returns the rent of the property.
    return_cost():
        Returns the cost of the property.
    return_owner():
        Returns the owner of the property.
    mortgage_property():
        Mortgages the property and returns half the cost. Returns -1 if already mortgaged.
    change_owner(new_owner):
        Changes the owner of the property.
    """
    def __init__(self, name, cost, rent, street_group):
        self.name = name
        self.cost = cost
        self.rent = rent
        self.street_group = street_group
        self.owner = None
        self.mortgaged = False

    def return_rent(self):
        return self.rent

    def return_cost(self):
        return self.cost

    def return_owner(self):
        return self.owner

    def change_owner(self, new_owner):
        self.owner = new_owner

    def mortgage_property(self):
        if not self.mortgaged:
            self.mortgaged = True
            return self.cost // 2
        return -1


def initializeProperties():
    properties = LinkedList()
    properties.append(Node(Property("Mediterranean Avenue", 60, 2, 1)))
    properties.append(Node(Property("Baltic Avenue", 60, 4, 1)))
    properties.append(Node(Property("Oriental Avenue", 100, 6, 2)))
    properties.append(Node(Property("Vermont Avenue", 100, 6, 2)))
    properties.append(Node(Property("Connecticut Avenue", 120, 8, 2)))
    properties.append(Node(Property("St. Charles Place", 140, 10, 3)))
    properties.append(Node(Property("States Avenue", 140, 10, 3)))
    properties.append(Node(Property("Virginia Avenue", 160, 12, 3)))
    properties.append(Node(Property("St. James Place", 180, 14, 4)))
    properties.append(Node(Property("Tennessee Avenue", 180, 14, 4)))
    properties.append(Node(Property("New York Avenue", 200, 16, 4)))
    properties.append(Node(Property("Kentucky Avenue", 220, 18, 5)))
    properties.append(Node(Property("Indiana Avenue", 220, 18, 5)))
    properties.append(Node(Property("Illinois Avenue", 240, 20, 5)))
    properties.append(Node(Property("Atlantic Avenue", 260, 22, 6)))
    properties.append(Node(Property("Ventnor Avenue", 260, 22, 6)))
    properties.append(Node(Property("Marvin Gardens", 280, 24, 6)))
    properties.append(Node(Property("Pacific Avenue", 300, 26, 7)))
    properties.append(Node(Property("North Carolina Avenue", 300, 26, 7)))
    properties.append(Node(Property("Pennsylvania Avenue", 320, 28, 7)))
    properties.append(Node(Property("Park Place", 350, 35, 8)))
    properties.append(Node(Property("Boardwalk", 400, 50, 8)))
    return properties
