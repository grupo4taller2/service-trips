# flake8: noqa
from src.no_sql_database.no_sql_db import token_collection

from exponent_server_sdk import (
    PushClient,
    PushMessage,
)


def sendNotificationRider(rider_username,driver_username):
    print("SEND NOTIFICATION RIDER")
    token_bdd = token_collection.find_one({"username":rider_username})
    if(token_bdd is None):
        print("NO TOKEN")
        return
    print(rider_username)
    print(token_bdd)
    print(token_bdd["token"])
    token = token_bdd["token"]
    body_msg = f"{driver_username} will be your driver for your latest trip"
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        title=rider_username,
                        body=body_msg,
                        data=None))
    except Exception as e:
        print("ERROR")