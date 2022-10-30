class TripState:
    pass


class LookingForDriver(TripState):
    pass


class AcceptedByDriver(TripState):
    pass


class DriverWaiting(TripState):
    pass


class Ongoing(TripState):
    pass


class Finished(TripState):
    pass
