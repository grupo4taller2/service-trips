from firebase_admin import  messaging
from src.notifications.firebase_init import firebase_app
from src.no_sql_database.no_sql_db import driver_collection

def sendNotification(username):
    # This registration token comes from the client FCM SDKs.
    registration_token = 'YOUR_REGISTRATION_TOKEN'
    user = driver_collection.find_one({"driver_username": "franco" })
    print(user)
    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

