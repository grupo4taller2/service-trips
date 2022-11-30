Feature: Metricas
    Scenario: Viajes en los últimos 30 minutos
        Given Existen 2 viajes finalizados en los ultimos 30 minutos para el chofer "mateo"
        When Obtengo la cantidad de viajes en los ultimos 30 minutos para el chofer "mateo"
        Then El resultado son 2 viajes
