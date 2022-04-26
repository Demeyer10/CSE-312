import json
import os
import secrets
import bcrypt
import database as db
from responose import generate_response, generate_response_redirect
from router import Route
from template_engine import render_template, replace_placeholder


def add_paths(router):
    # All allowed static paths (All other paths go to a 404 Error)
    router.add_route(Route("GET", "/hello", hello))
    router.add_route(Route("GET", "/hi", hi))
    router.add_route(Route("GET", "/functions.js", js))
    router.add_route(Route("GET", "/style.css", style))
    router.add_route(Route("GET", "/image/.", images))
    router.add_route(Route("GET", "/$", home))
    router.add_route(Route("GET", "/login$", loginHome))
    router.add_route(Route("GET", "/login.css", loginStyle))
    router.add_route(Route("GET", "/signup$", signupHome))
    router.add_route(Route("GET", "/Signup.css", signUpStyle))
    router.add_route(Route("POST", '/register', register))
    router.add_route(Route("POST", '/login', login))
    router.add_route(Route("POST", "/image-upload", upload))
   
message = [{"message": "", "image_file": ""}]
base_content = {"loop_data": message}
tokens = []

# Generate response based on the request
def home(request, handler):
    chat_list = db.get_chat()
    if not 'username' in request.cookies:
         handler.request.sendall('HTTP/1.1 301 OK\r\nContent-Length: 0\r\nLocation: /login\r\n'.encode())
    login_token = request.cookies["token"]
    db_token = db.get_token_by_username(request.cookies["username"])[0]
    if not bcrypt.checkpw(login_token.encode('utf-8'), db_token[request.cookies['username']].encode("utf-8")):
        handler.request.sendall('HTTP/1.1 301 OK\r\nContent-Length: 0\r\nLocation: /login\r\n'.encode())
    if len(chat_list):
        upload_data = {"loop_data": chat_list}
        content = render_template("sample_page/index.html", upload_data)
        content = content.replace("{{username}}", request.cookies["username"])
        token = secrets.token_urlsafe(20)
        tokens.append(token.encode())
        content = content.replace("{{token}}", token)
    else:
        token = secrets.token_urlsafe(20)
        tokens.append(token.encode())
        content = render_template("sample_page/index.html", base_content)
        content = content.replace("{{token}}", token)
    if "visit" in request.cookies:
        content = content.replace("{{visit}}", request.cookies["visit"])
        response = generate_response(content.encode(), "text/html; charset=utf-8", "200 OK", ["visit"], [int(request.cookies["visit"])+1])
    else:
        content = content.replace("{{visit}}", "1")
        response = generate_response(content.encode(), "text/html; charset=utf-8", "200 OK", ["visit"], [2])
    handler.request.sendall(response)

def hello(request, handler):
    response = generate_response('Hello World'.encode())
    handler.request.sendall(response)

def hi(request, handler):
    handler.request.sendall('HTTP/1.1 301 OK\r\nContent-Length: 0\r\nLocation: /hello\r\n'.encode())

def style(request, handler):
    send_response('sample_page/style.css', 'text/css; charset=utf-8', request, handler)

def js(request, handler):
    send_response('sample_page/functions.js', 'text/javascript; charset=utf-8', request, handler)

def images(request, handler):
    data = request.path.split('/')
    # Search through images to find request on
    if os.path.exists("sample_page/image/" + data[2]):
        send_response('sample_page/image/' + data[2], 'image/jpeg', request, handler)
        return
    # Image request not found 404 Error
    response = generate_response('404\nCannot Find Page'.encode(),'text/plain; charset=utf-8','404 Error')
    handler.request.sendall(response)
    
def upload(request, handler):
    image_file_name = ""
    if request.token not in tokens:
        response = generate_response('Response Rejected'.encode(), "text/plain; charset=utf-8", "403 REJECTED")
        handler.request.sendall(response)
        return
    elif request.upload == b'' and request.comment == b'':
        handler.request.sendall('HTTP/1.1 301 OK\r\nContent-Length: 0\r\nLocation: /\r\n'.encode())
        return
    if request.upload != b'':
        image_id = db.get_new_image_id()
        image_file_name = "image" + str(image_id) + ".jpg"
        image_file = open("./sample_page/image/" + image_file_name, "wb")
        image_file.write(request.upload)
        image_file.close()
    db.save_upload(image_file_name, request.comment)
    handler.request.sendall('HTTP/1.1 301 OK\r\nContent-Length: 0\r\nLocation: /\r\n'.encode())


def loginHome(request, handler):
    send_response('sample_page/login.html', 'text/html; charset=utf-8', request, handler)

def loginStyle(request, handler):
    send_response('sample_page/login.css', 'text/css; charset=utf-8', request, handler)

def signupHome(request, handler):
    send_response('sample_page/Signup.html', 'text/html; charset=utf-8', request, handler)

def signUpStyle(request, handler):
    send_response('sample_page/Signup.css', 'text/css; charset=utf-8', request, handler)

def register(request, handler):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(request.password, salt)
    db.store_information(request.username, hashed_password)
    handler.request.sendall('HTTP/1.1 301 OK\r\nContent-Length: 0\r\nLocation: /\r\n'.encode())

def login(request, handler):
    user = db.get_information_by_username(request.username)[0]
    if user:
        hashed_password = user[request.username.decode()]
        password = request.password.decode().encode("utf-8")
        if bcrypt.checkpw(password, hashed_password):
            print("matched")
            token = secrets.token_urlsafe(20)
            response = generate_response_redirect(["token","username"], [token,request.username.decode()])
            salt = bcrypt.gensalt()
            token = bcrypt.hashpw(token.encode("utf-8"), salt)
            db.store_token(request.username.decode(), token)
            handler.request.sendall(response)
        else:
            print("no match") 
    else:
        print("user not found")

# Creating Responses
def send_response(filename, mime_type, request, handler):
    with open(filename, 'rb') as content:
        body = content.read()
        response = generate_response(body, mime_type, '200 OK')
        handler.request.sendall(response)
