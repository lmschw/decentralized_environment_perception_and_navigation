class Experiment:

    def __init__(self, config):
        self.config = config
        self.seed = config.environment.seed

    def run(self):
        print("Experiment started")
        print("Seed:", self.seed)
        print("Experiment finished")