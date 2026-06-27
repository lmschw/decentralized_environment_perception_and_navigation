import pybullet as p
import numpy as np


class RaySensor:
    def __init__(self, num_rays=7, max_dist=0.2):
        self.num_rays = num_rays
        self.max_dist = max_dist

        # symmetric field of view (front-facing)
        self.angles = np.linspace(-np.pi/2, np.pi/2, num_rays)

    def sense(self, body_id):
        pos, orn = p.getBasePositionAndOrientation(body_id)
        _, _, yaw = p.getEulerFromQuaternion(orn)

        readings = []

        for a in self.angles:
            angle = yaw + a

            dx = np.cos(angle) * self.max_dist
            dy = np.sin(angle) * self.max_dist

            ray_from = pos
            ray_to = [pos[0] + dx, pos[1] + dy, pos[2]]

            result = p.rayTest(ray_from, ray_to)[0]

            hit_fraction = result[2]  # 0..1

            if result[0] == -1:
                readings.append(1.0)  # no hit
            else:
                readings.append(hit_fraction)

        return np.array(readings, dtype=np.float32)