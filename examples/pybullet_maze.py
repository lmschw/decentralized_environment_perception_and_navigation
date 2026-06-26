from swarmrl.environment.maze import MazeGenerator
from swarmrl.environment.pybullet_world import World
from swarmrl.embodiment.thymio import ThymioRobot

maze = MazeGenerator(21, 21, seed=42).generate()

world = World(maze, gui=True)

robot = ThymioRobot()
world.add_robot(robot)

for _ in range(40000):
    robot.set_wheel_speeds(1.0, 0.5)
    world.step()
    print("loop tick")

world.close()