from backend.interactors.result import Result


class FinalRequirementsValidatorInteractor:
    def __init__(self, subject, student):
        self.subject = subject
        self.student = student

    def validate(self):
        return Result(data='ok')

