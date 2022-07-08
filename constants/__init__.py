from enum import Enum

from .boards import BOARDS
from .coding import ENCODE, DECODE


class Role(Enum):
    OFFENSIVE = str.islower, None
    DEFENSIVE = str.isupper, None

    def __init__(self, iff_func, opponent):
        """
        :param iff_func: IFF (Identification Friend or Foe) function
        :param opponent:
        """
        self._iff_func = iff_func
        self._opponent = opponent

    def __repr__(self):
        return self.__str__()

    @property
    def iff_func(self):
        """
        :return: the function that returns True for self pieces and False for enemy pieces
        """
        return self._iff_func

    @property
    def opponent(self) -> 'Role':
        return self._opponent


Role.OFFENSIVE._opponent = Role.DEFENSIVE
Role.DEFENSIVE._opponent = Role.OFFENSIVE


def get_role(p):
    for role in Role:
        if role.iff_func(p):
            return role
    return None


if __name__ == "__main__":
    print(Role.OFFENSIVE.opponent)
    print(Role.DEFENSIVE.opponent)
