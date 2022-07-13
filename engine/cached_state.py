from engine.evaluable_state import EvaluableState
from utils.metaclasses import CacheMeta


class CachedState(EvaluableState, metaclass=CacheMeta):
    pass
