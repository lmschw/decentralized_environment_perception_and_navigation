class EmbodiedAgent:
    """
    Container for one anonymous swarm agent.
    """

    def __init__(self, robot, sensor):
        self.robot = robot
        self.sensor = sensor