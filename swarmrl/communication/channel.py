import numpy as np


class CommunicationChannel:
    """
    Stateless local broadcast channel.

    Every timestep each robot broadcasts exactly one integer.
    Nearby robots receive a list of integers.
    """

    def __init__(self, radius=0.20):
        self.radius = 0.5

    def transmit(self, agents):
        """
        Parameters
        ----------
        agents : list[EmbodiedAgent]

        Returns
        -------
        list[list[int]]

        One inbox per robot.
        """

        positions = [
            agent.robot.get_position()
            for agent in agents
        ]

        inboxes = []

        for i in range(len(agents)):

            inbox = []

            for j in range(len(agents)):

                if i == j:
                    continue

                distance = np.linalg.norm(
                    positions[i] - positions[j]
                )

                if distance <= self.radius:

                    inbox.append(
                        agents[j].broadcast
                    )

            inboxes.append(inbox)

        return inboxes