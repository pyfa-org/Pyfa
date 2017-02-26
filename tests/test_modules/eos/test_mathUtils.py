from eos.mathUtils import floorFloat


def test_floorFloat():
    assert type(floorFloat(1)) is not float
    assert type(floorFloat(1)) is int
    assert type(floorFloat(1.1)) is not float
    assert type(floorFloat(1.1)) is int
    assert floorFloat(1.1) == 1
    assert floorFloat(1.9) == 1
    assert floorFloat(1.5) == 1
    assert floorFloat(-1.5) == -2
