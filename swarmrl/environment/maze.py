import numpy as np
from dataclasses import dataclass


@dataclass
class MazeGenerator:
    width: int
    height: int
    seed: int

    def generate(self) -> np.ndarray:
        rng = np.random.default_rng(self.seed)

        # grid: start fully walled
        maze = np.ones((self.height, self.width), dtype=np.int8)

        # start position
        start_x, start_y = 1, 1
        maze[start_y, start_x] = 0

        stack = [(start_x, start_y)]
        visited = set([(start_x, start_y)])

        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]

        while stack:
            x, y = stack[-1]

            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    1 <= nx < self.width - 1 and
                    1 <= ny < self.height - 1 and
                    (nx, ny) not in visited
                ):
                    neighbors.append((nx, ny))

            if not neighbors:
                stack.pop()
                continue

            nx, ny = neighbors[rng.integers(len(neighbors))]

            # carve path
            maze[ny, nx] = 0
            maze[y + (ny - y) // 2, x + (nx - x) // 2] = 0

            visited.add((nx, ny))
            stack.append((nx, ny))

        return maze
    
def generate_maze(width: int, height: int, seed: int) -> np.ndarray:
    return MazeGenerator(width, height, seed).generate()