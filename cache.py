

class LegalChoicesCache:
    def __init__(self, pickle_path=None):
        # todo: load cache
        self._map = {}

    def legal_movements(self, state):
        if state not in self._map:
            legal_choices = []
            for vector in state.valid_choices(state.next_side):
                result = state.create_from_vector(vector)
                try:
                    legal_choices.append(result.is_legal())
                except ValueError:
                    pass
                self._map[state] = legal_choices
        return self._map[state]

    @property
    def size(self):
        return len(self._map)

    @property
    def memory(self):
        return self._map.__sizeof__()


cache = LegalChoicesCache()
