import io

import face_recognition
import numpy as np
from PIL import UnidentifiedImageError

from backend.interactors.result import Result
from backend.utils import decode_image


class ImageValidatorInteractor:
    def __init__(self, b64_string):
        self.b64_string = b64_string

    def validate_identity(self, user):
        format_result = self.validate_image()

        if format_result.errors:
            return format_result

        result = face_recognition.compare_faces([self.face_encodings[0]], np.array(user.face_encodings))

        return Result(data=result[0])

    def validate_image(self):
        try:
            self._validate_encoding()
            self._resize_image()
            self._detect_face()
        except InvalidImageError as e:
            return Result(errors=str(e))
        return Result(data=self.face_encodings[0].tolist())

    def _validate_encoding(self):
        try:
            self.encoded_image = io.BytesIO(decode_image(self.b64_string))
        except UnidentifiedImageError:
            raise InvalidImageError("Invalid base64 string, not an image")

    def _resize_image(self):
        # self.image = Image.open(self.encoded_image)
        # self.image.thumbnail((500, 500))
        # self.resized_image = io.BytesIO(self.image.tobytes())
        self.resized_image = self.encoded_image

    def _detect_face(self):
        loaded_image = face_recognition.load_image_file(self.resized_image)
        self.face_encodings = face_recognition.face_encodings(loaded_image)
        if len(self.face_encodings) == 0:
            raise InvalidImageError("Invalid image, could not detect face")


class InvalidImageError(Exception):
    pass
