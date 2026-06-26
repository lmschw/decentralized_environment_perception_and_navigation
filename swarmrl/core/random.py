import numpy as np

class RandomManager:
    def __init__(self, seed: int):
        self._rng = np.random.default_rng(seed)

    @property
    def rng(self):
        return self._rng