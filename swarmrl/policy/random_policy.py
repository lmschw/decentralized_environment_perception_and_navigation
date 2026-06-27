import numpy as np


class RandomPolicy:
    def __call__(self, observations):
        actions = []

        for _ in observations:

            actions.append({
                "left": np.random.uniform(-1, 1),
                "right": np.random.uniform(-1, 1),
            })

        return actions