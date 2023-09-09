class ApiHostModel:
    def __init__(self, host: str, end: bool = False):
        self.__HOST: str = host
        self.end = end

    def __str__(self):
        return self.__HOST

    def __join__(self, item):
        path = "/".join([self.__HOST, item])
        return ApiHostModel(path)

    def __truediv__(self, other):
        return self.__join__(other) + ('/' if self.end else '')

    def __add__(self, other):
        return ApiHostModel(host=self.__HOST + other + ('/' if self.end else ''))

    # def __repr__(self):
    #     return self.__HOST

