from backend.interactors.result import Result


class CourseRefresherInteractor:
    def __init__(self, teacher):
        self.teacher = teacher

    def refresh(self):
        return Result(data='ok')
