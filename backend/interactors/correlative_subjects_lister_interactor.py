from backend.interactors.result import Result


class CorrelativeSubjectsListerInteractor:
    def __init__(self, subject):
        self.subject = subject

    def list(self):
        return Result(data='ok')

