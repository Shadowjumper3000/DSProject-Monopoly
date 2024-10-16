"""
This is the main test file for the project.

It contains all the test cases for the project.
"""

import unittest
import player_management


class TestPlayerManagement(unittest.TestCase):
    """
    TestPlayerManagement is a test case class for testing the player management functionalities 
    in a Monopoly game. It includes tests for initializing individual players and multiple players, 
    as well as handling invalid numbers of players.
    Methods:
        test_initialize_player():
            Tests the initialization of a single player with default attributes.
        test_initialize_players():
            Tests the initialization of multiple players and verifies their attributes.
        test_initialize_players_invalid_number():
            Tests the initialization of players with an invalid number of player names 
            and expects a ValueError to be raised.
    """

    def test_initialize_player(self):
        player_num = 1
        player_name = "Alice"
        player = player_management.initialize_player(player_num, player_name)

        self.assertIsInstance(player, player_management.Player)
        self.assertEqual(player.player_id, player_num)
        self.assertEqual(player.name, player_name)
        self.assertEqual(player.money, 1500)
        self.assertEqual(player.position, 0)
        self.assertEqual(player.estates, [])
        self.assertFalse(player.in_jail)
        self.assertEqual(player.jail_free_cards, 0)

    def test_initialize_players(self):
        player_names = ["Alice", "Bob", "Charlie"]
        players = player_management.initialize_players(player_names)

        self.assertEqual(len(players), 3)
        for i, player in enumerate(players, start=1):
            self.assertIsInstance(player, player_management.Player)
            self.assertEqual(player.player_id, i)
            self.assertEqual(player.name, player_names[i - 1])
            self.assertEqual(player.money, 1500)
            self.assertEqual(player.position, 0)
            self.assertEqual(player.properties, [])
            self.assertFalse(player.in_jail)
            self.assertEqual(player.jail_free_cards, 0)

    def test_initialize_players_invalid_number(self):
        player_names = ["Alice"]
        with self.assertRaises(ValueError):
            player_management.initialize_players(player_names)

        player_names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank"]
        with self.assertRaises(ValueError):
            player_management.initialize_players(player_names)


if __name__ == '__main__':
    unittest.main()
