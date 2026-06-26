from swarmrl.core.config import load_config
from swarmrl.core.experiment import Experiment

config = load_config("configs/default.yaml")

experiment = Experiment(config)

experiment.run()