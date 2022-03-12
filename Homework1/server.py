import socketserver
import sys
import os


from router import Router
from request import Request
from static_paths import add_paths
from user_path import add_paths as path_user




class MyTCPHandler(socketserver.BaseRequestHandler):

    
    def __init__(self, request, client_address, server):
        self.router = Router()
        add_paths(self.router)
        path_user(self.router)
        super().__init__(request, client_address, server)

    def handle(self):
        received_data = self.request.recv(1024)
        request = Request(received_data)
        if "Content-Length" in request.headers:
            received_data += buffer(int(request.headers["Content-Length"])-len(request.body), self)
        sys.stdout.flush()
        sys.stderr.flush()
        request = Request(received_data)
        self.router.handle_request(request, self)

def buffer(content_length, self):
    content = b''
    while len(content) != content_length:
        if content_length >= len(content)+1024:
            content += self.request.recv(1024)
        else:
            content += self.request.recv(content_length-len(content))
    return content
    
        
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8000
    server = socketserver.ThreadingTCPServer((HOST,PORT), MyTCPHandler)
    server.serve_forever()
