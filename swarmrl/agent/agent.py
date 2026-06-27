class Agent:
    def __init__(self, robot, sensor, policy):
        self.robot = robot
        self.sensor = sensor
        self.policy = policy

    def act(self, world):
        obs = self.sensor.sense(self.robot.body_id)
        action = self.policy(obs)

        self.robot.set_wheel_speeds(*action)

        return obs, action