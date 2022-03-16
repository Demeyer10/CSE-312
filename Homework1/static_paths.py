import json
import os
import database as db
from responose import generate_response
from router import Route
from template_engine import render_template

def add_paths(router):
    # All allowed static paths (All other paths go to a 404 Error)
    router.add_route(Route("GET", "/hello", hello))
    router.add_route(Route("GET", "/hi", hi))
    router.add_route(Route("GET", "/functions.js", js))
    router.add_route(Route("GET", "/style.css", style))
    router.add_route(Route("GET", "/image/.", images))
    router.add_route(Route("GET", "/$", home))
    router.add_route(Route("POST", "/image-upload", upload))
   
message = [{"message": "", "image_file": ""}]
base_content = {"loop_data": message}

# Generate response based on the request
def home(request, handler):
    chat_list = db.get_chat()
    if len(chat_list):
        upload_data = {"loop_data": chat_list}
        content = render_template("sample_page/index.html", upload_data)
    else:
        content = render_template("sample_page/index.html", base_content)
    response = generate_response(content.encode(), "text/html; charset=utf-8", "200 OK")
    handler.request.sendall(response)

def hello(request, handler):
    response = generate_response('Hello World'.encode())
    handler.request.sendall(response)

def hi(request, handler):
    handler.request.sendall('HTTP/1.1 301 OK\r\nContent-Length: 0\r\nLocation: /hello\r\n'.encode())

def style(request, handler):
    send_response('sample_page/style.css', 'text/css; charset=utf-8', request, handler)

def js(request, handler):
    send_response('sample_page/functions.js', 'text/js; charset=utf-8', request, handler)

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
    if request.upload != b'':
        image_id = db.get_new_image_id()
        image_file_name = "image" + str(image_id) + ".jpg"
        image_file = open("./sample_page/image/" + image_file_name, "wb")
        image_file.write(request.upload)
        image_file.close()
    db.save_upload(image_file_name, request.comment)
    handler.request.sendall('HTTP/1.1 301 OK\r\nContent-Length: 0\r\nLocation: /\r\n'.encode())



# Creating Responses
def send_response(filename, mime_type, request, handler):
    with open(filename, 'rb') as content:
        body = content.read()
        response = generate_response(body, mime_type, '200 OK')
        handler.request.sendall(response)
