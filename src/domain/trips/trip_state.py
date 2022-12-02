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

    def transition(self, driver, new_state):
        raise NotImplementedError


class LookingForDriverState(TripState):
    def __init__(self, driver=None):
        super().__init__('looking_for_driver')

    def taken_by(self, driver: Driver):
        raise NotImplementedError
        # return AcceptedByDriverState(driver)

    def transition(self, driver, new_state):
        # FIXME: Cancelaciones se tratarían acá con un hashmap
        # de estados posibles, por ejemplo
        if isinstance(new_state, AcceptedByDriverState):
            return AcceptedByDriverState(driver)
        return LookingForDriverState(driver)


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

    def transition(self, driver, new_state):
        # FIXME: Cancelaciones se tratarían acá con un hashmap
        # de estados posibles, por ejemplo
        if isinstance(new_state, DriverWaitingState):
            return DriverWaitingState(driver)
        return AcceptedByDriverState(driver)


class DriverWaitingState(TripState):
    def __init__(self, driver: Driver):
        super().__init__('driver_arrived')
        self.driver = driver

    def driver_username(self):
        return self.driver.username

    def driver_latitude(self):
        return self.driver.location.latitude

    def driver_longitude(self):
        return self.driver.location.longitude

    def transition(self, driver, new_state):
        # FIXME: Cancelaciones se tratarían acá con un hashmap
        # de estados posibles, por ejemplo
        if isinstance(new_state, OngoingState):
            return OngoingState(driver)
        return DriverWaitingState(driver)


class OngoingState(TripState):
    def __init__(self, driver: Driver):
        super().__init__('start_confirmed_by_driver')
        self.driver = driver

    def driver_username(self):
        return self.driver.username

    def driver_latitude(self):
        return self.driver.location.latitude

    def driver_longitude(self):
        return self.driver.location.longitude

    def transition(self, driver, new_state):
        # FIXME: Cancelaciones se tratarían acá con un hashmap
        # de estados posibles, por ejemplo
        if isinstance(new_state, FinishedState):
            return FinishedState(driver)
        return OngoingState(driver)


class FinishedState(TripState):
    def __init__(self, driver: Driver):
        super().__init__('finished_confirmed_by_driver')
        self.driver = driver

    def driver_username(self):
        return self.driver.username

    def driver_latitude(self):
        return self.driver.location.latitude

    def driver_longitude(self):
        return self.driver.location.longitude

    def transition(self, driver, new_state):
        # FIXME: Cancelaciones se tratarían acá con un hashmap
        # de estados posibles, por ejemplo
        return FinishedState(driver)


class TripFacade:
    NAMES_TO_TYPES = {
        'looking_for_driver': LookingForDriverState,
        'accepted_by_driver': AcceptedByDriverState,
        'driver_arrived': DriverWaitingState,
        'start_confirmed_by_driver': OngoingState,
        'finished_confirmed_by_driver': FinishedState
    }

    @classmethod
    def create_from_name(cls, state_name: str, driver: Driver = None):
        return cls.NAMES_TO_TYPES[state_name](driver)
