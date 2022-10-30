class TripState:
    def __init__(self, name):
        self.name: str = name


class LookingForDriverState(TripState):
    def __init__(self):
        super().__init__('looking_for_driver')


class AcceptedByDriverState(TripState):
    pass


class DriverWaitingState(TripState):
    pass


class OngoingState(TripState):
    pass


class FinishedState(TripState):
    pass


class TripFacade:
    NAMES_TO_TYPES = {
        'looking_for_driver': LookingForDriverState
    }

    def create_from_name(self, state_name: str):
        return self.NAMES_TO_TYPES[state_name]()
