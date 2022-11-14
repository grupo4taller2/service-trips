from prometheus_client import Counter, generate_latest
import random

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
    def count_trip_update(cls, state_name: str):
        metric_name = STATE_TO_METRIC[state_name]
        cls.ACCUMULATED_METRICS_COUNTER.labels(metric_name).inc()

    @classmethod
    def latest(cls):
        return generate_latest()
