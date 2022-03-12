class Request:
    new_line = b'\r\n'
    boundary_line = b'\r\n\r\n'

    def __init__(self, request: bytes):
        [request_line, header_as_bytes, self.body] = split_request(request)
        [self.method, self.path, self.http] = parse_request_line(request_line)
        self.headers = parse_headers(header_as_bytes)
        if "Content-Type" in self.headers:
            self.boundary = parse_boundary(self.headers)
            [self.comment, self.upload] = parse_additional_content(self.boundary, self.body)

def split_request(request: bytes):
    new_line_boundary = request.find(Request.new_line)
    boundary_line = request.find(Request.boundary_line)

    request_line =  request[:new_line_boundary]
    header_as_bytes = request[(new_line_boundary + len(Request.new_line)):boundary_line]
    body = request[(boundary_line + len(Request.boundary_line)):]

    return [request_line, header_as_bytes, body]

def parse_request_line(request_line: bytes):
    return request_line.decode().split(" ")

def parse_headers(headers_raw: bytes):
    headers = {}
    lines_as_str = headers_raw.decode().split(Request.new_line.decode())
    for line in lines_as_str:
        splits = line.split(":")
        headers[splits[0].strip()] = splits[1].strip()
    return headers

def parse_boundary(headers):
    content_type = headers["Content-Type"]
    boundary = content_type.split('boundary=')[1]
    boundary = "--" + boundary
    return boundary.encode()

def parse_additional_content(boundary: bytes, body: bytes):
    content = body.split(boundary)
    comment = b''
    upload = b''
    for i in range(1,len(content)-1):
        [request_line, headers, content_body] = split_request(content[i])
        headers = parse_headers(headers)
        if headers["Content-Disposition"].split(';')[1].split("=")[1] == '"comment"':
            comment = content_body
        elif headers["Content-Disposition"].split(';')[1].split("=")[1] == '"upload"':
            upload = content_body
    return [comment[:-2:], upload[:-2:]]
