"""
This function performs a basic test.

Returns:
    bool: True if the test passes, False otherwise.
"""

import unittest
from player_management import Player


class TestPlayer(unittest.TestCase):
    """
    Test the Player class.
    """

    def setUp(self):
        """
        Create two players for testing.
        """
        self.player1 = Player(player_id=1, name="Player 1")
        self.player2 = Player(player_id=2, name="Player 2")

    def test_initial_money(self):
        """
        Test that the players start with the correct amount of money.
        """
        self.assertEqual(self.player1.money, 1500)
        self.assertEqual(self.player2.money, 1500)

    def test_buy_estate(self):
        """
        Test that a player can buy an estate.
        """
        class MockEstate:
            """
            A mock estate class for testing.
            """
            def __init__(self, name, cost, street_group):
                self.name = name
                self.cost = cost
                self.street_group = street_group
                self.owner = None

            def change_owner(self, owner_name):
                """
                Change the owner of the estate.
                """
                self.owner = owner_name

        estate = MockEstate(name="Boardwalk", cost=400, street_group=1)
        self.player1.buy_estate(estate)
        self.assertEqual(self.player1.money, 1100)
        self.assertIn(estate, self.player1.estates)
        self.assertEqual(estate.owner, "Player 1")

    def test_pay_rent(self):
        """
        Test that a player can pay rent to another player.
        """
        self.player1.money = 500
        self.player2.money = 1000
        self.player1.pay_rent(200, self.player2)
        self.assertEqual(self.player1.money, 300)
        self.assertEqual(self.player2.money, 1200)

    def test_go_to_jail(self):
        """
        Test that a player can go to jail.
        """
        self.player1.go_to_jail()
        self.assertTrue(self.player1.in_jail)
        self.assertEqual(self.player1.position, 10)

    def test_declare_bankruptcy(self):
        """
        Test that a player can declare bankruptcy.
        """
        self.player1.declare_bankruptcy()
        self.assertEqual(self.player1.money, 0)
        self.assertEqual(len(self.player1.estates), 0)

    def test_sell_estate(self):
        """
        Test that a player can sell an estate to another player.
        """
        class MockEstate:
            """
            A mock estate class for testing.
            """
            def __init__(self, name, cost, street_group):
                self.name = name
                self.cost = cost
                self.street_group = street_group
                self.owner = None

            def change_owner(self, owner_name):
                """
                Change the owner of the estate.
                """
                self.owner = owner_name

        estate = MockEstate(name="Boardwalk", cost=400, street_group=1)
        self.player1.buy_estate(estate)
        self.player1.sell_estate(estate, self.player2, 400)
        self.assertEqual(self.player1.money, 1500)
        self.assertEqual(self.player2.money, 1100)
        self.assertIn(estate, self.player2.estates)
        self.assertNotIn(estate, self.player1.estates)


if __name__ == '__main__':
    unittest.main()
