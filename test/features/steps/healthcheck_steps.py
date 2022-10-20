from behave import given, when, then


@given(u'The app has started')
def step_app_started(context):
    pass


@when(u'Do a health check')
def step_do_health_check(context):
    context.response = context.client.get('/api/v1/healthcheck')


@then(u'The response includes "{}"')
def step_assert_message_contains(context, message_content):
    assert message_content in context.response.json()['message']
