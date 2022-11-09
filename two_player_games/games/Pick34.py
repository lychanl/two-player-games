import itertools
from typing import Iterable, List, Optional
from two_player_games.game import Game
from two_player_games.move import Move
from two_player_games.player import Player
from two_player_games.state import State


class Pick34(Game):
    """Class that represents the Pick34 game"""
    FIRST_PLAYER_DEFAULT_CHAR = '1'
    SECOND_PLAYER_DEFAULT_CHAR = '2'

    def __init__(self, first_player: Player = None, second_player: Player = None):
        """
        Initializes game.

        Parameters:
            first_player: the player that will go first (if None is passed, a player will be created)
            second_player: the player that will go second (if None is passed, a player will be created)
        """
        self.first_player = first_player or Player(self.FIRST_PLAYER_DEFAULT_CHAR)
        self.second_player = second_player or Player(self.SECOND_PLAYER_DEFAULT_CHAR)

        state = Pick34State(self.first_player, self.second_player)

        super().__init__(state)


class Pick34Move(Move):
    """
    Class that represents a move in the Pick15Move game

    Variables:
        number: selected number (from 1 to 16)
    """

    def __init__(self, number: int):
        self.number = number

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Pick34Move):
            return False
        return self.number == o.number


class Pick34State(State):
    """Class that represents a state in the Pick15State game"""
    MAX_NUMBER = 16
    AIM_VALUE = 34

    def __init__(self,
                 current_player: Player, other_player: Player,
                 current_player_numbers: List[int] = None,
                 other_player_numbers: List[int] = None):
        """Creates the state. Do not call directly."""

        if current_player_numbers is None:
            current_player_numbers = []
        if other_player_numbers is None:
            other_player_numbers = []

        self.current_player_numbers = current_player_numbers
        self.other_player_numbers = other_player_numbers
        self.selected_numbers = set(self.current_player_numbers).union(self.other_player_numbers)
        super().__init__(current_player, other_player)

    def get_moves(self) -> Iterable[Pick34Move]:
        return [Pick34Move(number) for number in range(1, self.MAX_NUMBER + 1) if number not in self.selected_numbers]

    def make_move(self, move: Pick34Move) -> 'Pick34State':
        if move.number > self.MAX_NUMBER or move.number in self.selected_numbers:
            raise ValueError("Invalid move")
        else:
            self.current_player_numbers.append(move.number)

            next_player = self._other_player
            next_player_numbers = self.other_player_numbers

            other_player = self._current_player
            other_player_numbers = self.current_player_numbers

        return Pick34State(
            next_player, other_player, next_player_numbers, other_player_numbers
        )

    def is_finished(self) -> bool:
        return self._check_if_sums_to_aim_value(self.current_player_numbers) or \
               self._check_if_sums_to_aim_value(self.other_player_numbers) or \
               len(self.selected_numbers) == self.MAX_NUMBER

    def get_winner(self) -> Optional[Player]:
        if not self.is_finished():
            return None
        if self._check_if_sums_to_aim_value(self.current_player_numbers):
            return self._current_player
        elif self._check_if_sums_to_aim_value(self.other_player_numbers):
            return self._other_player
        else:
            return None

    def __str__(self) -> str:
        return f"Current player: {self._current_player.char}, Numbers: " \
               f"{'[]' if not self.current_player_numbers else sorted(self.current_player_numbers)}," \
               f"\nOther player: {self._other_player.char}, Numbers: " \
               f"{'[]' if not self.other_player_numbers else sorted(self.other_player_numbers)}"

    # below are helper methods for the public interface

    def _check_if_sums_to_aim_value(self, numbers: List[int]) -> bool:
        return self.AIM_VALUE in [sum(i) for i in itertools.combinations(numbers, 4)]
