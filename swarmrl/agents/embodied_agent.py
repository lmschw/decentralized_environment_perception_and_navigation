class EmbodiedAgent:

    def __init__(self, index, robot, sensor):

        self.index = index

        self.robot = robot
        self.sensor = sensor

        # Diagnostics only
        self.distance_travelled = 0.0
        self.previous_position = None

        self.collisions = 0