from swarmrl.core.config import load_config

def test_config_loads():
    config = load_config("configs/default.yaml")

    assert config.environment.width == 20