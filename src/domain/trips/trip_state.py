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
