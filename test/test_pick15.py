import unittest

from two_player_games.games.Pick15 import Pick15, Pick15Move


class TestPick15(unittest.TestCase):
    def test_init(self):
        game = Pick15()
        self.assertEqual(str(game), "Current player: 1, Numbers: [],\nOther player: 2, Numbers: []")
        self.assertIs(game.get_current_player(), game.first_player)

    def test_moves(self):
        game = Pick15()

        game.make_move(Pick15Move(1))
        self.assertEqual(str(game), "Current player: 2, Numbers: [],\nOther player: 1, Numbers: [1]")
        self.assertIs(game.get_current_player(), game.second_player)

        game.make_move(Pick15Move(2))
        self.assertEqual(str(game), "Current player: 1, Numbers: [1],\nOther player: 2, Numbers: [2]")
        self.assertIs(game.get_current_player(), game.first_player)

        game.make_move(Pick15Move(5))
        game.make_move(Pick15Move(7))

        self.assertEqual(str(game), "Current player: 1, Numbers: [1, 5],\nOther player: 2, Numbers: [2, 7]")
        self.assertIs(game.get_current_player(), game.first_player)

    def test_get_moves(self):
        game = Pick15()

        game.make_move(Pick15Move(5))
        game.make_move(Pick15Move(7))
        game.make_move(Pick15Move(3))

        self.assertSequenceEqual(
            game.get_moves(), [Pick15Move(number) for number in [1, 2, 4, 6, 8, 9]]
        )

    def test_invalid_move(self):
        game = Pick15()

        self.assertRaises(ValueError, lambda: game.make_move(Pick15Move(11)))

        game.make_move(Pick15Move(4))
        self.assertRaises(ValueError, lambda: game.make_move(Pick15Move(4)))

    def test_winner_and_finished(self):
        game = Pick15()

        game.make_move(Pick15Move(4))
        game.make_move(Pick15Move(9))
        game.make_move(Pick15Move(5))
        game.make_move(Pick15Move(6))

        self.assertFalse(game.is_finished())
        self.assertIsNone(game.get_winner())

        game.make_move(Pick15Move(3))
        game.make_move(Pick15Move(8))
        game.make_move(Pick15Move(7))

        self.assertTrue(game.is_finished())
        self.assertIs(game.get_winner(), game.first_player)

    def test_winner_and_finished_draw(self):
        game = Pick15()

        game.make_move(Pick15Move(5))
        game.make_move(Pick15Move(8))
        game.make_move(Pick15Move(3))
        game.make_move(Pick15Move(7))

        self.assertFalse(game.is_finished())
        self.assertIsNone(game.get_winner())

        game.make_move(Pick15Move(9))
        game.make_move(Pick15Move(1))
        game.make_move(Pick15Move(6))
        game.make_move(Pick15Move(4))
        game.make_move(Pick15Move(2))

        self.assertEqual([], game.get_moves())
        self.assertTrue(game.is_finished())
        self.assertIsNone(game.get_winner())
