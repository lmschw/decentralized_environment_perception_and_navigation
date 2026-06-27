import numpy as np


class CoverageTracker:
    """
    Tracks how much of the free space has been explored by the swarm.

    Coverage is measured as the fraction of free maze cells that have been
    visited by at least one robot.
    """

    def __init__(self, maze):
        self.maze = maze

        self.height, self.width = maze.shape

        # Number of traversable cells
        self.free_cells = np.count_nonzero(maze == 0)

        # Set of visited maze cells
        self.visited = set()

    def update(self, positions, cell_size):
        """
        Update coverage with the current robot positions.

        Parameters
        ----------
        positions : iterable[np.ndarray]
            Robot positions in world coordinates.

        cell_size : float
            Size of one maze cell.
        """

        for pos in positions:

            x = int(pos[0] / cell_size)
            y = int(pos[1] / cell_size)

            if (
                0 <= x < self.width
                and
                0 <= y < self.height
                and
                self.maze[y, x] == 0
            ):
                self.visited.add((x, y))

    @property
    def coverage(self):
        if self.free_cells == 0:
            return 0.0

        return len(self.visited) / self.free_cells
    
    @property
    def explored_cells(self):
        return self.visited