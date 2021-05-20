from django.db import transaction, IntegrityError
from push_notifications.models import GCMDevice

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
        SiuService().save_final_grades(final)

    def close(self, final):
        final.status = Final.Status.PENDING_ACT
        final.save()

    def send_act(self, final):
        response = SiuService().create_final_act(final)
        final.act = response['id']
        final.status = Final.Status.ACT_SENT
        final.save()
        self.notify_devices(final.final_exams, f"Ya está cargada en el SIU el acta con tu nota de {final.subject_name} del día {final.date.date()}")
        # Trigger notifications and such

    def notify_grades(self, final):
        self.notify_devices(final.final_exams.filter(grade__isnull=False), f"El docente ya subió tu nota para tu final de {final.subject_name} del día {final.date.date()}")

    def notify_date_approved(self, final):
        device = GCMDevice.objects.filter(user=final.teacher.user).first()
        if device:
            device.send_message(f"La fecha de final de {final.subject_name} para el día {final.date.date()} fue aprobada")

    def notify_devices(self, final_exams, message):
        for fe in final_exams:
            device = GCMDevice.objects.filter(user=fe.student.user).first()
            if device:
                device.send_message(message)
