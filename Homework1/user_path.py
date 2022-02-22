from curses.ascii import isdigit
import json
import sys


from responose import generate_response
from router import Route, Error
import database as db

def add_paths(router):
    router.add_route(Route("POST", "/user", create_user))
    router.add_route(Route("GET", "/user$", all_users))
    router.add_route(Route("GET", "/user/[0-9]+$", retrieve_user))
    router.add_route(Route("PUT", "/user/[0-9]+$", update_user))
    router.add_route(Route("DELETE", "/user/[0-9]+$", delete_user))


def create_user(request, handler):
    body_dic = json.loads(request.body)
    body_dic['id'] = db.get_new_id()
    response = generate_response(json.dumps(body_dic).encode(), "application/json", "201 CREATED")
    handler.request.sendall(response)
    db.create(body_dic)

def all_users(request, handler):
    user_list = db.all_users()
    response = generate_response(str(user_list).encode(), "text/plain", "201 OK")
    handler.request.sendall(response)


def retrieve_user(request, handler):
    path = request.path.split("/")
    user = db.get_user(int(path[2]))
    if len(user):
        response = generate_response(json.dumps(user[0]).encode(), "application/json", "200 OK")
        handler.request.sendall(response)
    else:
        Error(request, handler, "404\nUser Not Found")

def update_user(request, handler):
    path = request.path.split("/")
    user = db.get_user(int(path[2]))
    if not len(user):
        Error(request, handler, "404\nUser Not Found")
        return
    db.update_user(int(path[2]),json.loads(request.body))
    user = db.get_user(int(path[2]))
    response = generate_response(json.dumps(user[0]).encode(), "application/json", "200 OK")
    handler.request.sendall(response)


def delete_user(request, handler):
    print("In progress")
