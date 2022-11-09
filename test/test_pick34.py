import unittest

from two_player_games.games.Pick34 import Pick34, Pick34Move


class TestPick34(unittest.TestCase):
    def test_init(self):
        game = Pick34()
        self.assertEqual(str(game), "Current player: 1, Numbers: [],\nOther player: 2, Numbers: []")
        self.assertIs(game.get_current_player(), game.first_player)

    def test_moves(self):
        game = Pick34()

        game.make_move(Pick34Move(1))
        self.assertEqual(str(game), "Current player: 2, Numbers: [],\nOther player: 1, Numbers: [1]")
        self.assertIs(game.get_current_player(), game.second_player)

        game.make_move(Pick34Move(2))
        self.assertEqual(str(game), "Current player: 1, Numbers: [1],\nOther player: 2, Numbers: [2]")
        self.assertIs(game.get_current_player(), game.first_player)

        game.make_move(Pick34Move(5))
        game.make_move(Pick34Move(16))

        self.assertEqual(str(game), "Current player: 1, Numbers: [1, 5],\nOther player: 2, Numbers: [2, 16]")
        self.assertIs(game.get_current_player(), game.first_player)

    def test_get_moves(self):
        game = Pick34()

        game.make_move(Pick34Move(5))
        game.make_move(Pick34Move(7))
        game.make_move(Pick34Move(3))
        game.make_move(Pick34Move(16))
        game.make_move(Pick34Move(15))
        game.make_move(Pick34Move(14))
        game.make_move(Pick34Move(12))

        self.assertSequenceEqual(
            game.get_moves(), [Pick34Move(number) for number in [1, 2, 4, 6, 8, 9, 10, 11, 13]]
        )

    def test_invalid_move(self):
        game = Pick34()

        self.assertRaises(ValueError, lambda: game.make_move(Pick34Move(21)))

        game.make_move(Pick34Move(4))
        self.assertRaises(ValueError, lambda: game.make_move(Pick34Move(4)))

    def test_winner_and_finished(self):
        game = Pick34()

        game.make_move(Pick34Move(7))
        game.make_move(Pick34Move(1))
        game.make_move(Pick34Move(9))
        game.make_move(Pick34Move(2))

        self.assertFalse(game.is_finished())
        self.assertIsNone(game.get_winner())

        game.make_move(Pick34Move(12))
        game.make_move(Pick34Move(8))
        game.make_move(Pick34Move(6))

        self.assertTrue(game.is_finished())
        self.assertIs(game.get_winner(), game.first_player)
