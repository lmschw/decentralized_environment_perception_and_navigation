from __future__ import annotations

from swarmrl.environment.maze import MazeGenerator
from swarmrl.environment.pybullet_world import World

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
        robot_cls=ThymioRobot,
        sensor_cls=RaySensor,
        agent_cls=EmbodiedAgent,
        gui=True,
    ):
        self.config = config
        self.gui = gui

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

        self.world = World(maze, gui=self.gui)

        self.agents = []

        # Sprint 1.4: one anonymous robot
        agent = self.agent_cls(
            robot=self.robot_cls(),
            sensor=self.sensor_cls(),
        )

        self.world.add_robot(agent.robot)

        self.agents.append(agent)

        self.step_count = 0

        observations = self._collect_observations()

        info = {}

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

        observations = self._collect_observations()

        rewards = [0.0 for _ in self.agents]

        terminated = [False for _ in self.agents]
        truncated = [False for _ in self.agents]

        info = {
            "step": self.step_count,
        }

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

    def close(self):
        """
        Close the environment.
        """

        if self.world is not None:
            self.world.close()
            self.world = None