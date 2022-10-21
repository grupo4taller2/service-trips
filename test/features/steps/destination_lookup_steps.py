from behave import when, then
from src.conf.config import Settings


@when(u'Realizo una búsqueda con dirección "{address}"')
def step_do_search(context, address):
    response = context.client.get(
        f'{Settings().API_V1_STR}/locations/search?address={address}'
    )
    context.location_search_response = response


@then(u'El resultado es una ubicación válida')
def step_check_valid_result(context):
    assert context.location_search_response.status_code == 200


@then(u'la latitud es aproximadamente {:f}')
def step_check_obtained_latitude(context, latitude):
    obtained_latitude = context.location_search_response.json()['latitude']
    assert obtained_latitude == latitude


@then(u'la longitud es aproximadamente {:f}')
def step_check_obtained_longitude(context, longitude):
    obtained_longitude = context.location_search_response.json()['longitude']
    assert obtained_longitude == longitude


@then(u'El resultado es una ubicación inválida')
def step_check_result_is_invalid(context):
    assert context.location_search_response.status_code == 404


@then(u'se indica como mensaje de error "{message}"')
def step_impl(context, message):
    assert context.location_search_response.json()['message'] == message
