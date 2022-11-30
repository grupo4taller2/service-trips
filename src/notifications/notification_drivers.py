import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.domain import commands
from src.service_layer import messagebus
from src.repositories.unit_of_work import UnitOfWork

def getFreeDrivers():
    cmd = commands.GetFreeDriversCommand(
        cantidad=10
    )
    uow = UnitOfWork()
    lista_free_drivers = messagebus.handle(cmd, uow)[0]
    return lista_free_drivers


def sendNotificationDrivers():
    free_drivers = getFreeDrivers()
    print("ESTO ES EL PROBLEMA")
    print(free_drivers)
    """
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    print(os.environ["TRIPS_SERVICE_USERS_URL"])
    uri = os.environ["TRIPS_SERVICE_USERS_URL"] + "/drivers/username/all"
    response = session.get(uri)
    lista_drivers = response.json()
    print(lista_drivers)


    def find_free_drivers(self):    
 
         # from sqlalchemy.sql import text
        SQL_QUERY = text("drivers.username FROM drivers EXCEPT SELECT DISTINCT taken_trips.driver_username FROM requested_trips, taken_trips WHERE requested_trips.state IN ('accepted_by_driver', 'driver_arrived', 'start_confirmed_by_driver')")
 
        result = self.session.query(SQL_QUERY).all() 
        print([row[0] for row in result]
    """