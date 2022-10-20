Feature: HealthCheck

    Scenario: Do health check
        Given The app has started
        When Do a health check
        Then The response includes "UP"
