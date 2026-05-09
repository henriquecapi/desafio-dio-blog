class NotFoundPostError(Exception):
    def __init__(self, message: str = "Post não encontrado."):
        self.message = message


class NotFoundUserError(Exception):
    def __init__(self, message: str = "Usuário não encontrado."):
        self.message = message


class BadRequestError(Exception):
    def __init__(self, message: str):
        self.message = message


class ConflictError(Exception):
    def __init__(self, message: str):
        self.message = message
