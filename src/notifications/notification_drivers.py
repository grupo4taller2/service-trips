# flake8: noqa
from src.domain import commands
from src.service_layer import messagebus
from src.repositories.unit_of_work import UnitOfWork

from src.no_sql_database.no_sql_db import token_collection

from exponent_server_sdk import (
    PushClient,
    PushMessage,
)


def sendNotification(username):
    token_bdd = token_collection.find_one({"username": username})
    if(token_bdd is None):
        print("NO TOKEN")
        return
    print(username)
    print(token_bdd)
    print(token_bdd["token"])
    token = token_bdd["token"]
    body_msg = "New Trip Available"
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        title= username,
                        body=body_msg,
                        data=None))
    except Exception as e:
        print("ERROR")


def getFreeDrivers():
    cmd = commands.GetFreeDriversCommand(
        cantidad=10
    )
    uow = UnitOfWork()
    lista_free_drivers = messagebus.handle(cmd, uow)[0]
    return lista_free_drivers


def sendNotificationDrivers():
    free_drivers = getFreeDrivers()
    print("Free Drivers")
    print(free_drivers)
    for driver in free_drivers:
        sendNotification(driver)
    print("FINISHED")
    