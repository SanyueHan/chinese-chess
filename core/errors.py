

class RuleViolatedError(Exception):
    pass


class ExceedBoardError(RuleViolatedError):
    """
    Raised if the target of a movement falls beyond the board
    """


class ExceedBoundaryError(RuleViolatedError):
    """
    Raised if the target of a movement falls beyond its boundary
    """


class AttackFriendError(RuleViolatedError):
    """
    Raised if a piece is attacking a friend
    """


class NotOneRackError(RuleViolatedError):
    """
    Raised if no rack exists when cannon is attacking
    """


class PathBlockedError(RuleViolatedError):
    """
    Raised if obstacles exist in moving path of a piece
    """
