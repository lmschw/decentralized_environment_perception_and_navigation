import numpy as np

class DebugPolicy:

    def __init__(self):
        self.step = 0

    def __call__(self, observations):

        actions = []

        for i, _ in enumerate(observations):
            actions.append(
                {
                    "left": np.random.uniform(-1.0, 1.0),
                    "right": np.random.uniform(-1.0, 1.0),
                    "broadcast": i,
                }
            )

        self.step += 1

        return actions