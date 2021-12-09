import pymongo
from pymongo import MongoClient


client = pymongo.MongoClient('mongodb://localhost:27017')
db_test = client["todo_application"]
collection_test = db_test["todos_app"]

db = client['Schedules']
collection = db['students']
collection_students = db['users']
# second collection same db
collection_name = db["advising_form"]

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['Advising']
collection = db['Schedules']
