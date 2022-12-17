class ResponseHelper:
    def __init__(self):
        self.success: bool = True
        self.message: str = 'Success'
        self.datas: list = []
        self.status = 200

    def set_to_failed(self, message: str, status: int):
        self.success = False
        self.message = message
        self.status = status
        del self.datas

    def set_data(self, data):
        self.datas = data

    def remove_datas(self):
        del self.datas

    def get_response(self):
        return self.__dict__, self.status
