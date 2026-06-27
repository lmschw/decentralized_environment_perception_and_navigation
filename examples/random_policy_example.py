from swarmrl.core.config import load_config
from swarmrl.environment.swarm_env import SwarmEnv
from swarmrl.policy.random_policy import RandomPolicy

config = load_config("configs/default.yaml")

env = SwarmEnv(
    config,
    num_agents=10,
)

policy = RandomPolicy()

obs, info = env.reset()

while True:
    actions = policy(obs)

    obs, rewards, terminated, truncated, info = env.step(actions)

    if info["step"] % 100 == 0:
        print(
            f"Step {info['step']:4d} | "
            f"Coverage: {info['coverage']:.1%} | "
            f"Distance: {sum(info['distance_travelled']):.2f} m | "
            f"Collisions: {sum(info['collisions'])}"
        )