from pymongo import MongoClient

MONGO_URI = "mongodb+srv://root_IA:GerardoPT@cluster0.zzb8tuy.mongodb.net/"

client = MongoClient(MONGO_URI)

db = client["db_parking"]

vehicles_collection = db["vehicles"]
users_collection = db["users"]