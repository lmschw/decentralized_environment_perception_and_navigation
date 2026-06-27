from swarmrl.environment.maze import MazeGenerator
from swarmrl.environment.pybullet_world import World
from swarmrl.embodiment.thymio import ThymioRobot
from swarmrl.sensing.raycast import RaySensor
from swarmrl.agent.agent import Agent
from swarmrl.policy.random_policy import RandomPolicy

maze = MazeGenerator(21, 21, 42).generate()
world = World(maze, gui=True)

robot = ThymioRobot()
world.add_robot(robot)

sensor = RaySensor(num_rays=7, max_dist=0.15)
policy = RandomPolicy()

agent = Agent(robot, sensor, policy)

while True:
    world.step([agent])