import socketserver
import sys
import random
import os



from buffer_engine import buffer
from router import Router
from request import Request
from static_paths import add_paths
from user_path import add_paths as path_user
from websocket_paths import add_paths as websocket_path


class MyTCPHandler(socketserver.BaseRequestHandler):

    websocket_connection = {}

    
    def __init__(self, request, client_address, server):
        self.router = Router()
        add_paths(self.router)
        path_user(self.router)
        websocket_path(self.router)
        super().__init__(request, client_address, server)

    def handle(self):
            received_data = self.request.recv(1024)
            request = Request(received_data)
            if "Content-Length" in request.headers:
                received_data += buffer(int(request.headers["Content-Length"])-len(request.body), self)
            sys.stdout.flush()
            sys.stderr.flush()
            #print(received_data.decode())
            request = Request(received_data)
            self.router.handle_request(request, self)
    
        
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080
    server = socketserver.ThreadingTCPServer((HOST,PORT), MyTCPHandler)
    server.serve_forever()
