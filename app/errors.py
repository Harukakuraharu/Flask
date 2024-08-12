

class HttpError(Exception):

    def __init__(self, status_code: int, error_message: str | dict):
        self.status_code = status_code
        self.error_message = error_message


        