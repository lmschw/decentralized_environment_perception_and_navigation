from dataclasses import dataclass, field
import yaml

@dataclass(slots=True)
class PhysicsConfig:
    timestep: float = 1.0 / 240.0


@dataclass(slots=True)
class EnvironmentConfig:
    width: int = 20
    height: int = 20
    seed: int = 42


@dataclass(slots=True)
class RobotConfig:
    radius: float = 0.08
    wheel_base: float = 0.095


@dataclass(slots=True)
class ExperimentConfig:
    physics: PhysicsConfig = field(default_factory=PhysicsConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    robot: RobotConfig = field(default_factory=RobotConfig)

def load_config(path: str) -> ExperimentConfig:
    """
    Load YAML config and convert it into strongly typed ExperimentConfig.
    """
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    physics = PhysicsConfig(**raw.get("physics", {}))
    environment = EnvironmentConfig(**raw.get("environment", {}))
    robot = RobotConfig(**raw.get("robot", {}))

    return ExperimentConfig(
        physics=physics,
        environment=environment,
        robot=robot,
    )