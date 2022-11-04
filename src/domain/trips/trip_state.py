from src.domain.driver import Driver


class TripState:
    def __init__(self, name):
        self.name: str = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def taken_by(self, driver: Driver):
        raise NotImplementedError

    # FIXME: Move to trip?
    def driver_username(self):
        raise NotImplementedError

    def driver_latitude(self):
        raise NotImplementedError

    def driver_longitude(self):
        raise NotImplementedError


class LookingForDriverState(TripState):
    def __init__(self):
        super().__init__('looking_for_driver')

    def taken_by(self, driver: Driver):
        return AcceptedByDriverState(driver)


class AcceptedByDriverState(TripState):
    def __init__(self, driver: Driver):
        super().__init__('accepted_by_driver')
        self.driver = driver

    def driver_username(self):
        return self.driver.username

    def driver_latitude(self):
        return self.driver.location.latitude

    def driver_longitude(self):
        return self.driver.location.longitude


class DriverWaitingState(TripState):
    pass


class OngoingState(TripState):
    pass


class FinishedState(TripState):
    pass


class TripFacade:
    NAMES_TO_TYPES = {
        'looking_for_driver': LookingForDriverState,
        'accepted_by_driver': AcceptedByDriverState
    }

    def create_from_name(self, state_name: str):
        return self.NAMES_TO_TYPES[state_name]()
