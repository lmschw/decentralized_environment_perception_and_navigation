Maze Representation

We use a 2D occupancy grid.

Reason:
- Direct mapping to PyBullet collision geometry
- Simple observation extraction later
- Deterministic and testable

Tradeoff:
- Less expressive than graph-based mazes
- Harder to represent irregular geometry (ignored for now)