from django.db import transaction, IntegrityError

from backend.api_exceptions import InvalidDataError
from backend.models import Final
from backend.services.notification_service import NotificationService
from backend.services.siu_service import SiuService


class FinalService:
    def grade(self, final, grades): # TODO fix validation of grade
        if final.status != Final.Status.PENDING_ACT:
            raise InvalidDataError("Final is not in the correct status to grade")
        final_exams = final.final_exams.filter(id__in=[grade['final_exam_id'] for grade in grades])
        if len(final_exams) != len(grades):
            raise InvalidDataError(detail="Some final exam id is invalid")
        with transaction.atomic():
            try:
                for fe in final_exams:
                    grade = self._get_grade(fe.id, grades)
                    if not grade:
                        continue
                    fe.grade = grade
                    fe.save()
            except IntegrityError:
                raise InvalidDataError(detail="Some grade is invalid")
        SiuService().save_final_grades(final)

    def close(self, final):
        final.status = Final.Status.PENDING_ACT
        final.save()

    def send_act(self, final):
        response = SiuService().create_final_act(final)
        final.act = response['id']
        final.status = Final.Status.ACT_SENT
        final.save()
        NotificationService().notify_act(final)

    def notify_grades(self, final):
        NotificationService().notify_grade(final)

    def _get_grade(self, fe_id, grades):
        for grade in grades:
            if grade['final_exam_id'] == fe_id:
                return grade['grade']
