Maze Representation

We use a 2D occupancy grid.

Reason:
- Direct mapping to PyBullet collision geometry
- Simple observation extraction later
- Deterministic and testable

Tradeoff:
- Less expressive than graph-based mazes
- Harder to represent irregular geometry (ignored for now)


Physics backend: PyBullet

Reason:
- sufficient realism for swarm robotics research
- fast iteration cycle
- supports rigid body dynamics

Tradeoff:
- not high fidelity soft-body simulation
- limited sensor realism

Decision:
keep abstraction boundary so backend can be replaced later