from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://sophieanaiswrd:od0fqAPP0QhkLPhh@cluster0.mviyre7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)

db = client["kanjiApp"] # database name
users_collection = db["users"] # collection for users