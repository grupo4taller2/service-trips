class LocationNotFoundException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
        super().__init__(self.message)

    def __str__(self):
        return self.message if self.message else 'No encontrada'


class LocationServiceUnavailableException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
        super().__init__(self.message)

    def __str__(self):
        return self.message if self.message else 'No disponible'


class DirectionsNotFoundException(Exception):
    def __init__(self, *args):
        if args:
            self.message = f'origin: {args[0]},destination: {args[1]}'
        else:
            self.message = None
        super().__init__(self.message)

    def __str__(self):
        return self.message if self.message else 'No encontrada'


class DirectionsServiceUnavailableException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
        super().__init__(self.message)

    def __str__(self):
        return self.message if self.message else 'No disponible'
