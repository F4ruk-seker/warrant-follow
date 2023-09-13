class TaskBase:
    def __init__(self):
        self.__errors = []

    @property
    def has_error(self):
        return len(self.__errors) > 0

    @property
    def get_errors(self) -> list:
        return self.__errors

    def do(self):
        ...
