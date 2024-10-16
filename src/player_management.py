"""
player_management.py

This module contains the Player class.
"""


class Player:
    """"
    A class to represent the player in the Monopoly game.

    Attributes
    ----------
    player_id : int
        The players id (player 1, 2, etc.)
    name : str
        The name of the player
    money: int or float?
        The amount of money a player currently has.
    properties: arr
        The properties the player owns
    in_jail : bool
        Is the player currently in jail
    jail_free_cards : int
        The number of "get out of jail" cards the player has
    """

    def __init__(self, player_id, name, initial_money=1500):
        """
        Constructs the necessary attributes of the player object

        Parameters
        ----------
        player_id: int
            The unique player identifier
        name: str
            The players chosen name
        initial_money: int
            The amount of money all players start the game with
        """

        self.player_id = player_id
        self.name = name
        self.money = initial_money
        self.position = 0
        self.estates = []
        self.in_jail = False
        self.jail_free_cards = 0

    def move(self, steps):
        """
        Allows the player to move around the board

        Parameters
        ----------
        steps : int
            The number of places the player is going to move. Checks if player passes go.
        """
        self.position = (self.position + steps) % 40
        if self.position + steps >= 40:
            self.pass_go()

    def pass_go(self):
        """
        Provides player with money for passing go
        """
        self.money += 200

    def buy_propert(self, estate):
        """
        Provides the player the ability to buy a property if the can afford it.

        Parameters
        ----------
        property : property
            The property object which the player can buy.
        """
        if self.money >= estate.cost:
            self.money -= estate.cost
            self.estates.append(estate)
            print(f"{self.name} has bought {estate.name}")
        else:
            print(f"{self.name} doesn't have enough money to buy {estate.name}")

    def player_mortgage_property(self, estate):
        """
        Allows the player to mortgage a property

        Parameters
        ----------
        property: Property
            The property which the player wants to mortgage
        """
        if property in self.estates:
            mortgage = estate.mortage_property()
            if mortgage == -1:
                print("Unable to mortgage property, because it has already been mortgaged")
            else:
                self.money += mortgage
                print(f"Property has been mortgaged. {mortgage} has been added to you money")
        else:
            print(f"Unabel to mortgage propert, {self.name} does not own this property")

    def player_unmortgage_property(self, estate):
        """
        Allows the player to unmortgage a property

        Parameters
        ----------
        property: Property
            The property which the player wants to unmortgage
        """
        if property in self.estates:
            mortgage = estate.unmortage_property()
            if mortgage == -1:
                print("Unable to unmortgage property, because it has not been mortgaged")
            else:
                self.money -= mortgage
                print(f"Property has been unmortgaged. {mortgage} has been deducted from you money")
        else:
            print(f"Unable to umortgage property, {self.name} does not own this property")

    def pay_rent(self, rent_amount, owner):
        """
        Allows the player to pay rent

        Parameters
        ----------
        rent_amount: int
            The amount of rent the player must pay
        owner: 
            The player who owns the property and collects the rent
        """
        if self.money >= rent_amount:
            self.money -= rent_amount
            owner.money += rent_amount
            print(f"{self.name} paid {rent_amount} to {owner.name}")
        else:
            print(f"{self.name} can't afford to pay rent")

    def pick_up_card(self, card):
        """
        Allows the player to interact with the prompt on the card

        Parameters
        ----------
        card: Card
            The chance or community chestcard that the player has picked up
        """
        if card.value != 0:
            self.money += card.value
        else:
            # Card class needs to have aditional functionality like change position etc.
            pass

    def go_to_jail(self):
        """
        Player goes to jail if he is on the "go to jail" position
        """
        print(f"{self.name} is going to jail")
        self.position = 10
        self.in_jail = True

    def declare_bankruptcy(self):
        """
        Player can declare bankruptcy to stop playing
        """
        self.money = 0
        self.estates.clear()
        print(f"{self.name} has declared bankrupcty!")


def initialize_player(player_num):
    """
    Function to create a new player

    Parameters
    ----------
    player_num : int
        If players are added in order this is the position in which the player has been added

    Returns
    -------
    new_player : Player
        An instance of the Player class
    """

    username = input(f"Player {player_num}, Please enter your username: ")
    new_player = Player(
        player_id = player_num,
        name = username
    )
    return new_player


def initialize_players():
    """
    Function to initialise the players of the Monopoly game.

    Returns
    -------
    players : list
        A list containing all the players
    """
    players = []
    while True:
        try:
            num_players = int(input("Enter the number of players who will be playing(2-5): "))

            if 2 <= num_players <= 5:
                print("Initialising the game with 3 players...")
                break
            print("The number must be between 2 and 5. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    for i in len(num_players):
        players.append(initialize_player(i))
    return players
