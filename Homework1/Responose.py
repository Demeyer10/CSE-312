def generate_response(body: bytes, content_type: str = "text/plain; charset=utf-8", response_code: str = '200 OK'):
    response = b'HTTP/1.1 ' + response_code.encode()
    response += b'\r\nContent-Length: ' + str(len(body)).encode()
    response += b'\r\nContent-Type: ' + content_type.encode()
    response += b'\r\n\r\n'
    response += body
    return response
