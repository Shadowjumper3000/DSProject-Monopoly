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
    apply_effect,
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
                "enabled": True,
            },
            {
                "label": "Trade",
                "action": self.handle_trade,
                "rect": pygame.Rect(730, 170, 120, 50),
                "enabled": True,
            },
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

    def move_to_nearest_utility(self, player):
        """Move player to the nearest utility.
        # !!! This method is not used in the current implementation.

        Args:
            player (Player): The player to move.
        """
        utilities = ["Electric Company", "Water Works"]
        current_position = player.position
        nearest_utility = min(
            utilities,
            key=lambda utility: (self.estates.index(utility) - current_position)
            % len(self.estates),
        )
        self.move_player_to(player, nearest_utility)

    def move_to_nearest_railroad(self, player):
        """Move player to the nearest railroad.
        # !!! This method is not used in the current implementation.

        Args:
            player (Player): The player to move.
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
            key=lambda railroad: (self.estates.index(railroad) - current_position)
            % len(self.estates),
        )
        self.move_player_to(player, nearest_railroad)

    def move_player_to(self, player, location_name):
        """Move player to a specific location.
        # TODO Update to pass the location object instead of the name.

        Args:
            player (Player): The player to move.
            location_name (str): The name of the location to move to.
        """
        target_position = next(
            i for i, estate in enumerate(self.estates) if estate.name == location_name
        )
        steps = (target_position - player.position) % len(self.estates)
        self.move_player(player, steps)

    def draw_player_info(self):
        """
        Draw player information on the right side of the screen.
        """
        current_player = self.players[self.current_player_index]
        info_x = 705
        info_y = 230  # Start below the buttons
        line_height = 30

        # Clear the area where player info is displayed
        pygame.draw.rect(self.screen, (255, 255, 255), (info_x, 10, 200, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), (info_x, info_y, 400, 600))

        # Draw current player name
        name_text = self.font.render(f"Player: {current_player.name}", True, (0, 0, 0))
        self.screen.blit(name_text, (info_x, 10))  # Display at the top right
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

        for estate in current_player.properties:
            estate_color = group_colors.get(
                estate.group, (0, 0, 0)
            )  # Default to black if group not found
            estate_text = self.font.render(f"- {estate.name}", True, estate_color)
            self.screen.blit(estate_text, (info_x, info_y))
            info_y += line_height

        # Draw picked-up Community Chest cards
        cards_text = self.font.render("Cards:", True, (0, 0, 0))
        self.screen.blit(cards_text, (info_x, info_y))
        info_y += line_height

        max_width = 250  # Maximum width for card text

        for card in current_player.community_chest_cards:
            wrapped_lines = wrap_text(card.description, self.font, max_width)
            for line in wrapped_lines:
                card_text = self.font.render(line, True, (0, 0, 0))
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
        print(f"Before move: {player.name} is on position {player.position}")
        old_position = player.position
        player.position = (player.position + steps) % len(self.estates)
        if player.position < old_position:
            player.update_balance(200)
            print(f"{player.name} passed Go and collected $200")
        print(f"After move: {player.name} is on position {player.position}")
        self.handle_estate(player)

    def handle_estate(self, player):
        """
        Handle the current estate the player is on.
        Called after player moves to a new estate.

        Args:
            player (Player): The player whose turn it is.
        """
        current_estate = self.estates[player.position]
        print(f"{player.name} is currently on {current_estate.name}")
        print(f"{player.name} has ${player.balance}")
        print(f"{player.name} currently owns:")
        for estate in player.properties:
            status = "(Mortgaged)" if estate.mortgaged else ""
            print(f"  - {estate.name} {status}")

        if current_estate.name == "Chance":
            self.draw_chance_card(player)
        elif current_estate.name == "Community Chest":
            self.draw_community_chest_card(player)
        elif current_estate.name == "Go To Jail":
            player.go_to_jail()
            print(f"{player.name} is going to jail")
        elif current_estate.name == "Tax":
            player.update_balance(-current_estate.rent)
            print(f"{player.name} paid ${current_estate.rent} in taxes")
        else:
            if current_estate.owner is None:
                self.buttons[1]["enabled"] = True  # Enable "Buy Property" button
            elif current_estate.owner == player:
                self.buttons[2]["enabled"] = True  # Enable "Build House" button

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
        apply_effect(player, self, card)
        print(f"{player.name} drew a Chance card: {card.description}")

    def draw_community_chest_card(self, player):
        card = self.community_chest_deck.draw_card()
        self.display_card(card)
        apply_effect(player, self, card)
        print(f"{player.name} drew a Community Chest card: {card.description}")

    def handle_click(self, pos):
        if hasattr(self, "current_card") and self.current_card:
            card_rect = pygame.Rect(350, 300, 300, 100)
            if card_rect.collidepoint(pos):
                self.current_card = None
                self.update_board()
                return

        for button in self.buttons:
            if button["rect"].collidepoint(pos) and button["enabled"]:
                button["action"]()

    def handle_buy(self):
        player = self.players[self.current_player_index]
        current_estate = self.estates[player.position]
        if current_estate.owner is None:
            if current_estate.buy_estate(player):
                print(f"{player.name} bought {current_estate.name}")
            else:
                print(f"{player.name} could not buy {current_estate.name}")
        self.buttons[1]["enabled"] = False  # Disable "Buy Property" button
        self.update_board()

    def handle_trade(self, player):
        pass

    def handle_mortgage(self, player):
        pass

    def end_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.dice_rolled = False
        self.buttons[0]["enabled"] = True  # Enable "Roll Dice" button
        self.buttons[1]["enabled"] = False  # Disable "Buy Property" button
        self.buttons[2]["enabled"] = False  # Disable "Build House" button
        self.update_board()

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
        if hasattr(self, "current_card") and self.current_card:
            self.display_card(self.current_card)
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
