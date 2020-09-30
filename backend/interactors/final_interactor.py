from backend.interactors.result import Result
from backend.interactors.siu_interactor import SIUInteractor
from backend.models import FinalExam, Final


class FinalInteractor:
    def close(self, final):
        final_exams = FinalExam.objects.filter(final=final, grade__isnull=True)
        if len(final_exams) > 0:
            return Result(errors=[fe.id for fe in final_exams])
        final.update(status=Final.Status.PENDING_ACT)
        # Trigger notifications and such
        return Result()

    def create_act(self, final):
        result = SIUInteractor().create_act(final)
        if result.errors:
            return result
        final.update(status=Final.Status.ACT_SENT)
