        
from pymongo import MongoClient 


mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
user_collection = db["users"] 
user_collection_id = db["user_id"]
image_collection_id = db["image_id"]
chat_collection = db["chat"]


def get_new_id():
        id_object = user_collection_id.find_one({})
        if id_object:
                next_id = int(id_object['last_id']) + 1
                user_collection_id.update_one({},{'$set': {'last_id': next_id}})
                return next_id
        else:
                user_collection_id.insert_one({'last_id': 1})
                return 1

def get_new_image_id():
        id_object = image_collection_id.find_one({})
        if id_object:
                next_id = int(id_object['last_id']) + 1
                image_collection_id.update_one({},{'$set': {'last_id': next_id}})
                return next_id
        else:
                image_collection_id.insert_one({'last_id': 1})
                return 1

def create(body):
        user = user_collection.insert_one(body)

def all_users():
        users_list = user_collection.find({}, {"_id": 0})
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

def save_upload(image, comment):
        chat = chat_collection.insert_one({'message': comment.decode(), "image_file": image})

def get_chat():
        chat_list = chat_collection.find({}, {"_id": 0})
        return list(chat_list)


