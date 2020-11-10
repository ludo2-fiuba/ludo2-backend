from backend.services.result import Result
from backend.services.siu_service import SiuService
from backend.models import FinalExam, Final


class FinalService:
    def close(self, final):
        final_exams = FinalExam.objects.filter(final=final, grade__isnull=True)
        if len(final_exams) > 0:
            return Result(errors=[fe.id for fe in final_exams])
        final.status = Final.Status.PENDING_ACT
        final.save()
        # Trigger notifications and such
        return Result(data=final)

    def send_act(self, final):
        SiuService().create_final_act(final)
        final.status = Final.Status.ACT_SENT
        final.save()
        return Result(data=final)
