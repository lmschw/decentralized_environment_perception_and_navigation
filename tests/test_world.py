from swarmrl.environment.maze import MazeGenerator
from swarmrl.environment.pybullet_world import World

def test_world_initialization():
    maze = MazeGenerator(11, 11, 42).generate()
    world = World(maze, gui=False)

    assert world.maze.shape == (11, 11)