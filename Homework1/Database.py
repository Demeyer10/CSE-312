        
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
        body.pop('_id')

def all_users():
        users_list = user_collection.find({} ,{"_id": 0})
        return list(users_list)

def get_user(id):
        user = user_collection.find({"id": id}, {"_id": 0})
        return list(user)

def update_user(id, body):
        user_collection.update_one({"id": id},{'$set': {'email': body['email'], 'username': body['username']}})

def delete_user(id):
        user_collection.delete_one({"id": id})

def check_database(id):
        user = get_user(id)
        if not len(user):
                return True
        else:
                return False