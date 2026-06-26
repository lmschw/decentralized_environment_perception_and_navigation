from swarmrl.environment.maze import MazeGenerator
from swarmrl.environment.visualization import render_maze

maze = MazeGenerator(width=21, height=21, seed=42).generate()

render_maze(maze, title="Deterministic Maze (seed=42)")