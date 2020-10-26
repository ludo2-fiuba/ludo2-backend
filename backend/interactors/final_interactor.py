from backend.interactors.result import Result
from backend.interactors.siu_interactor import SiuInteractor
from backend.models import FinalExam, Final


class FinalInteractor:
    def close(self, final):
        final_exams = FinalExam.objects.filter(final=final, grade__isnull=True)
        if len(final_exams) > 0:
            return Result(errors=[fe.id for fe in final_exams])
        final.status = Final.Status.PENDING_ACT
        final.save()
        # Trigger notifications and such
        return Result(data=final)

    def send_act(self, final):
        SiuInteractor().create_final_act(final)
        final.status = Final.Status.ACT_SENT
        final.save()
        return Result(data=final)
