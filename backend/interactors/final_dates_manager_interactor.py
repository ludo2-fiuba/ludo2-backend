from backend.interactors.result import Result


class FinalDatesManagerInteractor:
    def __init__(self, course):
        self.course = course

    def set(self):
        return Result(data='ok')

    def list(self):
        return Result(data='ok')
