from __future__ import annotations

import numpy as np
import math

from swarmrl.environment.maze import MazeGenerator
from swarmrl.environment.pybullet_world import World
from swarmrl.environment.coverage import CoverageTracker

from swarmrl.agents.embodied_agent import EmbodiedAgent
from swarmrl.embodiment.thymio import ThymioRobot
from swarmrl.sensing.raycast import RaySensor

class SwarmEnv:
    """
    Gym-style environment wrapper.

    Responsibilities:
        - episode management
        - spawning agents
        - observations
        - rewards
        - termination

    World is responsible only for physics.
    """

    def __init__(
        self,
        config,
        num_agents=1,
        robot_cls=ThymioRobot,
        sensor_cls=RaySensor,
        agent_cls=EmbodiedAgent,
        gui=True,
    ):
        self.config = config
        self.gui = gui

        self.num_agents = num_agents

        self.robot_cls = robot_cls
        self.sensor_cls = sensor_cls
        self.agent_cls = agent_cls

        self.world = None
        self.agents = []

        self.step_count = 0

    def reset(self, seed=None):
        """
        Starts a new episode.
        """

        if self.world is not None:
            self.world.close()

        maze = MazeGenerator(
            width=self.config.environment.width,
            height=self.config.environment.height,
            seed=seed if seed is not None else self.config.environment.seed,
        ).generate()

        self.coverage_tracker = CoverageTracker(maze)

        self.world = World(maze, gui=self.gui)

        self.agents = []

        spawn_positions = self._sample_spawn_positions(
            maze,
            seed if seed is not None else self.config.environment.seed,
        )

        for i, position in enumerate(spawn_positions):

            agent = self.agent_cls(
                index=i,
                robot=self.robot_cls(),
                sensor=self.sensor_cls(),
            )

            self.world.add_robot(
                agent.robot,
                position,
            )

            self.agents.append(agent)

        for agent in self.agents:
            agent.previous_position = agent.robot.get_position()
        self.step_count = 0

        observations = self._collect_observations()

        info = {
            "step": self.step_count,
            "num_agents": len(self.agents),
            **self._collect_metrics(),
        }

        return observations, info

    def step(self, actions):
        """
        Advance the simulation by one timestep.

        Parameters
        ----------
        actions : list[dict]
            One action dictionary per agent.
        """

        self.step_count += 1

        for agent, action in zip(self.agents, actions):
            agent.robot.set_wheel_speeds(
                action["left"],
                action["right"],
            )

        self.world.step()

        for agent in self.agents:
            position = agent.robot.get_position()

            if agent.previous_position is not None:

                agent.distance_travelled += np.linalg.norm(
                    position - agent.previous_position
                )

            agent.previous_position = position

        positions = [
            agent.robot.get_position()
            for agent in self.agents
        ]

        self.coverage_tracker.update(
            positions,
            self.world.cell_size,
        )

        for agent in self.agents:

            if agent.robot.get_contacts():
                agent.collisions += 1

        observations = self._collect_observations()

        rewards = [0.0 for _ in self.agents]

        terminated = [False for _ in self.agents]
        truncated = [False for _ in self.agents]

        info = {
            "step": self.step_count,
            "num_agents": len(self.agents),
            **self._collect_metrics(),
        }

        print(info)

        return (
            observations,
            rewards,
            terminated,
            truncated,
            info,
        )

    def _collect_observations(self):
        observations = []

        for agent in self.agents:
            observations.append(
                {
                    "proximity": agent.sensor.sense(
                        agent.robot.body_id
                    )
                }
            )

        return observations

    def render(self):
        pass  # PyBullet GUI already renders

    def close(self):
        if self.world is not None:
            self.world.close()
            self.world = None

    def _sample_spawn_positions(self, maze, seed):
        """
        Deterministically sample spawn locations with a minimum spacing.
        """

        rng = np.random.default_rng(seed)

        height, width = maze.shape

        candidates = [
            (x, y)
            for y in range(height)
            for x in range(width)
            if maze[y, x] == 0
        ]

        rng.shuffle(candidates)

        positions = []

        min_distance = 2  # cells

        for candidate in candidates:

            if all(
                math.dist(candidate, existing) >= min_distance
                for existing in positions
            ):
                positions.append(candidate)

            if len(positions) == self.num_agents:
                break

        if len(positions) != self.num_agents:
            raise RuntimeError(
                "Could not find enough valid spawn positions."
            )

        return positions
    
    def _collect_metrics(self):
        return {
            "coverage": self.coverage_tracker.coverage,
            "explored_cells": len(self.coverage_tracker.visited),
            "distance_travelled": [
                agent.distance_travelled
                for agent in self.agents
            ],
            "collisions": [
                agent.collisions
                for agent in self.agents
            ],
        }