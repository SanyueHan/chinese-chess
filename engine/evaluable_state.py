from TimeAnalyzer.metaclass import TimeAnalyzer
from engine.derivable_state import DerivableState


class EvaluableState(DerivableState, metaclass=TimeAnalyzer):
    """
    EvaluableState provide a score to evaluate the situation
    used as heuristic function in heuristic search
    """

    SCORE_TABLE = {
        'p': 2,
        'a': 3,
        'm': 3,
        'c': 5,
        'k': 5,
        'r': 10,
    }  # 62 in total

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__score = None

    @property
    def score(self) -> (int, int):
        if self.__score is None:
            self.__score = (self._get_exist_score(), self._get_power_score())
        return self.__score

    def _get_exist_score(self) -> int:
        """
        :return: 0 means game playing, 1 means self win, -1 means self lose
        """
        return bool(self._get_general_position(self.current_player)) - bool(self._get_general_position(self.current_player.opponent))

    def _get_power_score(self) -> int:
        self_power = sum(self.SCORE_TABLE.get(p.lower(), 0) for p in self._get_pieces(self.current_player).values())
        oppo_power = sum(self.SCORE_TABLE.get(p.lower(), 0) for p in self._get_pieces(self.current_player.opponent).values())
        return self_power - oppo_power
