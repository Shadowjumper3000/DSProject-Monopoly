class Estate:
    # Represents a property on the game board
    def __init__(self, name, price, rent, position, group, buyable):
        # Initialize the estate's attributes
        self.name = name
        self.price = price
        self.group = group
        self.rent = rent
        self.house_cost = price // 2
        self.owner = None
        self.houses = 0
        self.hotel = False
        self.mortgaged = False
        self.position = position
        self.buyable = buyable

    def get_current_rent(self, game):
        """Calculate the current rent based on estate type."""
        if self.group == "Utility":
            # Rent is 4 times dice roll if one utility owned, 10 times if both
            utilities_owned = [
                estate for estate in game.estates
                if estate.group == "Utility" and estate.owner == self.owner
            ]
            # Use average dice roll of 7 for estimation
            dice_roll_estimate = 7
            multiplier = 4 if len(utilities_owned) == 1 else 10
            rent = multiplier * dice_roll_estimate
        elif self.group == "Station":
            # Rent depends on number of stations owned
            stations_owned = [
                estate for estate in game.estates
                if estate.group == "Station" and estate.owner == self.owner
            ]
            rent = 25 * len(stations_owned)
        else:
            rent = self.rent
            if self.hotel:
                rent *= 5
            elif self.houses > 0:
                rent *= self.houses
        return rent

    def pay_rent(self, player):
        # Handles the payment of rent when a player lands on the estate
        if self.owner is not None and self.owner != player and not self.mortgaged:
            rent_to_pay = self.rent
            if self.hotel:
                rent_to_pay *= 5
            elif self.houses > 0:
                rent_to_pay *= self.houses
            
            # Check if the player can afford the rent
            if player.balance >= rent_to_pay:
                player.balance -= rent_to_pay
                self.owner.balance += rent_to_pay
                print(f"{player.name} paid ${rent_to_pay} in rent to {self.owner.name}")
            else:
                print(f"{player.name} does not have enough money to pay rent")
                return False
        return True

    def build_house(self, game):
        # Allows the owner to build a house or upgrade to a hotel
        group_estates = [estate for estate in game.estates if estate.group == self.group]
        
        # Check if the owner owns all estates in the group
        if all(estate.owner == self.owner for estate in group_estates):
            if self.houses < 4 and not self.hotel:
                self.houses += 1
                return True
            elif self.houses == 4:
                self.hotel = True
                self.houses = 0
                return True
        return False

    def mortgage(self):
        # Mortgages the estate to gain funds
        if not self.mortgaged:
            self.mortgaged = True
            return True
        return False

    def unmortgage(self):
        # Unmortgages the estate
        if self.mortgaged:
            self.mortgaged = False
            return True
        return False

    def __str__(self):
        # Provides a string representation of the estate
        return f"{self.name} - Price: {self.price}, Rent: {self.rent}, Houses: {self.houses}, Hotel: {self.hotel}, Owner: {self.owner.name if self.owner else 'None'}"


def initialize_estates():
    # Creates a list of estates with their respective properties
    board_size = 700
    estate_width = 58  # Width of each estate
    corner_width = estate_width * 1.5  # Width of corner estates
    offset = 30  # Small offset for x and y coordinates

    # List of estate objects with details such as name, price, rent, position, etc.
    estates = [
        Estate(
            "Go",
            0,
            0,
            (board_size - corner_width + offset, board_size - corner_width + offset),
            group="Corner",
            buyable=False,
        ),
        Estate(
            "Old Kent Road",
            60,
            2,
            (
                board_size - corner_width - estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Brown",
            buyable=True,
        ),
        Estate(
            "Community Chest",
            0,
            0,
            (
                board_size - corner_width - 2 * estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Community Chest",
            buyable=False,
        ),
        Estate(
            "Whitechapel Road",
            60,
            4,
            (
                board_size - corner_width - 3 * estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Brown",
            buyable=True,
        ),
        Estate(
            "Income Tax",
            200,
            0,
            (
                board_size - corner_width - 4 * estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Tax",
            buyable=False,
        ),
        Estate(
            "Kings Cross Station",
            200,
            25,
            (
                board_size - corner_width - 5 * estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Station",
            buyable=True,
        ),
        Estate(
            "The Angel Islington",
            100,
            6,
            (
                board_size - corner_width - 6 * estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Light Blue",
            buyable=True,
        ),
        Estate(
            "Chance",
            0,
            0,
            (
                board_size - corner_width - 7 * estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Chance",
            buyable=False,
        ),
        Estate(
            "Euston Road",
            100,
            6,
            (
                board_size - corner_width - 8 * estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Light Blue",
            buyable=True,
        ),
        Estate(
            "Pentonville Road",
            120,
            8,
            (
                board_size - corner_width - 9 * estate_width + offset,
                board_size - corner_width + offset,
            ),
            group="Light Blue",
            buyable=True,
        ),
        Estate(
            "Jail",
            0,
            0,
            (0 + offset, board_size - corner_width + offset),
            group="Corner",
            buyable=False,
        ),
        Estate(
            "Pall Mall",
            140,
            10,
            (0 + offset, board_size - corner_width - estate_width + offset),
            group="Pink",
            buyable=True,
        ),
        Estate(
            "Electric Company",
            150,
            0,
            (0 + offset, board_size - corner_width - 2 * estate_width + offset),
            group="Utility",
            buyable=True,
        ),
        Estate(
            "Whitehall",
            140,
            10,
            (0 + offset, board_size - corner_width - 3 * estate_width + offset),
            group="Pink",
            buyable=True,
        ),
        Estate(
            "Northumberland Avenue",
            160,
            12,
            (0 + offset, board_size - corner_width - 4 * estate_width + offset),
            group="Pink",
            buyable=True,
        ),
        Estate(
            "Marylebone Station",
            200,
            25,
            (0 + offset, board_size - corner_width - 5 * estate_width + offset),
            group="Station",
            buyable=True,
        ),
        Estate(
            "Bow Street",
            180,
            14,
            (0 + offset, board_size - corner_width - 6 * estate_width + offset),
            group="Orange",
            buyable=True,
        ),
        Estate(
            "Community Chest",
            0,
            0,
            (0 + offset, board_size - corner_width - 7 * estate_width + offset),
            group="Community Chest",
            buyable=False,
        ),
        Estate(
            "Marlborough Street",
            180,
            14,
            (0 + offset, board_size - corner_width - 8 * estate_width + offset),
            group="Orange",
            buyable=True,
        ),
        Estate(
            "Vine Street",
            200,
            16,
            (0 + offset, board_size - corner_width - 9 * estate_width + offset),
            group="Orange",
            buyable=True,
        ),
        Estate(
            "Free Parking",
            0,
            0,
            (0 + offset, 0 + offset),
            group="Corner",
            buyable=False,
        ),
        Estate(
            "Strand",
            220,
            18,
            (corner_width + offset, 0 + offset),
            group="Red",
            buyable=True,
        ),
        Estate(
            "Chance",
            0,
            0,
            (corner_width + estate_width + offset, 0 + offset),
            group="Chance",
            buyable=False,
        ),
        Estate(
            "Fleet Street",
            220,
            18,
            (corner_width + 2 * estate_width + offset, 0 + offset),
            group="Red",
            buyable=True,
        ),
        Estate(
            "Trafalgar Square",
            240,
            20,
            (corner_width + 3 * estate_width + offset, 0 + offset),
            group="Red",
            buyable=True,
        ),
        Estate(
            "Fenchurch St. Station",
            200,
            25,
            (corner_width + 4 * estate_width + offset, 0 + offset),
            group="Station",
            buyable=True,
        ),
        Estate(
            "Leicester Square",
            260,
            22,
            (corner_width + 5 * estate_width + offset, 0 + offset),
            group="Yellow",
            buyable=True,
        ),
        Estate(
            "Coventry Street",
            260,
            22,
            (corner_width + 6 * estate_width + offset, 0 + offset),
            group="Yellow",
            buyable=True,
        ),
        Estate(
            "Water Works",
            150,
            0,
            (corner_width + 7 * estate_width + offset, 0 + offset),
            group="Utility",
            buyable=True,
        ),
        Estate(
            "Piccadilly",
            280,
            24,
            (corner_width + 8 * estate_width + offset, 0 + offset),
            group="Yellow",
            buyable=True,
        ),
        Estate(
            "Go to Jail",
            0,
            0,
            (board_size - corner_width + offset, 0 + offset),
            group="Corner",
            buyable=False,
        ),
        Estate(
            "Regent Street",
            300,
            26,
            (board_size - corner_width + offset, corner_width + offset),
            group="Green",
            buyable=True,
        ),
        Estate(
            "Oxford Street",
            300,
            26,
            (board_size - corner_width + offset, corner_width + estate_width + offset),
            group="Green",
            buyable=True,
        ),
        Estate(
            "Community Chest",
            0,
            0,
            (
                board_size - corner_width + offset,
                corner_width + 2 * estate_width + offset,
            ),
            group="Community Chest",
            buyable=False,
        ),
        Estate(
            "Bond Street",
            320,
            28,
            (
                board_size - corner_width + offset,
                corner_width + 3 * estate_width + offset,
            ),
            group="Green",
            buyable=True,
        ),
        Estate(
            "Liverpool St. Station",
            200,
            25,
            (
                board_size - corner_width + offset,
                corner_width + 4 * estate_width + offset,
            ),
            group="Station",
            buyable=True,
        ),
        Estate(
            "Chance",
            0,
            0,
            (
                board_size - corner_width + offset,
                corner_width + 5 * estate_width + offset,
            ),
            group="Chance",
            buyable=False,
        ),
        Estate(
            "Park Lane",
            350,
            35,
            (
                board_size - corner_width + offset,
                corner_width + 6 * estate_width + offset,
            ),
            group="Dark Blue",
            buyable=True,
        ),
        Estate(
            "Super Tax",
            100,
            0,
            (
                board_size - corner_width + offset,
                corner_width + 7 * estate_width + offset,
            ),
            group="Tax",
            buyable=False,
        ),
        Estate(
            "Mayfair",
            400,
            50,
            (
                board_size - corner_width + offset,
                corner_width + 8 * estate_width + offset,
            ),
            group="Dark Blue",
            buyable=True,
        ),
    ]
    return estates


def initialize_estate_dict(estate_lib):
    # Creates a dictionary mapping estate names to their indices in the estate list
    return {estate.name: index for index, estate in enumerate(estate_lib)}
