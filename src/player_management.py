"""
Player class to manage player information and actions
"""


class Player:
    """
    Player class to manage player information and actions
    """

    def __init__(self, name, color, initial_balance=1500):
        """
        Initializes a new player with the given name, color, and initial balance.
        :param name: The name of the player.
        :param color: The color representing the player.
        :param initial_balance: The initial balance of the player (default is 1500).
        """
        self.name = name
        self.color = color
        self.balance = initial_balance
        self.position = 0
        self.estates = []
        self.in_jail = False
        self.jail_turns = 0
        self.community_chest_cards = []  # List to store picked-up Community Chest cards

    def update_balance(self, amount):
        """
        Updates the player's balance by adding the specified amount.
        :param amount: The amount to add (or subtract if negative).

        O(1)
        """
        self.balance += amount

    def add_community_chest_card(self, card):
        """
        Adds a Community Chest card to the player's collection.
        :param card: The Community Chest card to add.

        O(1)
        """
        self.community_chest_cards.append(card)

    def insert_estate_sorted(self, estate, game):
        """
        Adds an estate to the player's owned properties list, maintaining order by its index
        on the game's estate list (using insertion sort).
        :param estate: The estate to add to the player's list.
        :param game: The game object containing the master list of estates.

        O(n): where n is the number of estates owned by the player
        """

        # Get the index of the estate in the game's estate list
        estate_index = game.estates.index(estate)

        # Append the estate to the player's estates list
        self.estates.append(estate)

        # Use insertion sort to keep the list ordered by the estate index
        i = len(self.estates) - 1
        while i > 0 and game.estates.index(self.estates[i - 1]) > estate_index:
            self.estates[i] = self.estates[i - 1]
            i -= 1
        self.estates[i] = estate  # Place the new estate in its correct position

    def get_total_repair_cost(self, house_cost, hotel_cost):
        """
        Calculates the total cost for repairing all the player's properties.
        :param house_cost: The cost to repair one house.
        :param hotel_cost: The cost to repair one hotel.
        :return: The total repair cost for all properties owned by the player.

        O(n): where n is the number of estates owned by the player
        """
        total_cost = 0
        for estate in self.estates:
            if estate.hotel:
                total_cost += hotel_cost  # Add hotel repair cost if estate has a hotel
            else:
                total_cost += estate.houses * house_cost  # Add house repair cost
        return total_cost

    def __str__(self):
        """
        Returns a string representation of the player's current state.
        :return: A string containing the player's name, position, balance, number of properties, and jail status.
        """
        return f"Player {self.name}: Position {self.position}, Balance {self.balance}, Properties {len(self.estates)}, In Jail {self.in_jail}"
