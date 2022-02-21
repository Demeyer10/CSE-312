        
from pymongo import MongoClient 


mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
user_collection = db["users"] 
user_collection_id = db["user_id"]


def get_new_id():
        id_object = user_collection_id.find_one({})
        if id_object:
                next_id = int(id_object['last_id']) + 1
                user_collection_id.update_one({},{'$set': {'last_id': next_id}})
                return next_id
        else:
                user_collection_id.insert_one({'last_id': 1})
                return 1

def create(body):
        user_collection.insert_one(body)
        print(body)