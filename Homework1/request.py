class Request:

    def __init__(self, data):
        self.parsed_data = (data.decode()).split(' ')
        self.method = self.parsed_data[0]
        self.path = self.parsed_data[1]
        