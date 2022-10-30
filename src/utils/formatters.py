class TimeFormatter:
    def format(self, time_in_seconds: int):
        minutes, seconds = divmod(time_in_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        result = ''
        if hours > 0:
            result += f'{hours} hr'
        if minutes > 0:
            result += f' {minutes} mins'
        return result


class DistanceFormatter:
    KM_IN_METERS = 1000
    DECIMAL_PLACES = 1

    def format(self, meters: int):
        if meters < self.KM_IN_METERS:
            return f'{meters} m'
        return f'{round(meters/self.KM_IN_METERS, self.DECIMAL_PLACES)} km'
