class Estate:
    def __init__(self, name, price, rent, position, group):
        self.name = name
        self.price = price
        self.group = group
        self.rent = rent
        if group in ["Brown", "Light Blue", "Pink", "Orange", "Red", "Yellow", "Green", "Dark Blue", "Station", "Utility"]:
            self.owner = None
        else:
            self.owner = "Bank"
        self.houses = 0
        self.hotel = False
        self.mortgaged = False
        self.position = position

    def buy_estate(self, player):
        if self.owner is None:
            if player.balance >= self.price:
                player.balance -= self.price
                self.owner = player
                player.properties.append(self)
                return True
            else:
                return False
        else:
            return False

    def pay_rent(self, player):
        if self.owner is not None and self.owner != player:
            rent_to_pay = self.rent
            if self.hotel:
                rent_to_pay *= 5
            elif self.houses > 0:
                rent_to_pay *= self.houses
            player.balance -= rent_to_pay
            self.owner.balance += rent_to_pay

    def build_house(self):
        if self.houses < 4 and not self.hotel:
            self.houses += 1
            return True
        elif self.houses == 4:
            self.hotel = True
            self.houses = 0
            return True
        else:
            return False

    def mortgage(self):
        if not self.mortgaged:
            self.mortgaged = True
            return True
        return False

    def unmortgage(self):
        if self.mortgaged:
            self.mortgaged = False
            return True
        return False

    def __str__(self):
        return f"{self.name} - Price: {self.price}, Rent: {self.rent}, Houses: {self.houses}, Hotel: {self.hotel}, Owner: {self.owner.name if self.owner else 'None'}"


def initialize_estates():
    board_size = 700
    estate_width = 58  # Width of each estate
    corner_width = estate_width * 1.5  # Width of corner estates
    offset = 30  # Small offset for x and y coordinates

    estates = [
        # Bottom row (0-10)
        Estate("Go", 0, 0, (board_size - corner_width + offset, board_size - corner_width + offset), group="Corner"),
        Estate("Old Kent Road", 60, 2, (board_size - corner_width - estate_width + offset, board_size - corner_width + offset), group="Brown"),
        Estate("Community Chest", 0, 0, (board_size - corner_width - 2 * estate_width + offset, board_size - corner_width + offset), group="Community Chest"),
        Estate("Whitechapel Road", 60, 4, (board_size - corner_width - 3 * estate_width + offset, board_size - corner_width + offset), group="Brown"),
        Estate("Income Tax", 200, 0, (board_size - corner_width - 4 * estate_width + offset, board_size - corner_width + offset), group="Tax"),
        Estate("Kings Cross Station", 200, 25, (board_size - corner_width - 5 * estate_width + offset, board_size - corner_width + offset), group="Station"),
        Estate("The Angel Islington", 100, 6, (board_size - corner_width - 6 * estate_width + offset, board_size - corner_width + offset), group="Light Blue"),
        Estate("Chance", 0, 0, (board_size - corner_width - 7 * estate_width + offset, board_size - corner_width + offset), group="Chance"),
        Estate("Euston Road", 100, 6, (board_size - corner_width - 8 * estate_width + offset, board_size - corner_width + offset), group="Light Blue"),
        Estate("Pentonville Road", 120, 8, (board_size - corner_width - 9 * estate_width + offset, board_size - corner_width + offset), group="Light Blue"),

        # Left column (11-20)
        Estate("Jail", 0, 0, (0 + offset, board_size - corner_width + offset), group="Corner"),
        Estate("Pall Mall", 140, 10, (0 + offset, board_size - corner_width - estate_width + offset), group="Pink"),
        Estate("Electric Company", 150, 0, (0 + offset, board_size - corner_width - 2 * estate_width + offset), group="Utility"),
        Estate("Whitehall", 140, 10, (0 + offset, board_size - corner_width - 3 * estate_width + offset), group="Pink"),
        Estate("Northumberland Avenue", 160, 12, (0 + offset, board_size - corner_width - 4 * estate_width + offset), group="Pink"),
        Estate("Marylebone Station", 200, 25, (0 + offset, board_size - corner_width - 5 * estate_width + offset), group="Station"),
        Estate("Bow Street", 180, 14, (0 + offset, board_size - corner_width - 6 * estate_width + offset), group="Orange"),
        Estate("Community Chest", 0, 0, (0 + offset, board_size - corner_width - 7 * estate_width + offset), group="Community Chest"),
        Estate("Marlborough Street", 180, 14, (0 + offset, board_size - corner_width - 8 * estate_width + offset), group="Orange"),
        Estate("Vine Street", 200, 16, (0 + offset, board_size - corner_width - 9 * estate_width + offset), group="Orange"),

        # Top row (21-30)
        Estate("Free Parking", 0, 0, (0 + offset, 0 + offset), group="Corner"),
        Estate("Strand", 220, 18, (corner_width + offset, 0 + offset), group="Red"),
        Estate("Chance", 0, 0, (corner_width + estate_width + offset, 0 + offset), group="Chance"),
        Estate("Fleet Street", 220, 18, (corner_width + 2 * estate_width + offset, 0 + offset), group="Red"),
        Estate("Trafalgar Square", 240, 20, (corner_width + 3 * estate_width + offset, 0 + offset), group="Red"),
        Estate("Fenchurch St. Station", 200, 25, (corner_width + 4 * estate_width + offset, 0 + offset), group="Station"),
        Estate("Leicester Square", 260, 22, (corner_width + 5 * estate_width + offset, 0 + offset), group="Yellow"),
        Estate("Coventry Street", 260, 22, (corner_width + 6 * estate_width + offset, 0 + offset), group="Yellow"),
        Estate("Water Works", 150, 0, (corner_width + 7 * estate_width + offset, 0 + offset), group="Utility"),
        Estate("Piccadilly", 280, 24, (corner_width + 8 * estate_width + offset, 0 + offset), group="Yellow"),

        # Right column (31-40)
        Estate("Go to Jail", 0, 0, (board_size - corner_width + offset, 0 + offset), group="Corner"),
        Estate("Regent Street", 300, 26, (board_size - corner_width + offset, corner_width + offset), group="Green"),
        Estate("Oxford Street", 300, 26, (board_size - corner_width + offset, corner_width + estate_width + offset), group="Green"),
        Estate("Community Chest", 0, 0, (board_size - corner_width + offset, corner_width + 2 * estate_width + offset), group="Community Chest"),
        Estate("Bond Street", 320, 28, (board_size - corner_width + offset, corner_width + 3 * estate_width + offset), group="Green"),
        Estate("Liverpool St. Station", 200, 25, (board_size - corner_width + offset, corner_width + 4 * estate_width + offset), group="Station"),
        Estate("Chance", 0, 0, (board_size - corner_width + offset, corner_width + 5 * estate_width + offset), group="Chance"),
        Estate("Park Lane", 350, 35, (board_size - corner_width + offset, corner_width + 6 * estate_width + offset), group="Dark Blue"),
        Estate("Super Tax", 100, 0, (board_size - corner_width + offset, corner_width + 7 * estate_width + offset), group="Tax"),
        Estate("Mayfair", 400, 50, (board_size - corner_width + offset, corner_width + 8 * estate_width + offset), group="Dark Blue"),
    ]

    return estates