from dbm.dumb import error
import json
import sys


from responose import generate_response
from router import Route, Error
import database as db

def add_paths(router):
    router.add_route(Route("POST", "/users", create_user))
    router.add_route(Route("GET", "/users$", all_users))
    router.add_route(Route("GET", "/users/[0-9]+$", retrieve_user))
    router.add_route(Route("PUT", "/users/[0-9]+$", update_user))
    router.add_route(Route("DELETE", "/users/[0-9]+$", delete_user))
    


def create_user(request, handler):
    body_dic = json.loads(request.body)
    body_dic['id'] = db.get_new_id()
    response = generate_response(json.dumps(body_dic).encode(), "application/json", "201 CREATED")
    handler.request.sendall(response)
    db.create(body_dic)

def all_users(request, handler):
    user_list = db.all_users()
    if not len(user_list):
        Error(request, handler, "404\nNo User in Database")
        return
    response = generate_response(json.dumps(user_list).encode(), "text/plain", "200 OK")
    handler.request.sendall(response)


def retrieve_user(request, handler):
    path = request.path.split("/")
    user_id = int(path[2])
    if db.check_database(user_id):
        Error(request, handler, "404\nUser Not Found")
        return
    user = db.get_user(user_id)
    response = generate_response(json.dumps(user[0]).encode(), "application/json", "200 OK")
    handler.request.sendall(response)
        

def update_user(request, handler):
    path = request.path.split("/")
    user_id = int(path[2])
    if db.check_database(user_id):
        Error(request, handler, "404\nUser Not Found")
        return
    db.update_user(user_id,json.loads(request.body))
    user = db.get_user(user_id)
    response = generate_response(json.dumps(user[0]).encode(), "application/json", "200 OK")
    handler.request.sendall(response)


def delete_user(request, handler):
    path = request.path.split("/")
    user_id = int(path[2])
    if db.check_database(user_id):
        Error(request, handler, "404\nUser Not Found")
        return
    response = generate_response(bytes(0), "text/plain", "204 NO CONTENT")
    handler.request.sendall(response)
    db.delete_user(user_id)
    
    
