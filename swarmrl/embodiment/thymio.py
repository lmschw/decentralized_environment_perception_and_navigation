import numpy as np
import pybullet as p


class ThymioRobot:
    """
    Minimal differential-drive robot used by SwarmRL.

    The robot exposes only:
      - differential wheel speeds
      - body pose
      - body velocity

    Sensors and communication are handled elsewhere.
    """

    def __init__(
        self,
        radius: float = 0.015,
        height: float = 0.020,
        mass: float = 0.05,
        wheel_base: float = 0.05,
        speed_scale: float = 0.20,
    ):
        # Physical parameters
        self.radius = radius
        self.height = height
        self.mass = mass
        self.wheel_base = wheel_base
        self.speed_scale = speed_scale

        # PyBullet state
        self.body_id = None
        self.client = None
        self.cell_size = None

        # Control state
        self.left_speed = 0.0
        self.right_speed = 0.0

        # Computed body velocities
        self.v = 0.0
        self.omega = 0.0

    # ------------------------------------------------------------------
    # Spawn
    # ------------------------------------------------------------------

    def spawn(self, client, cell_size, grid_position):
        self.client = client
        self.cell_size = cell_size

        grid_x, grid_y = grid_position

        # Spawn in the centre of the maze cell
        x = (grid_x + 0.5) * cell_size
        y = (grid_y + 0.5) * cell_size
        z = self.radius

        collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=self.radius,
            height=self.height,
        )

        visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=self.radius,
            length=self.height,
            rgbaColor=[0.2, 0.3, 0.8, 1.0],
        )

        self.body_id = p.createMultiBody(
            baseMass=self.mass,
            baseCollisionShapeIndex=collision,
            baseVisualShapeIndex=visual,
            basePosition=[x, y, z],
            baseOrientation=p.getQuaternionFromEuler([0, 0, 0]),
        )

        # Temporary random colours to distinguish robots
        color = np.random.default_rng().uniform(0.2, 1.0, 3)

        p.changeVisualShape(
            self.body_id,
            -1,
            rgbaColor=[color[0], color[1], color[2], 1.0],
        )

        p.changeDynamics(
            self.body_id,
            -1,
            lateralFriction=1.2,
            linearDamping=0.01,
            angularDamping=0.01,
            restitution=0.0,
        )

    # ------------------------------------------------------------------
    # Actuation
    # ------------------------------------------------------------------

    def set_wheel_speeds(self, left: float, right: float):
        self.left_speed = float(left)
        self.right_speed = float(right)

    def apply_action(self, dt: float = 1 / 240):
        """
        Convert wheel speeds into body linear/angular velocity.
        """

        self.v = (
            self.speed_scale
            * (self.left_speed + self.right_speed)
            / 2.0
        )

        self.omega = (
            self.speed_scale
            * (self.right_speed - self.left_speed)
            / self.wheel_base
        )

    # ------------------------------------------------------------------
    # Physics
    # ------------------------------------------------------------------

    def physics_step(self):
        if self.body_id is None:
            return

        _, orn = p.getBasePositionAndOrientation(self.body_id)

        _, _, theta = p.getEulerFromQuaternion(orn)

        vx = self.v * np.cos(theta)
        vy = self.v * np.sin(theta)

        p.resetBaseVelocity(
            self.body_id,
            linearVelocity=[vx, vy, 0.0],
            angularVelocity=[0.0, 0.0, self.omega],
        )

    def get_position(self):
        pos, _ = p.getBasePositionAndOrientation(self.body_id)
        return np.array(pos[:2])
    
    def get_heading(self):
        _, orn = p.getBasePositionAndOrientation(self.body_id)

        _, _, yaw = p.getEulerFromQuaternion(orn)

        return yaw
    
    def get_contacts(self):
        if self.body_id is None:
            return []

        return p.getContactPoints(self.body_id)