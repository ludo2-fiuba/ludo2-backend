class Result:
    def __init__(self, data=None, errors=[]):
        self.data = data
        self.errors = errors

    def is_successful(self):
        return self.errors is []
