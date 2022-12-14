from pymongo import mongo_client
import os


client = mongo_client.MongoClient(os.environ['MONGO_CONNECTION'])


print('Connected to MongoDB...')

db = client["fastapi"]

driver_collection = db.driver_collection

rider_collection = db.rider_collection

token_collection = db.token_collection
