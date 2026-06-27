import numpy as np


class RandomPolicy:
    def __init__(self, hold_steps=10):
        self.hold_steps = hold_steps
        self.counter = 0
        self.current_actions = None

    def __call__(self, observations):
        if (
            self.current_actions is None
            or self.counter % self.hold_steps == 0
        ):
            self.current_actions = [
                {
                    "left": np.random.uniform(-1.0, 1.0),
                    "right": np.random.uniform(-1.0, 1.0),
                    "broadcast": np.random.randint(0, 16)
                }
                for _ in observations
            ]

        self.counter += 1
        return self.current_actions