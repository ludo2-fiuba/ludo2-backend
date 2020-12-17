from django.db import transaction, IntegrityError

from backend.api_exceptions import InvalidDataError
from backend.models import FinalExam, Final
from backend.services.result import Result
from backend.services.siu_service import SiuService


class FinalService:
    def grade(self, final, grades):
        if final.status != Final.Status.PENDING_ACT:
            raise InvalidDataError("Final is not in the correct status to grade")
        final_exams = final.final_exams.filter(id__in=grades.keys())
        if len(final_exams) != len(grades):
            raise InvalidDataError(detail="Some final exam id is invalid")
        with transaction.atomic():
            try:
                for fe in final_exams:
                    fe.grade = grades[str(fe.id)]
                    fe.save()
            except IntegrityError:
                raise InvalidDataError(detail="Some grade is invalid")

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
