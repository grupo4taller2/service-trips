# flake8: noqa
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from src.database.requested_trip_dto import RequestedTripDTO
from src.database.taken_trip_dto import TakenTripDTO

from src.repositories.base_repository import BaseRepository
from src.domain.trips.trip import Trip
from src.domain.trips.trip_state import TripFacade
from src.domain.rider import Rider
from src.domain.driver import Driver
from src.domain.directions import Directions
from src.domain.location import Location
from src.domain.time import Time
from src.domain.distance import Distance

from src.utils.formatters import TimeFormatter, DistanceFormatter

from src.notifications.notification_rider import sendNotificationRider


class TripMapper:
    def joined_sql_to_trip(self, sql_trip):
        dict_form = dict(sql_trip)
        requested = dict_form['RequestedTripDTO']
        taken = dict_form['TakenTripDTO']

        rider: Rider = Rider(requested.rider_username)
        origin: Location = Location(requested.origin_address,
                                    requested.origin_latitude,
                                    requested.origin_longitude)

        destination: Location = Location(requested.destination_address,
                                         requested.destination_latitude,
                                         requested.destination_longitude)

        time: Time = Time(requested.estimated_time,
                          TimeFormatter().format(requested.estimated_time))

        distance: Distance = Distance(
            requested.distance,
            DistanceFormatter().format(requested.distance))

        directions: Directions = Directions(origin,
                                            destination,
                                            time,
                                            distance)

        if requested.state == 'looking_for_driver':
            state = TripFacade().create_from_name('looking_for_driver')

        else:
            driver_location = Location('unknown',
                                       taken.driver_latitude,
                                       taken.driver_longitude)
            driver: Driver = Driver(taken.driver_username,
                                    driver_location)
            state = TripFacade().create_from_name(requested.state, driver)

        return Trip(
            id=UUID(requested.id),
            rider=rider,
            directions=directions,
            type=requested.type,
            state=state,
            estimated_price=requested.estimated_price)

    def sql_to_trip(self, sql_trip):
        rider: Rider = Rider(sql_trip.rider_username)
        origin: Location = Location(sql_trip.origin_address,
                                    sql_trip.origin_latitude,
                                    sql_trip.origin_longitude)

        destination: Location = Location(sql_trip.destination_address,
                                         sql_trip.destination_latitude,
                                         sql_trip.destination_longitude)

        time: Time = Time(sql_trip.estimated_time,
                          TimeFormatter().format(sql_trip.estimated_time))

        distance: Distance = Distance(
            sql_trip.distance,
            DistanceFormatter().format(sql_trip.distance))

        directions: Directions = Directions(origin,
                                            destination,
                                            time,
                                            distance)

        if sql_trip.state == 'looking_for_driver':
            state = TripFacade().create_from_name('looking_for_driver')

        else:
            driver_location = Location('unknown',
                                       sql_trip.driver_latitude,
                                       sql_trip.driver_longitude)
            driver: Driver = Driver(sql_trip.driver_username,
                                    driver_location)
            state = TripFacade().create_from_name(sql_trip.state, driver)

        return Trip(
            id=UUID(sql_trip.id),
            rider=rider,
            directions=directions,
            type=sql_trip.type,
            state=state,
            estimated_price=sql_trip.estimated_price)


class TripRepository(BaseRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session

    def trips_for_driver(self, username):
        q = 'COUNT(driver_username) FROM taken_trips LEFT JOIN '
        q += 'requested_trips rt on rt.id = taken_trips.id WHERE '
        q += 'taken_trips.updated_at > current_timestamp - interval '
        q += "'30 minutes' AND rt.state = 'finished_confirmed_by_driver' "
        q += f"AND taken_trips.driver_username = '{username}'"

        result = self.session.query(text(q))
        return result[0][0]

    def trips_last_minutes(self, minutes):
        q = 'SELECT driver_username, distance, rider_username, estimated_time'
        q += ', estimated_price FROM taken_trips LEFT JOIN '
        q += 'requested_trips rt on rt.id = taken_trips.id WHERE '
        q += 'taken_trips.updated_at > current_timestamp - interval '
        q += f"'{minutes} minutes'"

        result = self.session.execute(text(q))
        return result.all()

    def save(self, trip: Trip):
        trip_dto = RequestedTripDTO.from_entity(trip)
        self.session.add(trip_dto)

    def update(self, trip: Trip):
        previous_query = self.session.query(RequestedTripDTO).filter_by(id=str(trip.id)).first()
        previous_state = previous_query.state
        new_state = trip.state.name
        if(previous_state == 'looking_for_driver' and new_state == 'accepted_by_driver'):
            sendNotificationRider(previous_query.rider_username, trip.driver_username())
        state_update = {
            RequestedTripDTO.state: trip.state.name
        }

        self.session.query(RequestedTripDTO) \
            .filter_by(id=str(trip.id)) \
            .update(state_update)

        self.session.flush()

        taken_trip_dto = TakenTripDTO.from_entity(trip)
        if self.session.query(TakenTripDTO).filter_by(id=str(trip.id)).first():
            taken_trip_update = {
                TakenTripDTO.driver_username: taken_trip_dto.driver_username,
                TakenTripDTO.driver_latitude: taken_trip_dto.driver_latitude,
                TakenTripDTO.driver_longitude: taken_trip_dto.driver_longitude,
            }
            self.session.query(TakenTripDTO) \
                .filter_by(id=str(trip.id)) \
                .update(taken_trip_update)
        else:
            self.session.add(taken_trip_dto)

        self.seen.add(trip)
        return trip

    def find_by_id(self, id: str):
        trip_dto = self.session \
            .query(RequestedTripDTO, TakenTripDTO) \
            .outerjoin(TakenTripDTO, RequestedTripDTO.id == TakenTripDTO.id) \
            .filter(RequestedTripDTO.id == id) \
            .one()

        mapper = TripMapper()
        trip = mapper.joined_sql_to_trip(trip_dto)
        self.seen.add(trip)
        return trip

    def find_for_driver_state_offset_limit(self,
                                           username: str,
                                           state: str,
                                           offset: int,
                                           limit: int):

        trip_dtos = self.session.query(RequestedTripDTO) \
            .filter_by(state=state)

        trip_dtos = trip_dtos.join(TakenTripDTO,
                                   TakenTripDTO.id == RequestedTripDTO.id,
                                   isouter=True)

        trip_dtos = trip_dtos.order_by(RequestedTripDTO.created_at) \
            .limit(limit).offset(offset)
        mapper = TripMapper()

        return [mapper.sql_to_trip(t_dto) for t_dto in trip_dtos]

    def find_free_drivers(self):

        SQL_TEST = text(
            "tt.id, tt.updated_at , tt.driver_username "
            "FROM( "
            "SELECT taken_trips.driver_username AS driver_username,MAX(taken_trips.updated_at) AS updated_at "
            "FROM taken_trips "
            "GROUP BY taken_trips.driver_username) x "
            "JOIN taken_trips tt ON x.driver_username = tt.driver_username "
            "AND x.updated_at = tt.updated_at "
        )
        SQL_TEST_2 = text(
            "DISTINCT taken_trips.updated_at AS updated_at, taken_trips.driver_username AS driver_username "
            "FROM requested_trips, taken_trips "
        )
        SQL_QUERY = text(
            "DISTINCT driver_username "
            "FROM taken_trips "
            "EXCEPT "
            "SELECT DISTINCT tt.driver_username "
            "FROM requested_trips "
            "LEFT JOIN taken_trips tt on requested_trips.id = tt.id "
            "WHERE requested_trips.state IN ('accepted_by_driver', 'driver_arrived', 'start_confirmed_by_driver') "
            )
        result = self.session.query(SQL_TEST).all()
        result_2 = self.session.query(SQL_TEST_2).all()
        print("RESULT 2")
        print(result_2)
        print("RESULT")
        print(result)
        list_aux = []
        for row in result:
            list_aux.append(row[0])
        print(list_aux)
        if(len(list_aux) != 0):
            if(len(list_aux) == 1):
                tuple_aux = "('" + list_aux[0] + "')"
            else:
                tuple_aux = str(tuple(list_aux))
            print(tuple_aux)
            SQL_ORDER = text(
                "tt.driver_username "
                "FROM requested_trips "
                "LEFT JOIN taken_trips tt on requested_trips.id = tt.id "
                f"WHERE requested_trips.id IN {tuple_aux} "
                "AND requested_trips.state IN ('finished_confirmed_by_driver') "
                "ORDER BY requested_trips.updated_at DESC "
                "LIMIT 4"
            )
            old_order = self.session.query(SQL_ORDER).all()
        else:
            old_order = []
        SQL_NEW_DRIVERS = text(
            "drivers.username "
            "FROM drivers "
            "EXCEPT "
            "SELECT DISTINCT taken_trips.driver_username "
            "FROM requested_trips, taken_trips "
        )
        new_drivers = self.session.query(SQL_NEW_DRIVERS).all()
        list_new_drivers = []
        for row in new_drivers:
            list_new_drivers.append(row[0])
        if(len(list_new_drivers) != 0):
            if(len(list_new_drivers) == 1):
                tuple_new_drivers = "('" + list_new_drivers[0] + "')"
            else:
                tuple_new_drivers = str(tuple(list_new_drivers))
            SQL_NEW_DRIVERS_ORDER = text(
                "username "
                "FROM drivers "
                f"WHERE username IN {tuple_new_drivers} "
                "ORDER BY created_at DESC "
                "LIMIT 2"
            )
            final_new_drivers = self.session.query(SQL_NEW_DRIVERS_ORDER).all()
        else:
            final_new_drivers = []
        print("NEW DRIVERS ORDER")
        print(final_new_drivers)
        print("\n")
        print("OLD ORDER")
        print(old_order)
        final_drivers = []
        for row in old_order:
            final_drivers.append(row[0])
        print("TERMINE")
        for row in final_new_drivers:
            final_drivers.append(row[0])
        print("RESULTADO FINAL")
        print(final_drivers)
        return final_drivers
