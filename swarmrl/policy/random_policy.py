import numpy as np


class RandomPolicy:
    def __call__(self, obs):
        # return wheel speeds (left, right)
        return np.random.uniform(-1, 1, size=2)