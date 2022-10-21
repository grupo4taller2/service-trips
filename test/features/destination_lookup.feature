Feature: Destination lookup by name
    Scenario: IV2.1 Búsqueda con resultados
        When Realizo una búsqueda con dirección "Av. Paseo Colón 850, Buenos Aires"
        Then El resultado es una ubicación válida
            And la latitud es aproximadamente -34.6174635
            And la longitud es aproximadamente -58.369979

    Scenario: IV2.2 Búsqueda sin resultados
        When Realizo una búsqueda con dirección "a9fg78aurg90au"
        Then El resultado es una ubicación inválida
            And se indica como mensaje de error "Ubicación no encontrada"
