import pybullet as p
import numpy as np


class ThymioRobot:
    """
    Minimal differential-drive robot proxy for SwarmRL.

    - Physically simulated in PyBullet
    - Controlled via wheel speeds
    - Uses velocity control (NOT position reset)
    """

    def __init__(self):
        self.body_id = None

        # wheel commands
        self.left_speed = 0.0
        self.right_speed = 0.0

        # computed state
        self.v = 0.0
        self.omega = 0.0

        self.cell_size = None

    # ---------------------------------------------------------
    # Spawn
    # ---------------------------------------------------------
    def spawn(self, client, cell_size: float = 0.05):
        self.client = client
        self.cell_size = cell_size

        radius = 0.015
        height = 0.02
        mass = 0.05

        collision = p.createCollisionShape(
            shapeType=p.GEOM_CYLINDER,
            radius=radius,
            height=height,
        )

        visual = p.createVisualShape(
            shapeType=p.GEOM_CYLINDER,
            radius=radius,
            length=height,
            rgbaColor=[0.2, 0.3, 0.8, 1.0],
        )

        self.body_id = p.createMultiBody(
            baseMass=mass,
            baseCollisionShapeIndex=collision,
            baseVisualShapeIndex=visual,
            basePosition=[
                1 * cell_size,
                1 * cell_size,
                height / 2,
            ],
            baseOrientation=p.getQuaternionFromEuler([0, 0, 0]),
        )

        # stability tuning
        p.changeDynamics(
            self.body_id,
            -1,
            lateralFriction=1.2,
            linearDamping=0.2,
            angularDamping=0.2,
            restitution=0.0,
        )

    # ---------------------------------------------------------
    # Actuation interface
    # ---------------------------------------------------------
    def set_wheel_speeds(self, left: float, right: float):
        self.left_speed = left
        self.right_speed = right

    # ---------------------------------------------------------
    # Kinematics (compute velocity state)
    # ---------------------------------------------------------
    def apply_action(self, dt: float = 1 / 240):
        wheel_base = 0.05

        v_l = self.left_speed
        v_r = self.right_speed

        scale = 0.2  # tune factor

        self.v = scale * (self.left_speed + self.right_speed) / 2
        self.omega = scale * (self.right_speed - self.left_speed)

    # ---------------------------------------------------------
    # Physics step (IMPORTANT: no teleporting)
    # ---------------------------------------------------------
    def physics_step(self):
        if self.body_id is None:
            return

        pos, orn = p.getBasePositionAndOrientation(self.body_id)
        _, _, theta = p.getEulerFromQuaternion(orn)

        vx = self.v * np.cos(theta)
        vy = self.v * np.sin(theta)

        p.resetBaseVelocity(
            self.body_id,
            linearVelocity=[vx, vy, 0],
            angularVelocity=[0, 0, self.omega],
        )
