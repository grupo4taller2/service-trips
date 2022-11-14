from prometheus_client import Counter, generate_latest
import random


def generate_random_price():
    return random.random()


def generate_random_distance():
    return random.randint(50, 500)


GENERATORS = {
    'cotizacion': generate_random_price,
    'finalizacion': generate_random_distance
}


class FiuberMetrics:
    SOME_COUNTER = Counter(
        'my_counter',
        'First counter demo',
        ['metrica']
    )

    @classmethod
    def record(cls):
        metricas = ['cotizacion', 'finalizacion']
        metrica = random.choice(metricas)
        # valor = GENERATORS[metrica]()
        cls.SOME_COUNTER.labels(metrica).inc()

    @classmethod
    def latest(cls):
        return generate_latest()
