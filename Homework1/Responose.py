def generate_response(body: bytes, content_type: str = "text/plain; charset=utf-8", response_code: str = '200 OK', cookieIDs = [], cookieValues = []):
    response = b'HTTP/1.1 ' + response_code.encode()
    if len(cookieIDs):
        for idx in range(len(cookieIDs)):
            response += b'\r\nSet-Cookie: ' + cookieIDs[idx].encode() + b"=" + str(cookieValues[idx]).encode() + b"; Max-Age=3600; HttpOnly" 
    response += b'\r\nContent-Length: ' + str(len(body)).encode()
    response += b'\r\nContent-Type: ' + content_type.encode()
    response += b'\r\nX-Content-Type-Options: nosniff'
    response += b'\r\n\r\n'
    response += body
    return response

def generate_websocket_response(websocket_key: bytes):
    response = b'HTTP/1.1 101 Switching Protocols'
    response += b'\r\nUpgrade: websocket'
    response += b'\r\nConnection: Upgrade'
    response += b'\r\nSec-WebSocket-Accept: ' + websocket_key
    response += b'\r\n\r\n'
    return response

def generate_response_redirect(cookieIDs = [], cookieValues = [],response_code: str = "301 Redirect",location: str="/"):
    response = b'HTTP/1.1 ' + response_code.encode()
    if len(cookieIDs):
        for idx in range(len(cookieIDs)):
            response += b'\r\nSet-Cookie: ' + cookieIDs[idx].encode() + b"=" + str(cookieValues[idx]).encode() + b"; Max-Age=3600; HttpOnly"
    response += b'\r\nContent-Length: 0'
    response += b"\r\nLocation: " + location.encode()
    response += b'\r\n\r\n'
    return response
