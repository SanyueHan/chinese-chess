import unittest

from core.consts.boards import OFFENSIVE_DOWN
from core.role import Role
from engine.derivable_state import DerivableState


class TestChildren(unittest.TestCase):
    def test_1(self):
        state = DerivableState(board=OFFENSIVE_DOWN, current_player=Role.OFFENSIVE)
        self.assertEqual(len(state.children), 44)


if __name__ == "__main__":
    unittest.main()
