from src.domain.driver import Driver


def test_driver_name():
    driver: Driver = Driver('mateo')
    assert driver.username == 'mateo'
