

class RuleViolatedError(Exception):
    pass


class ExceedBoundaryError(RuleViolatedError):
    """
    Raised if the target of a movement falls beyond its boundary
    """


class AttackFriendError(RuleViolatedError):
    """
    Raised if a piece is attacking a friend
    """


class NoRackError(RuleViolatedError):
    """
    Raised if no rack exists when cannon is attacking
    """


class PathBlockedError(RuleViolatedError):
    """
    Raised if obstacles exist in moving path of a piece
    """
