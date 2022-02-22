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
        print('--Data Recieved--\n\n' + received_data.decode() + '\n\n--End of Data--')
        
        sys.stdout.flush()
        sys.stdout.flush()

        request = Request(received_data)

        self.router.handle_request(request, self)
        
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080
    server = socketserver.ThreadingTCPServer((HOST,PORT), MyTCPHandler)
    server.serve_forever()
