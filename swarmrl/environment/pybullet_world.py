import pybullet as p
import pybullet_data
import time
import numpy as np


class World:
    """
    PyBullet simulation wrapper for SwarmRL.

    Responsibilities:
    - physics setup
    - maze rendering
    - robot management
    - stepping simulation
    """

    def __init__(self, maze: np.ndarray, gui: bool = True):
        self.maze = maze
        self.gui = gui

        self.client = p.connect(p.GUI if gui else p.DIRECT)

        self.dt = 1 / 240

        p.setTimeStep(self.dt)
        p.setRealTimeSimulation(0)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)

        self.cell_size = 0.05

        self.robots = []

        self._load_plane()
        self._load_maze()
        self._setup_camera()

    # ---------------------------------------------------------
    # Static world
    # ---------------------------------------------------------
    def _load_plane(self):
        p.loadURDF("plane.urdf")

    def _load_maze(self):
        h, w = self.maze.shape

        wall_collision = p.createCollisionShape(
            shapeType=p.GEOM_BOX,
            halfExtents=[self.cell_size / 2] * 3,
        )

        wall_visual = p.createVisualShape(
            shapeType=p.GEOM_BOX,
            halfExtents=[self.cell_size / 2] * 3,
            rgbaColor=[0.1, 0.1, 0.1, 1],
        )

        for y in range(h):
            for x in range(w):
                if self.maze[y, x] == 1:

                    wall_id = p.createMultiBody(
                        baseMass=0,
                        baseCollisionShapeIndex=wall_collision,
                        baseVisualShapeIndex=wall_visual,
                        basePosition=[
                            x * self.cell_size,
                            y * self.cell_size,
                            self.cell_size / 2,
                        ],
                    )

                    p.changeDynamics(
                        wall_id,
                        -1,
                        lateralFriction=1.0,
                        restitution=0.0,
                    )

    def _setup_camera(self):
        h, w = self.maze.shape

        center_x = (w * self.cell_size) / 2
        center_y = (h * self.cell_size) / 2

        p.resetDebugVisualizerCamera(
            cameraDistance=max(h, w) * self.cell_size * 0.8,
            cameraYaw=0,
            cameraPitch=-89,  # near top-down
            cameraTargetPosition=[center_x, center_y, 0],
        )

    # ---------------------------------------------------------
    # Robot management
    # ---------------------------------------------------------
    def add_robot(self, robot, position):
        """
        Add a robot to the simulation.

        Parameters
        ----------
        robot : Robot
            Robot instance.

        position : tuple[int, int]
            Maze cell coordinates (x, y).
        """

        self.robots.append(robot)

        robot.spawn(
            self.client,
            self.cell_size,
            grid_position=position,
        )
    # ---------------------------------------------------------
    # Simulation loop
    # ---------------------------------------------------------
    def step(self, dt: float = 1 / 240):
        for robot in self.robots:
            robot.apply_action(dt)
            robot.physics_step()

        p.stepSimulation()

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------
    def close(self):
        p.disconnect()