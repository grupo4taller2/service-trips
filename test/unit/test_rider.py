from src.domain.rider import Rider


def test_rider_name():
    rider: Rider = Rider('mateo')
    assert rider.username == 'mateo'
