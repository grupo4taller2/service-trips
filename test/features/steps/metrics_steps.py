# flake8: noqa

from behave import when, then, given
from src.conf.config import Settings
from fastapi.testclient import TestClient


def trip_request_data():
    return {
        "rider_username": "lazaro",
        "rider_origin_address": "Av. Paseo Colón 850, Buenos Aires",
        "rider_destination_address": "Gral. Las Heras 2214, Buenos Aires",
        "trip_type": "regular"
    }

def driver_patch_data(chofer, state):
    return {
        "driver_username": f'{chofer}',
        "driver_current_latitude": -34.6174679,
        "driver_current_longitude": -58.36779,
        "trip_state": f'{state}'
    }


def states():
    return ['accepted_by_driver',
        'driver_arrived',
        'start_confirmed_by_driver',
        'finished_confirmed_by_driver']


@given(u'Existen {:d} viajes finalizados en los ultimos {:d} minutos para el chofer "{chofer}"')
def step_realizar_viajes(context, viajes, minutos, chofer):
    client: TestClient = context.client
    for i in range(viajes):
        trip_data = trip_request_data()
        response = client.post(
            url=f'{Settings().API_V1_STR}/trips',
            json=trip_data
        )
        assert response.status_code == 201
        trip_id = response.json()['id']
        for state in states():            
            response = client.patch(
                url=f'{Settings().API_V1_STR}/trips/{trip_id}',
                json=driver_patch_data(chofer, state)
            )
            assert response.status_code == 202


@when(u'Obtengo la cantidad de viajes en los ultimos {:d} minutos para el chofer "{chofer}"')
def step_obtener_viajes(context, minutos, chofer):
    client: TestClient = context.client
    response = client.get(
        url=f'{Settings().API_V1_STR}/metrics/{chofer}',
    )
    context.viajes = response.json()
    assert response.status_code == 200


@then(u'El resultado son {:d} viajes')
def step_n_viajes(context, viajes):
    print(context.viajes)
    assert context.viajes['finished_trips'] == 2
