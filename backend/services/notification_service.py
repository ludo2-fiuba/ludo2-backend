from push_notifications.models import GCMDevice


class NotificationService:
    def notify_date_approved(self, final):
        device = GCMDevice.objects.filter(user=final.teacher.user).last()
        if device:
            device.send_message(
                f"La fecha de final de {final.subject_name} para el día {final.date.date()} fue aprobada")

    def notify_final_grade(self, final):
        self.notify_devices(final.final_exams.filter(grade__isnull=False), f"El docente ya subió tu nota para tu final de {final.subject_name} del día {final.date.date()}")

    def notify_evaluation_date(self, evaluation):
        self.notify_student_devices(evaluation.semester.students, f"El la fecha de {evaluation} ha sido cambiada")

    def notify_evaluation_grade(self, evaluation):
        self.notify_devices(evaluation.submissions.filter(grade__isnull=False), f"El docente de {evaluation.semester.commission.subject_name} ya subió tu nota de {evaluation.evaluation_name}")

    def notify_act(self, final):
        self.notify_devices(final.final_exams.all(), f"Ya está cargada en el SIU el acta con tu nota de {final.subject_name} del día {final.date.date()}")

    def notify_devices(self, final_exams, message):
        for fe in final_exams:
            devices = GCMDevice.objects.filter(user=fe.student.user, active=True)
            for device in devices:
                device.send_message(message)

    def notify_student_devices(self, students, message):
        for student in students:
            devices = GCMDevice.objects.filter(user=student.user, active=True)
            for device in devices:
                device.send_message(message)
