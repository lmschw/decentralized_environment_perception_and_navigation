from swarmrl.environment.maze import MazeGenerator


def test_maze_deterministic():
    m1 = MazeGenerator(21, 21, 42).generate()
    m2 = MazeGenerator(21, 21, 42).generate()

    assert (m1 == m2).all()


def test_maze_has_open_space():
    maze = MazeGenerator(21, 21, 42).generate()
    assert maze.sum() < maze.size  # not fully blocked