import sys
import os
import unittest

# Add the directory containing player_management.py to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

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

        print(f"Testing initialize_player with player_num={player_num} and player_name={player_name}")
        print(f"Player ID: {player.player_id}, Name: {player.name}, Money: {player.money}")

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

        print(f"Testing initialize_players with player_names={player_names}")
        print(f"Number of players initialized: {len(players)}")

        self.assertEqual(len(players), 3)
        for i, player in enumerate(players, start=1):
            print(f"Player {i}: ID={player.player_id}, Name={player.name}, Money={player.money}")
            self.assertIsInstance(player, player_management.Player)
            self.assertEqual(player.player_id, i)
            self.assertEqual(player.name, player_names[i - 1])
            self.assertEqual(player.money, 1500)
            self.assertEqual(player.position, 0)
            self.assertEqual(player.estates, [])
            self.assertFalse(player.in_jail)
            self.assertEqual(player.jail_free_cards, 0)

    def test_initialize_players_invalid_number(self):
        player_names = ["Alice"]
        print(f"Testing initialize_players with invalid number of player_names={player_names}")
        with self.assertRaises(ValueError):
            player_management.initialize_players(player_names)

        player_names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank"]
        print(f"Testing initialize_players with invalid number of player_names={player_names}")
        with self.assertRaises(ValueError):
            player_management.initialize_players(player_names)

if __name__ == '__main__':
    unittest.main()