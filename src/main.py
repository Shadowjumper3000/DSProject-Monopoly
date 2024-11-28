"""
Main file for the Monopoly game.
"""

import pygame
import random
from player_management import Player
from estate_management import initialize_estates, initialize_estate_dict
from card_management import (
    create_chance_deck,
    create_community_chest_deck,
)
from utils import wrap_text


class Game:
    def __init__(self):
        """Initializes the game by setting up players, estates, decks, and the game board.

        Runtime Complexity:
            - Worst-case O(N): Where N is the total number of estates and players. Initialization involves creating and initializing lists.
            - Average-case O(N): Similar to worst-case as initialization processes a fixed number of items.
        """
        pygame.init()  # Initialize Pygame
        self.screen = pygame.display.set_mode((1000, 700))  # Extended width to 1000
        pygame.display.set_caption("Monopoly")
        self.background = pygame.image.load("src/img/upd_monopoly_board.png")
        self.font = pygame.font.Font(None, 36)
        self.players = []
        self.estates = initialize_estates()
        self.estate_dict = initialize_estate_dict(self.estates)
        self.current_player_index = 0
        self.dice_rolled = False
        self.chance_deck = create_chance_deck()
        self.community_chest_deck = create_community_chest_deck()
        self.current_card = None
        self.buttons = [
            {
                "label": "Roll Dice",
                "action": self.roll_dice,
                "rect": pygame.Rect(730, 20, 120, 50),
                "enabled": True,
            },
            {
                "label": "Buy Property",
                "action": self.handle_buy,
                "rect": pygame.Rect(860, 20, 120, 50),
                "enabled": False,
            },
            {
                "label": "Build House",
                "action": self.handle_build_house,
                "rect": pygame.Rect(730, 80, 120, 50),
                "enabled": False,
            },
            {
                "label": "Mortgage",
                "action": self.handle_mortgage,
                "rect": pygame.Rect(860, 80, 120, 50),
                "enabled": False,
            },
            {
                "label": "Trade",
                "action": self.handle_trade,
                "rect": pygame.Rect(730, 140, 120, 50),
                "enabled": True,
            },
            {
                "label": "End Turn",
                "action": self.end_turn,
                "rect": pygame.Rect(860, 140, 120, 50),
                "enabled": False,
            },
        ]
        self.buttons[0]["enabled"] = True  # Enable "Roll Dice" button
        self.running = True
        self.setup_phase = True
        self.input_box = pygame.Rect(250, 300, 200, 50)
        self.input_text = ""
        self.num_players = 0
        self.current_setup_step = 0
        self.token_colors = ["red", "blue", "green", "yellow"]
        self.current_color_index = 0
        self.current_card = None
        self.mortgage_popup_active = False
        self.mortgage_popup_player = None
        self.trade_popup_active = False
        self.trade_stage = None
        self.trade_with_player = None
        self.trade_property = None
        self.trade_offer = ""
        self.input_active = False

    def mortgage_property(self, player, estate):
        """Mortgages a property for a player and updates their balance accordingly.

        Runtime Complexity:
            - Worst-case O(1): Basic arithmetic and property state changes are constant time operations.
            - Average-case O(1): Same as worst-case.
        """
        if estate.mortgage():
            player.update_balance(estate.price // 2)
            print(f"{player.name} mortgaged {estate.name} for ${estate.price // 2}")
        else:
            print(f"{player.name} could not mortgage {estate.name}")

    def move_to_nearest_utility(self, player):
        """Moves the player token to the nearest utility property.

        Runtime Complexity:
            - Worst-case O(n): Where n is the number of utility properties. Iterates over all utility properties. Utility positions are fixed and can be found in dictirionary.
            - Average-case O(n): Same as worst-case.
        """
        utilities = ["Electric Company", "Water Works"]
        current_position = player.position
        nearest_utility = min(
            utilities,
            key=lambda utility: (
                self.get_estate_position_by_name(utility) - current_position
            )
            % len(self.estates),
        )
        self.move_player_to(player, nearest_utility)

    def move_to_nearest_railroad(self, player):
        """Moves the player token to the nearest railroad property.

        Runtime Complexity:
            - Worst-case O(1): Railroad properties are a fixed small number; calculations involve constant time operations.
            - Average-case O(1): Same as worst-case.
        """
        railroads = [
            "Kings Cross Station",
            "Marylebone Station",
            "Fenchurch St. Station",
            "Liverpool St. Station",
        ]
        current_position = player.position
        nearest_railroad = min(
            railroads,
            key=lambda railroad: (
                self.get_estate_position_by_name(railroad) - current_position
            )
            % len(self.estates),
        )
        self.move_player_to(player, nearest_railroad)

    def go_to_jail(self, player):
        """Sends the player to jail and updates their status.

        Runtime Complexity:
            - Worst-case O(1): Directly updates player's position and status.
            - Average-case O(1): Same as worst-case.
        """
        player.position = self.get_estate_position_by_name("Jail")
        if player.community_chest_cards:
            self.display_message(
                f"{player.name} goes to jail and uses a 'Get Out of Jail Free' card"
            )
            player.community_chest_cards.pop()
            self.get_out_of_jail(player)
        else:
            player.in_jail = True
            player.jail_turns = 0

    def get_out_of_jail(self, player):
        """Releases the player from jail and resets their jail turn counter.

        Runtime Complexity:
            - Worst-case O(1): Updates player's status in constant time.
            - Average-case O(1): Same as worst-case.
        """
        player.in_jail = False
        player.jail_turns = 0

    def handle_jail_turn(self, player):
        """Handles a player's turn if they are currently in jail.

        Runtime Complexity:
            - Worst-case O(1): Checks and updates player's jail status.
            - Average-case O(1): Same as worst-case.
        """
        if player.in_jail:
            player.jail_turns += 1
            if player.jail_turns >= 3:
                self.get_out_of_jail(player)
                print(f"{player.name} is released from jail after 3 turns")
            else:
                self.display_message(
                    f"{player.name} is in jail for {player.jail_turns} turns"
                )
                print(f"{player.name} is in jail for {player.jail_turns} turns")

    def get_estate_position_by_name(self, name):
        """Retrieves the position index of an estate by its name.

        Runtime Complexity:
            - Worst-case O(1): Dictionary lookup is a constant time operation.
            - Average-case O(1): Same as worst-case.
        """
        return self.estate_dict[name]

    def move_player_to(self, player, location_name):
        """Moves a player to a specified location by name.

        Runtime Complexity:
            - Worst-case O(E): Where E is the number of estates. In the worst case, the estate is at the end of the list.
            - Average-case O(E): On average, it may check half of the estates.
        """
        """Move player to a specific location.

        Args:
            player (Player): The player to move.
            location_name (str): The name of the location to move to.
        """
        try:
            target_position = next(
                i
                for i, estate in enumerate(self.estates)
                if estate.name == location_name
            )
            old_position = player.position
            steps = (target_position - old_position) % len(self.estates)
            self.move_player(player, steps)
            self.handle_estate(player)
        except StopIteration:
            print(f"Estate with name '{location_name}' not found")

    def draw_player_info(self):
        """Displays the current player's information, including properties and cards.

        Runtime Complexity:
            - Worst-case O(P): Where P is the number of properties and cards the player has. Iterates over properties and cards.
            - Average-case O(P): Same as worst-case.
        """
        current_player = self.players[self.current_player_index]
        info_x = 720
        info_y = 230  # Start at the top of the right side
        line_height = 30

        # Clear the entire right side of the board
        pygame.draw.rect(self.screen, (255, 255, 255), (info_x - 20, 0, 300, 700))

        # Draw buttons
        self.draw_buttons()

        # Draw current player name
        name_text = self.font.render(f"Player: {current_player.name}", True, (0, 0, 0))
        self.screen.blit(name_text, (info_x, info_y))
        info_y += line_height

        # Draw current player cash
        cash_text = self.font.render(
            f"Cash: ${current_player.balance}", True, (0, 0, 0)
        )
        self.screen.blit(cash_text, (info_x, info_y))
        info_y += line_height

        # Draw current player properties
        properties_text = self.font.render("Properties:", True, (0, 0, 0))
        self.screen.blit(properties_text, (info_x, info_y))
        info_y += line_height

        # Define group colors
        group_colors = {
            "Brown": (139, 69, 19),
            "Light Blue": (173, 216, 230),
            "Pink": (255, 182, 193),
            "Orange": (255, 165, 0),
            "Red": (255, 0, 0),
            "Yellow": (255, 255, 0),
            "Green": (0, 128, 0),
            "Dark Blue": (0, 0, 139),
            "Utility": (192, 192, 192),
            "Station": (0, 0, 0),
            "Community Chest": (0, 0, 255),
            "Chance": (255, 165, 0),
            "Tax": (128, 128, 128),
            "Corner": (0, 0, 0),
        }

        for estate in current_player.estates:
            estate_color = (
                (128, 128, 128)
                if estate.mortgaged
                else group_colors.get(estate.group, (0, 0, 0))
            )
            estate_text = self.font.render(f"- {estate.name}", True, estate_color)
            self.screen.blit(estate_text, (info_x, info_y))
            info_y += line_height

        # Draw picked-up Community Chest cards
        cards_text = self.font.render("Cards:", True, (0, 0, 0))
        self.screen.blit(cards_text, (info_x, info_y))
        info_y += line_height

        for card in current_player.community_chest_cards:
            card_text = self.font.render(f"- {card.description}", True, (0, 0, 255))
            self.screen.blit(card_text, (info_x, info_y))
            info_y += line_height

    def roll_dice(self):
        """Rolls the dice for the current player and moves them accordingly.

        Runtime Complexity:
            - Worst-case O(1): Dice roll and player movement are based on a fixed range.
            - Average-case O(1): Same as worst-case.
        """
        if not self.dice_rolled:
            dice_roll = random.randint(1, 6) + random.randint(1, 6)
            dice_roll = 2
            print(f"Dice rolled: {dice_roll}")
            # Display the dice roll on the screen
            dice_text = self.font.render(f"Dice: {dice_roll}", True, (0, 0, 0))
            self.screen.blit(dice_text, (750, 200))
            pygame.display.flip()
            pygame.time.wait(1000)  # Wait for 1 second to show the dice roll
            self.move_player(self.players[self.current_player_index], dice_roll)
            self.dice_rolled = True
            self.buttons[0]["enabled"] = False  # Disable "Roll Dice" button
            self.buttons[5]["enabled"] = True  # Enable "End Turn" button
        else:
            print("You have already rolled the dice this turn.")

    def move_player(self, player, steps):
        """Moves the player's token a specified number of steps on the board.

        Runtime Complexity:
            - Worst-case O(S): Where S is the number of steps moved (maximum of 12).
            - Average-case O(S): Average dice roll results in a small constant S.
        """
        """
        Move the player a certain number of steps on the board.

        Args:
            player (Player): The player to move.
            steps (int): The number of steps to move the player.
        """
        if player.in_jail:
            self.handle_jail_turn(player)
            return
        print(f"Before move: {player.name} is on position {player.position}")
        old_position = player.position
        print(old_position)
        for _ in range(steps):
            player.position = (player.position + 1) % len(self.estates)
            self.update_board()
            pygame.time.wait(200)  # Wait for 200 milliseconds between each step

        if player.position < old_position:
            player.update_balance(200)
            print(f"{player.name} passed Go and collected $200")

        print(f"After move: {player.name} is on position {player.position}")
        self.handle_estate(player)

    def handle_estate(self, player):
        """Handles the logic when a player lands on an estate.

        Runtime Complexity:
            - Worst-case O(1): Involves conditional checks and method calls that are constant time.
            - Average-case O(1): Same as worst-case.
        """
        current_estate = self.estates[player.position]
        print(f"{player.name} is currently on {current_estate.name}")
        print(f"{player.name} has ${player.balance}")
        print(f"{player.name} currently owns:")
        for estate in player.estates:
            status = "(Mortgaged)" if estate.mortgaged else ""
            print(f"  - {estate.name} {status}")

        if current_estate.group == "Tax":
            player.update_balance(-current_estate.price)
            print(f"{player.name} paid ${current_estate.price} in taxes")
        elif current_estate.name == "Chance":
            self.draw_chance_card(player)
        elif current_estate.name == "Community Chest":
            self.draw_community_chest_card(player)
        elif current_estate.name == "Go to Jail":
            self.go_to_jail(player)
        elif current_estate.owner is not None and current_estate.owner != player:
            if not current_estate.pay_rent(player):
                self.offer_mortgage(player)
        else:
            if current_estate.buyable:
                self.buttons[1]["enabled"] = True  # Enable "Buy Property" button

    def offer_mortgage(self, player):
        """Offers the player an option to mortgage properties.

        Runtime Complexity:
            - Worst-case O(1): Initiates the mortgage popup.
            - Average-case O(1): Same as worst-case.
        """
        print(f"{player.name} is offered to mortgage a property")
        self.display_mortgage_popup(player)

    def handle_build_house(self):
        """Allows the current player to build a house on a property they own.

        Runtime Complexity:
            - Worst-case O(G): Where G is the number of properties in the group. Checks ownership of each property in the group.
            - Average-case O(G): Same as worst-case.
        """
        player = self.players[self.current_player_index]
        current_estate = self.estates[player.position]
        if current_estate.owner == player:
            if current_estate.build_house(self):
                if current_estate.hotel:
                    print(f"{player.name} built a hotel on {current_estate.name}")
                    player.update_balance(-current_estate.house_cost * 2)
                    self.display_message(
                        f"{player.name} built a hotel on {current_estate.name}"
                    )
                else:
                    print(f"{player.name} built a house on {current_estate.name}")
                    player.update_balance(-current_estate.house_cost)
                    self.display_message(
                        f"{player.name} built a house on {current_estate.name}"
                    )
            else:
                print(f"{player.name} cannot build a house on {current_estate.name}")
                self.display_message(
                    f"{player.name} cannot build a house on {current_estate.name}"
                )

    def display_message(self, message):
        """Displays a message on the screen for a brief duration.

        Runtime Complexity:
            - Worst-case O(L): Where L is the number of lines after text wrapping.
            - Average-case O(L): Same as worst-case.
        """
        message_rect = pygame.Rect(200, 250, 600, 100)  # Centered on the screen
        pygame.draw.rect(self.screen, (255, 255, 255), message_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), message_rect, 2)

        wrapped_lines = wrap_text(message, self.font, message_rect.width - 20)
        text_y = message_rect.y + 10

        for line in wrapped_lines:
            message_text = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(message_text, (message_rect.x + 10, text_y))
            text_y += self.font.get_linesize()

        pygame.display.flip()
        pygame.time.wait(2000)  # Display the message for 2 seconds
        self.update_board()

    def display_card(self, card):
        """Displays a card's information on the screen.

        Runtime Complexity:
            - Worst-case O(L): Where L is the number of lines after text wrapping.
            - Average-case O(L): Same as worst-case.
        """
        # Log the type and attributes of the card object

        card_rect = pygame.Rect(200, 220, 300, 300)  # Centered on the 700x700 board
        pygame.draw.rect(self.screen, (255, 255, 255), card_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), card_rect, 2)

        max_width = (
            card_rect.width - 20
        )  # Maximum width for card text with some padding
        wrapped_lines = wrap_text(card.description, self.font, max_width)
        text_y = card_rect.y + 10  # Start text a little below the top of the card

        for line in wrapped_lines:
            card_text = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(card_text, (card_rect.x + 10, text_y))
            text_y += self.font.get_linesize()

        pygame.display.flip()
        pygame.time.wait(2000)  # Display the card for 2 seconds
        print("Card displayed")

    def draw_chance_card(self, player):
        """Draws a Chance card for the player and applies its effects.

        Runtime Complexity:
            - Worst-case O(1): Drawing a card and applying effects are constant time operations.
            - Average-case O(1): Same as worst-case.
        """
        self.current_card = self.chance_deck.draw_card()
        self.display_card(self.current_card)
        self.apply_effect(
            player,
            self.current_card,
        )
        print(f"{player.name} drew a Chance card: {self.current_card.description}")
        self.current_card = None

    def draw_community_chest_card(self, player):
        """Draws a Community Chest card for the player and applies its effects.

        Runtime Complexity:
            - Worst-case O(1): Drawing a card and applying effects are constant time operations.
            - Average-case O(1): Same as worst-case.
        """
        self.current_card = self.community_chest_deck.draw_card()
        self.display_card(self.current_card)
        print(
            f"{player.name} drew a Community Chest card: {self.current_card.description}"
        )
        self.apply_effect(player, self.current_card)
        self.current_card = None

    def handle_click(self, pos):
        """Handles click events on the game interface.

        Runtime Complexity:
            - Worst-case O(B): Where B is the number of buttons and interactive elements.
            - Average-case O(B): Same as worst-case.
        """
        if hasattr(self, "current_card") and self.current_card:
            card_rect = pygame.Rect(350, 300, 300, 100)
            if card_rect.collidepoint(pos):
                self.current_card = None
                self.update_board()
                return

        if hasattr(self, "mortgage_popup_active") and self.mortgage_popup_active:
            popup_rect = pygame.Rect(100, 100, 600, 500)
            if not popup_rect.collidepoint(pos):
                self.mortgage_popup_active = False
                self.update_board()
                return

            button_height = 40
            button_width = 560
            button_margin = 10
            button_y = popup_rect.y + 80

            # Handle recommended properties to mortgage
            properties = self.calculate_mortgage_efficiency(self.mortgage_popup_player)
            for estate, score in properties:
                button_rect = pygame.Rect(
                    popup_rect.x + 20, button_y, button_width, button_height
                )
                if button_rect.collidepoint(pos):
                    self.mortgage_property(self.mortgage_popup_player, estate)
                    self.mortgage_popup_active = False
                    self.update_board()
                    return
                button_y += button_height + button_margin

            # Handle mortgaged properties
            mortgaged_properties = [estate for estate in self.mortgage_popup_player.estates if estate.mortgaged]
            if mortgaged_properties:
                button_y += button_margin  # Skip the "Mortgaged Properties" title
                button_y += button_height
                for estate in mortgaged_properties:
                    button_rect = pygame.Rect(
                        popup_rect.x + 20, button_y, button_width, button_height
                    )
                    if button_rect.collidepoint(pos):
                        self.unmortgage_property(self.mortgage_popup_player, estate)
                        self.mortgage_popup_active = False
                        self.update_board()
                        return
                    button_y += button_height + button_margin

        if hasattr(self, "trade_popup_active") and self.trade_popup_active:
            if self.trade_stage == "select_player":
                self.handle_select_player_click(pos)
            elif self.trade_stage == "select_property":
                self.handle_select_property_click(pos)
            elif self.trade_stage == "enter_offer":
                self.handle_enter_offer_click(pos)
            elif self.trade_stage == "confirm_trade":
                self.handle_confirm_trade_click(pos)

        for button in self.buttons:
            if button["rect"].collidepoint(pos) and button["enabled"]:
                button["action"]()

    def unmortgage_property(self, player, estate):
        """Unmortgages a property for a player and updates their balance accordingly.

        Runtime Complexity:
            - Worst-case O(1): Basic arithmetic and property state changes are constant time operations.
            - Average-case O(1): Same as worst-case.
        """
        if estate.unmortgage():
            player.update_balance(-estate.price)
            print(f"{player.name} unmortgaged {estate.name} for ${estate.price}")
        else:
            print(f"{player.name} could not unmortgage {estate.name}")

    def handle_buy(self):
        """Processes the buying action when the current player chooses to buy a property.

        Runtime Complexity:
            - Worst-case O(1): Calls another method with constant time operations.
            - Average-case O(1): Same as worst-case.
        """
        player = self.players[self.current_player_index]
        current_estate = self.estates[player.position]
        if current_estate.buyable and current_estate.owner is None:
            if self.buy_estate(player, current_estate):
                print(f"{player.name} bought {current_estate.name}")
            else:
                print(f"{player.name} could not buy {current_estate.name}")
        self.buttons[1]["enabled"] = False  # Disable "Buy Property" button
        self.update_buttons()
        self.update_board()

    def buy_estate(self, player, estate):
        """Facilitates the purchase of an estate by a player.

        Runtime Complexity:
            - Worst-case O(E): Where E is the number of estates the player owns. Checks for complete groups.
            - Average-case O(E): Same as worst-case.
        """
        if player.balance >= estate.price:
            player.update_balance(-estate.price)
            estate.owner = player
            player.insert_estate_sorted(estate, self)

            # Check if the player owns three complete groups
            groups_owned = set()
            for estate in player.estates:
                group_estates = [e for e in self.estates if e.group == estate.group]
                if all(e.owner == player for e in group_estates):
                    groups_owned.add(estate.group)

            if len(groups_owned) >= 3:
                self.buttons[2]["enabled"] = True  # Enable "Build House" button

            return True
        return False

    def handle_trade(self):
        """Initiates the trading process between players.

        Runtime Complexity:
            - Worst-case O(1): Sets up variables for the trade.
            - Average-case O(1): Same as worst-case.
        """
        """Initiate the trading process."""
        self.trade_popup_active = True
        self.trade_stage = "select_player"
        self.trade_with_player = None
        self.trade_property = None
        self.trade_offer = ""
        self.input_active = False
        self.update_board()

    def display_trade_menu(self):
        """Displays the trading menu based on the current trading stage.

        Runtime Complexity:
            - Worst-case O(P): Where P is the number of players or properties displayed.
            - Average-case O(P): Same as worst-case.
        """
        """Display the trading menu based on the current stage."""
        popup_rect = pygame.Rect(150, 100, 700, 500)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), popup_rect, 2)

        if self.trade_stage == "select_player":
            title_text = self.font.render(
                "Select a player to trade with:", True, (0, 0, 0)
            )
            self.screen.blit(title_text, (popup_rect.x + 20, popup_rect.y + 20))

            button_height = 50
            button_width = 200
            button_margin = 10
            button_y = popup_rect.y + 80

            current_player = self.players[self.current_player_index]
            for player in self.players:
                if player != current_player:
                    button_rect = pygame.Rect(
                        popup_rect.x + 250, button_y, button_width, button_height
                    )
                    pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
                    player_text = self.font.render(player.name, True, (0, 0, 0))
                    self.screen.blit(
                        player_text, (button_rect.x + 10, button_rect.y + 10)
                    )
                    button_y += button_height + button_margin

        elif self.trade_stage == "select_property":
            if not self.trade_with_player.estates:
                title_text = self.font.render(
                    f"Player {self.trade_with_player.name} has no properties to trade.",
                    True,
                    (0, 0, 0),
                )
                self.screen.blit(title_text, (popup_rect.x + 20, popup_rect.y + 20))
                pygame.display.flip()
                pygame.time.wait(2000)  # Display message for 2 seconds
                self.trade_popup_active = False  # Close the trade menu
                self.update_board()  # Refresh the board
                return

            title_text = self.font.render(
                f"Select a property from {self.trade_with_player.name}:",
                True,
                (0, 0, 0),
            )
            self.screen.blit(title_text, (popup_rect.x + 20, popup_rect.y + 20))

            button_height = 40
            button_width = 660
            button_margin = 10
            button_y = popup_rect.y + 80

            for estate in self.trade_with_player.estates:
                button_rect = pygame.Rect(
                    popup_rect.x + 20, button_y, button_width, button_height
                )
                pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
                estate_text = self.font.render(
                    f"{estate.name} (${estate.price})", True, (0, 0, 0)
                )
                self.screen.blit(estate_text, (button_rect.x + 10, button_rect.y + 5))
                button_y += button_height + button_margin

        elif self.trade_stage == "enter_offer":
            title_text = self.font.render(
                f"Enter your offer for {self.trade_property.name}:", True, (0, 0, 0)
            )
            self.screen.blit(title_text, (popup_rect.x + 20, popup_rect.y + 20))

            input_box = pygame.Rect(popup_rect.x + 250, popup_rect.y + 80, 200, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), input_box)
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)
            offer_text = self.font.render(self.trade_offer, True, (0, 0, 0))
            self.screen.blit(offer_text, (input_box.x + 10, input_box.y + 10))

            player = self.players[self.current_player_index]
            is_valid_offer = (
                self.trade_offer.isdigit()
                and int(self.trade_offer) <= player.balance
                and int(self.trade_offer) > 0
            )

            if not is_valid_offer and self.trade_offer:
                error_text_line1 = self.font.render(
                    "Offer exceeds your balance or is invalid.", True, (200, 0, 0)
                )
                error_text_line2 = self.font.render(
                    "Please enter a valid amount.", True, (200, 0, 0)
                )
                self.screen.blit(
                    error_text_line1, (popup_rect.x + 20, popup_rect.y + 220)
                )
                self.screen.blit(
                    error_text_line2, (popup_rect.x + 20, popup_rect.y + 250)
                )

            if is_valid_offer:
                submit_button = pygame.Rect(
                    popup_rect.x + 300, popup_rect.y + 150, 100, 40
                )
                pygame.draw.rect(self.screen, (0, 255, 0), submit_button)
                pygame.draw.rect(self.screen, (0, 0, 0), submit_button, 2)
                submit_text = self.font.render("Submit", True, (0, 0, 0))
                self.screen.blit(
                    submit_text, (submit_button.x + 10, submit_button.y + 5)
                )

        elif self.trade_stage == "confirm_trade":
            title_text = self.font.render(
                f"{self.trade_with_player.name}, do you accept the trade?",
                True,
                (0, 0, 0),
            )
            self.screen.blit(title_text, (popup_rect.x + 20, popup_rect.y + 20))

            details_text = self.font.render(
                f"{self.players[self.current_player_index].name} offers ${self.trade_offer} for {self.trade_property.name}",
                True,
                (0, 0, 0),
            )
            self.screen.blit(details_text, (popup_rect.x + 20, popup_rect.y + 80))

            accept_button = pygame.Rect(popup_rect.x + 200, popup_rect.y + 150, 100, 40)
            pygame.draw.rect(self.screen, (0, 255, 0), accept_button)
            pygame.draw.rect(self.screen, (0, 0, 0), accept_button, 2)
            accept_text = self.font.render("Accept", True, (0, 0, 0))
            self.screen.blit(accept_text, (accept_button.x + 10, accept_button.y + 5))

            decline_button = pygame.Rect(
                popup_rect.x + 400, popup_rect.y + 150, 100, 40
            )
            pygame.draw.rect(self.screen, (255, 0, 0), decline_button)
            pygame.draw.rect(self.screen, (0, 0, 0), decline_button, 2)
            decline_text = self.font.render("Decline", True, (0, 0, 0))
            self.screen.blit(
                decline_text, (decline_button.x + 10, decline_button.y + 5)
            )

        pygame.display.flip()

    def handle_select_player_click(self, pos):
        """Handles player selection during a trade.

        Runtime Complexity:
            - Worst-case O(N): Where N is the number of players.
            - Average-case O(N): Same as worst-case.
        """
        popup_rect = pygame.Rect(150, 100, 700, 500)
        button_height = 50
        button_width = 200
        button_margin = 10
        button_y = popup_rect.y + 80

        current_player = self.players[self.current_player_index]
        for player in self.players:
            if player != current_player:
                button_rect = pygame.Rect(
                    popup_rect.x + 250, button_y, button_width, button_height
                )
                if button_rect.collidepoint(pos):
                    self.trade_with_player = player
                    self.trade_stage = "select_property"
                    self.update_board()
                    return
                button_y += button_height + button_margin

    def handle_select_property_click(self, pos):
        """Handles property selection during a trade.

        Runtime Complexity:
            - Worst-case O(E): Where E is the number of properties the other player owns.
            - Average-case O(E): Same as worst-case.
        """
        popup_rect = pygame.Rect(150, 100, 700, 500)
        button_height = 40
        button_width = 660
        button_margin = 10
        button_y = popup_rect.y + 80

        for estate in self.trade_with_player.estates:
            button_rect = pygame.Rect(
                popup_rect.x + 20, button_y, button_width, button_height
            )
            if button_rect.collidepoint(pos):
                self.trade_property = estate
                self.trade_stage = "enter_offer"
                self.input_active = True
                self.trade_offer = ""  # Reset offer when selecting a new property
                self.update_board()
                return
            button_y += button_height + button_margin

    def handle_enter_offer_click(self, pos):
        """Processes the offer input during a trade.

        Runtime Complexity:
            - Worst-case O(1): Validates input and updates state.
            - Average-case O(1): Same as worst-case.
        """
        popup_rect = pygame.Rect(150, 100, 700, 500)
        input_box = pygame.Rect(popup_rect.x + 250, popup_rect.y + 80, 200, 50)
        submit_button = pygame.Rect(popup_rect.x + 300, popup_rect.y + 150, 100, 40)

        player = self.players[self.current_player_index]
        is_valid_offer = (
            self.trade_offer.isdigit()
            and int(self.trade_offer) <= player.balance
            and int(self.trade_offer) > 0
        )

        if input_box.collidepoint(pos):
            self.input_active = True
        elif is_valid_offer and submit_button.collidepoint(pos):
            self.trade_stage = "confirm_trade"
            self.input_active = False
            self.update_board()
        else:
            print("Invalid offer amount.")

    def handle_confirm_trade_click(self, pos):
        """Handles the confirmation or rejection of a trade offer.

        Runtime Complexity:
            - Worst-case O(1): Updates player properties and balances.
            - Average-case O(1): Same as worst-case.
        """
        popup_rect = pygame.Rect(150, 100, 700, 500)
        accept_button = pygame.Rect(popup_rect.x + 200, popup_rect.y + 150, 100, 40)
        decline_button = pygame.Rect(popup_rect.x + 400, popup_rect.y + 150, 100, 40)

        if accept_button.collidepoint(pos):
            offer_amount = int(self.trade_offer)
            buyer = self.players[self.current_player_index]
            seller = self.trade_with_player

            if buyer.balance >= offer_amount:
                buyer.update_balance(-offer_amount)
                seller.update_balance(offer_amount)
                seller.estates.remove(self.trade_property)
                buyer.estates.append(self.trade_property)
                self.trade_property.owner = buyer
                print(
                    f"{seller.name} sold {self.trade_property.name} to {buyer.name} for ${offer_amount}"
                )
            else:
                print(f"{buyer.name} does not have enough money.")
            self.trade_popup_active = False
            self.update_board()

        elif decline_button.collidepoint(pos):
            print(f"{self.trade_with_player.name} declined the trade.")
            self.trade_popup_active = False
            self.update_board()

    def handle_keydown(self, event):
        """Handles keydown events during inputs.

        Runtime Complexity:
            - Worst-case O(1): Processes a single key event.
            - Average-case O(1): Same as worst-case.
        """
        if (
            self.trade_popup_active
            and self.trade_stage == "enter_offer"
            and self.input_active
        ):
            if event.key == pygame.K_RETURN:
                if self.trade_offer.isdigit() and int(self.trade_offer) > 0:
                    self.trade_stage = "confirm_trade"
                    self.input_active = False
                    self.update_board()
                else:
                    print("Invalid offer amount.")
            elif event.key == pygame.K_BACKSPACE:
                self.trade_offer = self.trade_offer[:-1]
                self.update_board()
            else:
                if event.unicode.isdigit():
                    self.trade_offer += event.unicode
                    self.update_board()
        else:
            # ...handle other key events...
            pass

    def handle_mortgage(self):
        """Initiates the mortgage process for the current player.

        Runtime Complexity:
            - Worst-case O(1): Checks if player has properties and displays mortgage options.
            - Average-case O(1): Same as worst-case.
        """
        player = self.players[self.current_player_index]
        if not player.estates:
            print(f"{player.name} has no properties to mortgage.")
            return

        self.display_mortgage_popup(player)

    def calculate_mortgage_efficiency(self, player):
        """Calculates the efficiency score for mortgaging each property.

        Runtime Complexity:
            - Worst-case O(E): Where E is the number of properties the player owns.
            - Average-case O(E): Same as worst-case.
        """
        """Calculate mortgage efficiency score for each mortgagable property.

        Args:
            player (Player): The player who wants to mortgage properties.

        Returns:
            List[Tuple[Estate, float]]: A list of tuples containing the estate and its efficiency score.
        """
        properties = []
        for estate in player.estates:
            if not estate.mortgaged:
                future_income_lost = estate.get_current_rent(self)  # Pass game instance
                mortgage_value = estate.price // 2
                efficiency_score = mortgage_value / future_income_lost if future_income_lost != 0 else 0
                properties.append((estate, efficiency_score))
        properties.sort(key=lambda x: x[1], reverse=True)
        return properties

    def display_mortgage_popup(self, player):
        """Displays a popup with mortgage recommendations.

        Runtime Complexity:
            - Worst-case O(E): Where E is the number of properties to display.
            - Average-case O(E): Same as worst-case.
        """
        self.mortgage_popup_active = True
        self.mortgage_popup_player = player

        # Increased popup size for better display
        popup_rect = pygame.Rect(100, 100, 600, 500)  
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), popup_rect, 2)

        title_text = self.font.render("Mortgage Property Recommendations", True, (0, 0, 0))
        self.screen.blit(title_text, (popup_rect.x + 20, popup_rect.y + 20))

        properties = self.calculate_mortgage_efficiency(player)

        # Display recommended properties to mortgage
        button_height = 40
        button_width = 560
        button_margin = 10
        button_y = popup_rect.y + 80

        for estate, score in properties:
            button_rect = pygame.Rect(
                popup_rect.x + 20, button_y, button_width, button_height
            )
            pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
            estate_text = self.font.render(
                f"{estate.name} - Efficiency Score: {score:.2f}", True, (0, 0, 0)
            )
            self.screen.blit(estate_text, (button_rect.x + 10, button_rect.y + 10))
            button_y += button_height + button_margin

        # Display mortgaged properties separately
        mortgaged_properties = [estate for estate in player.estates if estate.mortgaged]

        if mortgaged_properties:
            button_y += button_margin  # Add space before mortgaged properties
            mortgaged_text = self.font.render("Mortgaged Properties", True, (0, 0, 0))
            self.screen.blit(mortgaged_text, (popup_rect.x + 20, button_y))
            button_y += button_height

            for estate in mortgaged_properties:
                button_rect = pygame.Rect(
                    popup_rect.x + 20, button_y, button_width, button_height
                )
                pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
                estate_text = self.font.render(estate.name, True, (0, 0, 0))
                self.screen.blit(estate_text, (button_rect.x + 10, button_rect.y + 10))
                button_y += button_height + button_margin

        pygame.display.flip()

    def end_turn(self):
        """Ends the current player's turn and advances to the next player.

        Runtime Complexity:
            - Worst-case O(1): Updates indices and states.
            - Average-case O(1): Same as worst-case.
        """
        print(f"Turn ended for {self.players[self.current_player_index].name}")
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.dice_rolled = False
        self.update_buttons()
        self.update_board()

    def update_buttons(self):
        """Updates the state (enabled/disabled) of action buttons based on game conditions.

        Runtime Complexity:
            - Worst-case O(G): Where G is the number of properties in a group (for ownership checks).
            - Average-case O(G): Same as worst-case.
        """
        player = self.players[self.current_player_index]
        current_estate = self.estates[player.position]
        self.buttons[0][
            "enabled"
        ] = not self.dice_rolled  # Enable "Roll Dice" button if dice not rolled
        self.buttons[1]["enabled"] = (
            current_estate.buyable and current_estate.owner is None
        )  # Enable "Buy Property" button if property is buyable and not owned
        self.buttons[2]["enabled"] = (
            current_estate.owner == player
            and not current_estate.hotel
            and all(
                estate.owner == player
                for estate in self.estates
                if estate.group == current_estate.group
            )
        )  # Enable "Build House" button if player owns the property, it doesn't have a hotel, and player owns all properties in the group
        self.buttons[3]["enabled"] = bool(
            player.estates
        )  # Enable "Mortgage" button only if player has properties
        self.buttons[4]["enabled"] = any(
            p.estates for p in self.players if p != player
        )  # Enable "Trade" button only if another player owns a property
        self.buttons[5][
            "enabled"
        ] = self.dice_rolled  # Enable "End Turn" button only if dice rolled

    def draw_buttons(self):
        """Renders interactive buttons on the game interface.

        Runtime Complexity:
            - Worst-case O(B): Where B is the number of buttons.
            - Average-case O(B): Same as worst-case.
        """
        for button in self.buttons:
            color = (0, 0, 0) if button["enabled"] else (128, 128, 128)
            pygame.draw.rect(self.screen, color, button["rect"])
            text = self.font.render(button["label"], True, (255, 255, 255))

            # Scale text to fit within the button if necessary
            text_rect = text.get_rect()
            if text_rect.width > button["rect"].width - 20:  # Add some padding
                scale_factor = (button["rect"].width - 20) / text_rect.width
                text = pygame.transform.scale(
                    text,
                    (
                        int(text_rect.width * scale_factor),
                        int(text_rect.height * scale_factor),
                    ),
                )
                text_rect = text.get_rect()

            text_rect.center = button["rect"].center
            self.screen.blit(text, text_rect)

    def draw_tokens(self):
        """Draws player tokens and property indicators on the game board.

        Runtime Complexity:
            - Worst-case O(P + E): Where P is the number of players and E is the number of estates with houses/hotels.
            - Average-case O(P + E): Same as worst-case.
        """
        color_offsets = {
            "red": (0, 0),
            "blue": (10, 0),
            "green": (0, 10),
            "yellow": (10, 10),
        }

        for player in self.players:
            token_color = pygame.Color(player.color)
            token_position = self.estates[player.position].position
            offset = color_offsets.get(player.color, (0, 0))
            adjusted_position = (
                token_position[0] + offset[0],
                token_position[1] + offset[1],
            )
            pygame.draw.circle(
                self.screen, token_color, adjusted_position, 20
            )  # Increased radius to 20

        for estate in self.estates:
            estate_position = estate.position
            house_size = 10
            house_margin = 5

            if estate.hotel:
                # Draw a red square for the hotel
                hotel_rect = pygame.Rect(
                    estate_position[0] - house_size // 2,
                    estate_position[1] - house_size // 2,
                    house_size,
                    house_size,
                )
                pygame.draw.rect(self.screen, (255, 0, 0), hotel_rect)
            else:
                # Draw green squares for each house in a 2x2 grid
                for i in range(estate.houses):
                    row = i // 2
                    col = i % 2
                    house_rect = pygame.Rect(
                        estate_position[0] - house_size // 2 + (col * (house_size + house_margin)),
                        estate_position[1] - house_size // 2 + (row * (house_size + house_margin)),
                        house_size,
                        house_size,
                    )
                    pygame.draw.rect(self.screen, (0, 255, 0), house_rect)

    def update_board(self):
        """Updates the game board visuals, including tokens and player info.

        Runtime Complexity:
            - Worst-case O(P + B + E): Combines complexities of drawing tokens, buttons, and other elements.
            - Average-case O(P + B + E): Same as worst-case.
        """
        self.screen.blit(self.background, (0, 0))
        self.draw_buttons()
        self.draw_tokens()
        self.draw_player_info()
        if self.trade_popup_active:
            self.display_trade_menu()
        elif hasattr(self, "current_card") and self.current_card:
            self.display_card(self.current_card)
        elif hasattr(self, "mortgage_popup_active") and self.mortgage_popup_active:
            self.display_mortgage_popup(self.mortgage_popup_player)
        pygame.display.flip()

    def draw_setup_screen(self):
        """Displays the setup screen for initializing the game.

        Runtime Complexity:
            - Worst-case O(1): Renders static text and input field.
            - Average-case O(1): Same as worst-case.
        """
        self.screen.fill((255, 255, 255))
        if self.current_setup_step == 0:
            prompt = "Enter the number of players:"
        else:
            prompt = f"Enter the name for player {self.current_setup_step}:"
        text_surface = self.font.render(prompt, True, (0, 0, 0))
        self.screen.blit(text_surface, (250, 250))
        input_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(input_surface, (self.input_box.x + 10, self.input_box.y + 10))
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)
        pygame.display.flip()

    def handle_setup_event(self, event):
        """Handles events during the game setup phase.

        Runtime Complexity:
            - Worst-case O(1): Processes a single event.
            - Average-case O(1): Same as worst-case.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.current_setup_step == 0:
                    self.num_players = int(self.input_text)
                    self.current_setup_step += 1
                else:
                    player_name = self.input_text
                    player_color = self.token_colors[
                        self.current_color_index % len(self.token_colors)
                    ]
                    self.players.append(Player(player_name, player_color))
                    self.current_color_index += 1
                    self.current_setup_step += 1
                    if self.current_setup_step > self.num_players:
                        self.setup_phase = False
                self.input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def start_game(self):
        """Starts the game loop, handling setups and main gameplay.

        Runtime Complexity:
            - Worst-case O(T): Where T is the number of game ticks/events processed.
            - Average-case O(T): Depends on user interaction and game duration.
        """
        while self.running:
            if self.setup_phase:
                self.draw_setup_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        self.handle_setup_event(event)
            else:
                self.update_board()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_click(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        self.handle_keydown(event)

        pygame.quit()

    def apply_effect(self, player, card):
        """Applies the effect of a drawn card to the player.

        Runtime Complexity:
            - Worst-case O(E): May involve moving the player or modifying properties.
            - Average-case O(1): Most effects are simple state changes.
        """
        print(f"Applying effect of card: {card.description}")
        if card.is_get_out_of_jail:
            player.community_chest_cards.append(card)
            print(f"{player.name} got a Get Out of Jail Free card")
        if card.move_to:
            match card.move_to:
                case "nearest Utility":
                    self.move_to_nearest_utility(player)
                case "nearest Railroad":
                    self.move_to_nearest_railroad(player)
                case "Jail":
                    self.go_to_jail(player)
                case "Go":
                    self.move_player_to(player, 0)
                case "Bond Street":
                    self.move_player_to(player, 11)
                case "Illinois Avenue":
                    self.move_player_to(player, 24)
                case "Vine Street":
                    self.move_player_to(player, 39)
                case "Kings Cross Station":
                    self.move_player_to(player, 5)
                case _:
                    self.move_player_to(player, card.move_to)
        if card.value:
            player.update_balance(card.value * card.multiplier)
            print(f"{player.name} received ${card.value}")


if __name__ == "__main__":
    game = Game()
    game.start_game()
