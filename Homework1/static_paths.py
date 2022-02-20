import json

from Responose import generate_response
from router import Route

def add_paths(router):
    # All allowed static paths (All other paths go to a 404 Error)
    router.add_route(Route("GET", "/hello", hello))
    router.add_route(Route("GET", "/hi", hi))
    router.add_route(Route("GET", "/functions.js", js))
    router.add_route(Route("GET", "/style.css", style))
    router.add_route(Route("GET", "/image/.", images))
    router.add_route(Route("GET", "/$", home))
   
    


# Generate response based on the request
def home(request, handler):
    send_response('sample_page/index.html', 'text/html; charset=utf-8', request, handler)

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
    images = ['cat.jpg', 'dog.jpg', 'eagle.jpg', 'elephant.jpg', 'flamingo.jpg', 'kitten.jpg', 'parrot.jpg', 'rabbit.jpg']
    data = request.path.split('/')
    # Search through images to find request on
    for image in images:
        if image == data[2]:
            send_response('sample_page/image/' + image, 'image/jpeg', request, handler)
            return
    # Image request not found 404 Error
    response = generate_response('404\nCannot Find Page'.encode(),'text/plain; charset=utf-8','404 Error')
    handler.request.sendall(response)
        



# Creating Responses
def send_response(filename, mime_type, request, handler):
    with open(filename, 'rb') as content:
        body = content.read()
        response = generate_response(body, mime_type, '200 OK')
        handler.request.sendall(response)
