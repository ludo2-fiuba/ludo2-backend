from django.db import transaction, IntegrityError

from backend.api_exceptions import InvalidDataError
from backend.models import Final
from backend.services.siu_service import SiuService


class FinalService:
    def grade(self, final, grades): # TODO fix validation of grade
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
        final.status = Final.Status.PENDING_ACT
        final.save()

    def send_act(self, final):
        response = SiuService().create_final_act(final)
        final.act = response['id']
        final.status = Final.Status.ACT_SENT
        final.save()
        # Trigger notifications and such
