class ResponseHelper:
    def __init__(self):
        self.success: bool = True
        self.message: str = 'Success'
        self.data: list = []
        self.status = 200

    def set_to_failed(self, message: str, status: int):
        self.success = False
        self.message = message
        self.status = status
        del self.data

    def set_data(self, data):
        self.data = data

    def remove_data(self):
        del self.data

    def get_response(self):
        return self.__dict__, self.status
