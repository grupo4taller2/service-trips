from prometheus_client import Counter, Histogram, generate_latest
from src.domain.trips.trip import Trip


STATE_TO_METRIC = {
    'looking_for_driver': 'trip_requested',
    'accepted_by_driver': 'trip_accepted_by_driver',
    'driver_arrived': 'trip_driver_wating',
    'start_confirmed_by_driver': 'trip_ongoing',
    'finished_confirmed_by_driver': 'trip_finished'
}


class FiuberMetrics:
    ACCUMULATED_METRICS_COUNTER = Counter(
        'accumulated_counter',
        'Accumulated counter',
        ['metric']
    )
    FINISHED_TRIPS_DISTANCE_HISTOGRAM = Histogram(
        'finished_trips_distance',
        'Distance in meters for finished trips',
        buckets=[1000.0*i for i in range(1, 11)]
    )

    LocationSearched = 'location_searched'
    DirectionsSearched = 'directions_searched'
    TripRequested = 'trip_requested'
    TripAcceptedByDriver = 'trip_accepted_by_driver'
    TripOngoing = 'trip_ongoing'
    TripFinished = 'trip_finished'

    @classmethod
    def count_event(cls, metric: str):
        cls.ACCUMULATED_METRICS_COUNTER.labels(metric).inc()

    @classmethod
    def count_trip_update(cls, trip: Trip):
        trip_state_name = trip.state.name
        metric_name = STATE_TO_METRIC[trip_state_name]
        cls.ACCUMULATED_METRICS_COUNTER.labels(metric_name).inc()
        cls.trip_distance(trip)

    @classmethod
    def trip_distance(cls, trip: Trip):
        if trip.state.name != 'finished_confirmed_by_driver':
            return
        cls.FINISHED_TRIPS_DISTANCE_HISTOGRAM.observe(
            trip.distance_in_meters()
        )

    @classmethod
    def latest(cls):
        return generate_latest()
