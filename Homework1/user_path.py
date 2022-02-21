import json


from responose import generate_response
from router import Route
import database as db

def add_paths(router):
    router.add_route(Route("POST", "/user", create_user))


def create_user(request, handler):
    body_dic = request.body
    body_dic['id'] = db.get_new_id()
    response = generate_response(json.dumps(body_dic).encode(), 'application/json','201 CREATED')
    handler.request.sendall(response)
    db.create(body_dic)
    

