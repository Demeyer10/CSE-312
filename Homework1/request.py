class Request:

    def __init__(self, data):
        self.parsed_data = (data.decode()).split('\r\n')
        self.parse_method_path = self.parsed_data[0].split(' ')
        
        self.method = self.parse_method_path[0]
        self.path = self.parse_method_path[1]
        self.body = self.parsed_data[10]
        