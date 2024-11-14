"""
Main file for the Monopoly game.
"""

import pygame
import random
from src.player_management import Player
from src.estate_management import initialize_estates
from src.card_management import (
    create_chance_deck,
    create_community_chest_deck,
)
from src.utils import wrap_text


class Game:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.screen = pygame.display.set_mode((1000, 700))  # Extended width to 1000
        pygame.display.set_caption("Monopoly")
        self.background = pygame.image.load("src/img/upd_monopoly_board.png")
        self.font = pygame.font.Font(None, 36)
        self.players = []
        self.estates = initialize_estates()
        self.current_player_index = 0
        self.dice_rolled = False
        self.chance_deck = create_chance_deck()
        self.community_chest_deck = create_community_chest_deck()
        self.buttons = [
            {
                "label": "Roll Dice",
                "action": self.roll_dice,
                "rect": pygame.Rect(730, 50, 120, 50),
                "enabled": True,
            },
            {
                "label": "Buy Property",
                "action": self.handle_buy,
                "rect": pygame.Rect(860, 50, 120, 50),
                "enabled": False,
            },
            {
                "label": "Build House",
                "action": self.handle_build_house,
                "rect": pygame.Rect(730, 110, 120, 50),
                "enabled": False,
            },
            {
                "label": "Mortgage",
                "action": self.handle_mortgage,
                "rect": pygame.Rect(860, 110, 120, 50),
                "enabled": False,
            },
            # {
            #     "label": "Trade",
            #     "action": self.handle_trade,
            #     "rect": pygame.Rect(730, 170, 120, 50),
            #     "enabled": True,
            # },
            {
                "label": "End Turn",
                "action": self.end_turn,
                "rect": pygame.Rect(860, 170, 120, 50),
                "enabled": True,
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

    def mortgage_property(self, player, estate):
        if estate.mortgage():
            player.update_balance(estate.price // 2)
            print(f"{player.name} mortgaged {estate.name} for ${estate.price // 2}")
        else:
            print(f"{player.name} could not mortgage {estate.name}")

    def move_to_nearest_utility(self, player):
        utilities = ["Electric Company", "Water Works"]
        current_position = player.position
        nearest_utility = min(
            utilities,
            key=lambda utility: (self.get_estate_position_by_name(utility) - current_position) % len(self.estates)
        )
        self.move_player_to(player, nearest_utility)

    def move_to_nearest_railroad(self, player):
        railroads = ["Kings Cross Station", "Marylebone Station", "Fenchurch St. Station", "Liverpool St. Station"]
        current_position = player.position
        nearest_railroad = min(
            railroads,
            key=lambda railroad: (self.get_estate_position_by_name(railroad) - current_position) % len(self.estates)
        )
        self.move_player_to(player, nearest_railroad)

    def get_estate_position_by_name(self, name):
        for i, estate in enumerate(self.estates):
            if estate.name == name:
                return i
        raise ValueError(f"Estate with name '{name}' not found")

    def move_player_to(self, player, location_name):
        """Move player to a specific location.

        Args:
            player (Player): The player to move.
            location_name (str): The name of the location to move to.
        """
        try:
            target_position = next(
                i for i, estate in enumerate(self.estates) if estate.name == location_name
            )
            old_position = player.position
            player.position = target_position
            if player.position < old_position:
                player.update_balance(200)
                print(f"{player.name} passed Go and collected $200")
            self.handle_estate(player)
        except StopIteration:
            print(f"Estate with name '{location_name}' not found")

    def draw_player_info(self):
        current_player = self.players[self.current_player_index]
        info_x = 720
        info_y = 230  # Start below the buttons
        line_height = 30

        # Clear the area where player info is displayed
        pygame.draw.rect(self.screen, (255, 255, 255), (info_x, 10, 200, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), (info_x, info_y, 350, 600))

        # Draw current player name
        name_text = self.font.render(f"Player: {current_player.name}", True, (0, 0, 0))
        self.screen.blit(name_text, (info_x, 10))  # Display at the top right
        info_y += line_height

        # Draw current player cash
        cash_text = self.font.render(f"Cash: ${current_player.balance}", True, (0, 0, 0))
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
            "Corner": (0, 0, 0)
        }

        for estate in current_player.estates:
            if estate.mortgaged:
                estate_color = (128, 128, 128)  # Grey color for mortgaged estates
            else:
                estate_color = group_colors.get(estate.group, (0, 0, 0))  # Default to black if group not found
            estate_text = self.font.render(f"- {estate.name}", True, estate_color)
            self.screen.blit(estate_text, (info_x, info_y))
            info_y += line_height

        # Draw picked-up Community Chest cards
        cards_text = self.font.render("Cards:", True, (0, 0, 0))
        self.screen.blit(cards_text, (info_x, info_y))
        info_y += line_height

        for card in current_player.community_chest_cards:
            card_text = self.font.render(f"- {card.description}", True, (0, 0, 0))
            self.screen.blit(card_text, (info_x, info_y))
            info_y += line_height

    def roll_dice(self):
        """
        Roll the dice and move the current player.
        """
        if not self.dice_rolled:
            dice_roll = random.randint(1, 6) + random.randint(1, 6)
            print(f"Dice rolled: {dice_roll}")
            self.move_player(self.players[self.current_player_index], dice_roll)
            self.dice_rolled = True
            self.buttons[0]["enabled"] = False  # Disable "Roll Dice" button
        else:
            print("You have already rolled the dice this turn.")

    def move_player(self, player, steps):
        """
        Move the player a certain number of steps on the board.

        Args:
            player (Player): The player to move.
            steps (int): The number of steps to move the player.
        """
        if player.in_jail:
            player.jail_turns += 1
            if player.jail_turns >= 3:
                player.get_out_of_jail()
            else:
                print(f"{player.name} is in jail and cannot move.")
                return
        print(f"Before move: {player.name} is on position {player.position}")
        old_position = player.position
        player.position = (player.position + steps) % len(self.estates)
        if player.position < old_position:
            player.update_balance(200)
            print(f"{player.name} passed Go and collected $200")
        print(f"After move: {player.name} is on position {player.position}")
        self.handle_estate(player)

    def handle_estate(self, player):
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
        elif current_estate.owner is not None and current_estate.owner != player:
            if not current_estate.pay_rent(player):
                self.offer_mortgage(player)
        else:
            if current_estate.buyable:
                self.buttons[1]["enabled"] = True  # Enable "Buy Property" button

    def offer_mortgage(self, player):
        print(f"{player.name} is offered to mortgage a property")
        self.display_mortgage_popup(player)

    def handle_build_house(self):
        player = self.players[self.current_player_index]
        current_estate = self.estates[player.position]
        if current_estate.owner == player:
            if current_estate.build_house():
                print(f"{player.name} built a house on {current_estate.name}")
            else:
                print(f"{player.name} cannot build a house on {current_estate.name}")
        self.buttons[2]["enabled"] = False  # Disable "Build House" button

    def display_card(self, card):
        self.current_card = card
        card_rect = pygame.Rect(200, 250, 300, 200)  # Centered on the 700x700 board
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

    def draw_chance_card(self, player):
        card = self.chance_deck.draw_card()
        print(type(card))
        self.display_card(card)
        card.apply_effect(player, self)
        print(f"{player.name} drew a Chance card: {card.description}")

    def draw_community_chest_card(self, player):
        card = self.community_chest_deck.draw_card()
        self.display_card(card)
        card.apply_effect(player, self)
        print(f"{player.name} drew a Community Chest card: {card.description}")

    def handle_click(self, pos):
        if hasattr(self, "current_card") and self.current_card:
            card_rect = pygame.Rect(350, 300, 300, 100)
            if card_rect.collidepoint(pos):
                self.current_card = None
                self.update_board()
                return

        if hasattr(self, "mortgage_popup_active") and self.mortgage_popup_active:
            popup_rect = pygame.Rect(200, 150, 300, 400)
            button_height = 40
            button_width = 260
            button_margin = 10
            button_y = popup_rect.y + 60

            # Handle not mortgaged properties
            button_y += button_height  # Skip the "Not Mortgaged" title
            for estate in self.mortgage_popup_player.estates:
                if not estate.mortgaged:
                    button_rect = pygame.Rect(popup_rect.x + 20, button_y, button_width, button_height)
                    if button_rect.collidepoint(pos):
                        self.mortgage_property(self.mortgage_popup_player, estate)
                        self.mortgage_popup_active = False
                        self.update_board()
                        return
                    button_y += button_height + button_margin

            # Handle mortgaged properties
            button_y += button_margin  # Add some space between the two categories
            button_y += button_height  # Skip the "Mortgaged" title
            for estate in self.mortgage_popup_player.estates:
                if estate.mortgaged:
                    button_rect = pygame.Rect(popup_rect.x + 20, button_y, button_width, button_height)
                    if button_rect.collidepoint(pos):
                        self.unmortgage_property(self.mortgage_popup_player, estate)
                        self.mortgage_popup_active = False
                        self.update_board()
                        return
                    button_y += button_height + button_margin

        for button in self.buttons:
            if button["rect"].collidepoint(pos) and button["enabled"]:
                button["action"]()

    def unmortgage_property(self, player, estate):
        if estate.unmortgage():
            player.update_balance(-estate.price)
            print(f"{player.name} unmortgaged {estate.name} for ${estate.price}")
        else:
            print(f"{player.name} could not unmortgage {estate.name}")

    def handle_buy(self):
        player = self.players[self.current_player_index]
        current_estate = self.estates[player.position]
        if current_estate.buyable:
            if current_estate.buy_estate(player):
                print(f"{player.name} bought {current_estate.name}")
            else:
                print(f"{player.name} could not buy {current_estate.name}")
        self.buttons[1]["enabled"] = False  # Disable "Buy Property" button
        self.update_buttons()
        self.update_board()

    def handle_trade(self, player):
        trade_partner = self.players[(self.current_player_index + 1) % len(self.players)]
        current_estate = self.estates[player.position]

        if current_estate.owner == player:
            # Create a Pygame input window for trade amount
            trade_amount = self.get_trade_amount(f"Enter the amount of money to trade {current_estate.name} with {trade_partner.name}: ")
            if trade_amount is not None and trade_partner.balance >= trade_amount:
                if trade_amount is not None:
                    trade_partner.update_balance(-trade_amount)
                    player.update_balance(trade_amount)
                    current_estate.owner = trade_partner
                    player.estates.remove(current_estate)
                    trade_partner.estates.append(current_estate)
                    print(f"{player.name} traded {current_estate.name} with {trade_partner.name} for ${trade_amount}")
                else:
                    print("Invalid trade amount entered.")
            else:
                print(f"{trade_partner.name} does not have enough money to trade.")
        else:
            print(f"{player.name} does not own {current_estate.name}")
        self.buttons[4]["enabled"] = False  # Disable "Trade" button

    def get_trade_amount(self, prompt):
        """
        Display a Pygame input window to get the trade amount.
        """
        input_box = pygame.Rect(250, 300, 200, 50)
        input_text = ""
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            self.screen.fill((255, 255, 255))
            prompt_surface = self.font.render(prompt, True, (0, 0, 0))
            self.screen.blit(prompt_surface, (250, 250))
            input_surface = self.font.render(input_text, True, (0, 0, 0))
            self.screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)
            pygame.display.flip()

        try:
            return int(input_text)
        except ValueError:
            return None

    def handle_mortgage(self):
        player = self.players[self.current_player_index]
        if not player.estates:
            print(f"{player.name} has no properties to mortgage.")
            return

        self.display_mortgage_popup(player)

    def display_mortgage_popup(self, player):
        self.mortgage_popup_active = True
        self.mortgage_popup_player = player

        popup_rect = pygame.Rect(200, 150, 300, 400)  # Centered on the 700x700 board
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), popup_rect, 2)

        title_text = self.font.render("Mortgage Property", True, (0, 0, 0))
        self.screen.blit(title_text, (popup_rect.x + 20, popup_rect.y + 20))

        button_height = 40
        button_width = 260
        button_margin = 10
        button_y = popup_rect.y + 60

        # Display not mortgaged properties
        not_mortgaged_text = self.font.render("Not Mortgaged", True, (0, 0, 0))
        self.screen.blit(not_mortgaged_text, (popup_rect.x + 20, button_y))
        button_y += button_height

        for estate in player.estates:
            if not estate.mortgaged:
                button_rect = pygame.Rect(popup_rect.x + 20, button_y, button_width, button_height)
                pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
                estate_text = self.font.render(estate.name, True, (0, 0, 0))
                self.screen.blit(estate_text, (button_rect.x + 10, button_rect.y + 10))
                button_y += button_height + button_margin

        # Display mortgaged properties
        button_y += button_margin  # Add some space between the two categories
        mortgaged_text = self.font.render("Mortgaged", True, (0, 0, 0))
        self.screen.blit(mortgaged_text, (popup_rect.x + 20, button_y))
        button_y += button_height

        for estate in player.estates:
            if estate.mortgaged:
                button_rect = pygame.Rect(popup_rect.x + 20, button_y, button_width, button_height)
                pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
                estate_text = self.font.render(estate.name, True, (0, 0, 0))
                self.screen.blit(estate_text, (button_rect.x + 10, button_rect.y + 10))
                button_y += button_height + button_margin

        pygame.display.flip()

    def handle_turn(self):
        player = self.players[self.current_player_index]
        if player.in_jail:
            player.handle_jail_turn()
            if not player.in_jail:
                self.roll_dice()
        else:
            self.roll_dice()

    def end_turn(self):
        print(f"Turn ended for {self.players[self.current_player_index].name}")
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.dice_rolled = False
        self.buttons[0]["enabled"] = True  # Enable "Roll Dice" button
        self.buttons[1]["enabled"] = False  # Disable "Buy Property" button
        self.buttons[2]["enabled"] = False  # Disable "Build House" button
        self.update_buttons()
        self.update_board()

    def update_buttons(self):
        player = self.players[self.current_player_index]
        self.buttons[3]["enabled"] = bool(player.estates)  # Enable "Mortgage" button only if player has properties

    def draw_buttons(self):
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

    def update_board(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_buttons()
        self.draw_tokens()
        self.draw_player_info()  # Draw player info below the buttons
        if hasattr(self, 'current_card') and self.current_card:
            self.display_card(self.current_card)
        if hasattr(self, 'mortgage_popup_active') and self.mortgage_popup_active:
            self.display_mortgage_popup(self.mortgage_popup_player)
        pygame.display.flip()

    def draw_setup_screen(self):
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

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.start_game()
