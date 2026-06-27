from swarmrl.core.config import load_config
from swarmrl.environment.swarm_env import SwarmEnv
from swarmrl.policy.random_policy import RandomPolicy

config = load_config("configs/default.yaml")

env = SwarmEnv(config, gui=True)

policy = RandomPolicy()

obs, info = env.reset()

while True:

    actions = policy(obs)

    obs, reward, terminated, truncated, info = env.step(actions)