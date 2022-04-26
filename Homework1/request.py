

class Request:
    new_line = b'\r\n'
    boundary_line = b'\r\n\r\n'

    def __init__(self, request: bytes):
        [request_line, header_as_bytes, self.body] = split_request(request)
        [self.method, self.path, self.http] = parse_request_line(request_line)
        self.headers = parse_headers(header_as_bytes)
        self.cookies = {}
        if "Cookie" in self.headers:
            self.cookies = parse_cookies(self.headers)
        if "Content-Type" in self.headers:
            self.boundary = parse_boundary(self.headers)
            [self.username, self.password] = parse_login_information(self.boundary, self.body)
            [self.comment, self.upload, self.token] = parse_additional_content(self.boundary, self.body)

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
    token = b''
    for i in range(1,len(content)-1):
        [request_line, headers, content_body] = split_request(content[i])
        headers = parse_headers(headers)
        if headers["Content-Disposition"].split(';')[1].split("=")[1] == '"comment"':
            comment = content_body
            comment = comment.replace(b'&', b'&amp;')
            comment = comment.replace(b'>', b'&gt;')
            comment = comment.replace(b'<', b'&lt;')
        elif headers["Content-Disposition"].split(';')[1].split("=")[1] == '"upload"':
            upload = content_body
        elif headers["Content-Disposition"].split(';')[1].split("=")[1] == '"token"':
            token = content_body
    return [comment[:-2:], upload[:-2:], token[:-2:]]


def parse_login_information(boundary: bytes, body: bytes):
    content = body.split(boundary)
    username = b''
    password = b''
    for i in range(1,len(content)-1):
        [request_line, headers, content_body] = split_request(content[i])
        headers = parse_headers(headers)
        if headers["Content-Disposition"].split(';')[1].split("=")[1] == '"username"':
            username = content_body
        elif headers["Content-Disposition"].split(';')[1].split("=")[1] == '"password"':
            password = content_body
    return [username[:-2:],password[:-2:]]


def parse_cookies(header):
    cookies = header["Cookie"].split(";")
    cookie_dic = {}
    for cookie in cookies:
        cookie = cookie.split("=")
        cookie[0] = cookie[0].strip(" ")
        cookie_dic[cookie[0]] = cookie[1]
    return cookie_dic