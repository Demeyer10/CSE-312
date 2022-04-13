import json
import sys
import hashlib
import base64
import random


from frame_engine import unmask_data, decode_data, bit_frame, decode_frame_packet, build_frame_packet
from buffer_engine import buffer
from router import Route
import database as db
from responose import generate_websocket_response




def add_paths(router):
    router.add_route(Route("GET", "/websocket", upgrade_websocket))


def upgrade_websocket(request, handler):
    websocket_key = compute_websocket_key(request.headers['Sec-WebSocket-Key'])
    response = generate_websocket_response(websocket_key)
    handler.request.sendall(response)
    username = "User" + str(random.randint(0, 1000))
    handler.websocket_connection[handler] = username
    run_connection(request, handler)

def run_connection(request, handler):
    while True:
        received_data = handler.request.recv(1024)
        print(received_data)
        if received_data != b'':
            sys.stdout.flush()
            sys.stderr.flush()
            frame = bit_frame(list(received_data))
            packet = decode_frame_packet(frame)
            if packet["OPCODE"] == '1000':
                handler.websocket_connection.pop(handler)
                break
            received_data += buffer(int(packet["PAYLEN"])-int(len(packet["DATA"])/8), handler)
            frame = bit_frame(list(received_data))
            packet = decode_frame_packet(frame)
            if int(packet["MASK"]) == 1:
                packet["DATA"] = unmask_data(packet["DATA"], packet["MASKVALUE"])
                packet["DATA"] = decode_data(packet["DATA"])
            else:
                packet["DATA"] = decode_data(packet["DATA"])
            for users in handler.websocket_connection.keys():
                users.request.sendall(build_frame_packet(packet, handler))

def compute_websocket_key(key):
    key += "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    result = hashlib.sha1(key.encode())
    result = base64.b64encode(result.digest())
    return result





