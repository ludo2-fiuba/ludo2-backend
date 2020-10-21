from backend.interactors.result import Result
from backend.interactors.siu_interactor import SiuInteractor
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
        result = SiuInteractor().create_final_act(final)
        if not result.errors:
            final.update(status=Final.Status.ACT_SENT)
        return result
