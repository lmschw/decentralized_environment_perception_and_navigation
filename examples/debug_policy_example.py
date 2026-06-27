from swarmrl.core.config import load_config
from swarmrl.environment.swarm_env import SwarmEnv
from swarmrl.policy.debug_policy import DebugPolicy

config = load_config("configs/default.yaml")

env = SwarmEnv(
    config,
    num_agents=4,
    gui=True,
)

policy = DebugPolicy()

obs, info = env.reset()

while True:
    actions = policy(obs)

    obs, reward, terminated, truncated, info = env.step(actions)

    for i, observation in enumerate(obs):
        print(
            f"Robot {i} hears {observation['messages']}"
        )