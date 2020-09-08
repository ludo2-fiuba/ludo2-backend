import io

from backend.interactors.result import Result
import face_recognition

from backend.services import AwsS3Service
from backend.utils import decode_image, user_image_path


class FinalRequirementsValidatorInteractor:
    def __init__(self, user, subject, b64_string):
        self.subject = subject
        self.user = user
        self.requester_b64_string = b64_string

    def validate(self):
        requester = face_recognition.load_image_file(io.BytesIO(decode_image(self.requester_b64_string)))
        requester_encoding = face_recognition.face_encodings(requester)[0]

        student = face_recognition.load_image_file(AwsS3Service().download_object(user_image_path(self.user.dni)))
        student_encoding = face_recognition.face_encodings(student)[0]

        results = face_recognition.compare_faces([requester_encoding], student_encoding)

        return Result(data='ok') if results[0] else Result(errors='Faces do not match')
