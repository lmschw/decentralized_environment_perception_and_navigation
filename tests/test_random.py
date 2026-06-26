
from swarmrl.core.random import RandomManager


def test_rng_is_deterministic():
    rng1 = RandomManager(42)
    rng2 = RandomManager(42)

    assert rng1.rng.random() == rng2.rng.random()