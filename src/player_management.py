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
    money: int
        The amount of money a player currently has.
    estates: arr
        The estates the player owns
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

    def buy_estate(self, estate):
        """
        Provides the player the ability to buy a estate if the can afford it.

        Parameters
        ----------
        estate : estate
            The estate object which the player can buy.
        """
        if estate.street_group in range(11, 17) or estate.street_group == 0:
            print(f"{estate.name} is not for sale")
            return
        if estate.owner is not None:
            print(f"{estate.name} is already owned by {estate.owner}")
            return
        if self.money >= estate.cost:
            self.money -= estate.cost
            self.estates.append(estate)
            estate.change_owner(self.name)
            print(f"{self.name} has bought {estate.name}")
            return
        else:
            print(f"{self.name} doesn't have enough money to buy {estate.name}")
            return

    def player_mortgage_estate(self, estate):
        """
        Allows the player to mortgage an estate

        Parameters
        ----------
        estate: estate
            The estate which the player wants to mortgage
        """
        if estate in self.estates:
            mortgage = estate.mortage_estate()
            if mortgage is None:
                print("Unable to mortgage estate, because it has already been mortgaged")
            else:
                self.money += mortgage
                print(f"estate has been mortgaged. {mortgage} has been added to you money")
        else:
            print(f"Unable to mortgage estate, {self.name} does not own this estate")

    def player_unmortgage_estate(self, estate):
        """
        Allows the player to unmortgage a estate

        Parameters
        ----------
        estate: estate
            The estate which the player wants to unmortgage
        """
        if estate in self.estates:
            mortgage = estate.unmortage_estate()
            if mortgage is None:
                print("Unable to unmortgage estate, because it has not been mortgaged")
            else:
                self.money -= mortgage
                print(f"estate has been unmortgaged. {mortgage} has been deducted from you money")
        else:
            print(f"Unable to umortgage estate, {self.name} does not own this estate")

    def pay_rent(self, rent_amount, owner):
        """
        Allows the player to pay rent

        Parameters
        ----------
        rent_amount: int
            The amount of rent the player must pay
        owner: 
            The player who owns the estate and collects the rent
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

    def sell_estate(self, estate, buyer_player, estate_cost):
        """
        Allows the player to sell estates with another player

        Parameters
        ----------
        estate: estate
            The estate the player wants to sell
        buyer_player: Player
            The player the player wants to sell with
        estate_cost: int
            The cost of the estate
        """
        if buyer_player.money < estate_cost:
            print(f"{buyer_player.name} does not have enough money to buy {estate.name}")
            return -1
        if estate in self.estates:
            self.estates.remove(estate)
            buyer_player.estates.append(estate)
            buyer_player.money -= estate_cost
            self.money += estate_cost
            print(f"{self.name} has sold {estate.name} to {buyer_player.name} for {estate.cost}")
        else:
            print(f"{self.name} does not own {estate.name}")
            return -1
        return 0
