import matplotlib.pyplot as plt
import numpy as np


def render_maze(maze: np.ndarray, title: str = "Maze"):
    """
    Simple debug renderer for occupancy grids.

    0 = free space (white)
    1 = wall (black)
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(maze, cmap="binary")
    plt.title(title)
    plt.axis("off")
    plt.show()