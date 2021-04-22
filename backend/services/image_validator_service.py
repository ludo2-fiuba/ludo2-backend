import io

import face_recognition
import numpy as np
from PIL import UnidentifiedImageError
from PIL import Image

from backend.api_exceptions import InvalidImageError
from backend.utils import decode_image


class ImageValidatorService:
    def __init__(self, b64_string):
        self.b64_string = b64_string

    def validate_identity(self, student):
        self.validate_image()

        return face_recognition.compare_faces([self.face_encodings[0]], np.array(student.face_encodings))[0]

    def validate_image(self):
        self._validate_encoding()
        self._resize_image()
        self._detect_face()
        return self.face_encodings[0].tolist(), self.image

    def _validate_encoding(self):
        try:
            image_bytes = io.BytesIO(decode_image(self.b64_string))
            self.encoded_image = face_recognition.load_image_file(image_bytes)
            self.image = Image.open(image_bytes)
        except UnidentifiedImageError:
            raise InvalidImageError(detail="Invalid base64 string, not an image")

    def _resize_image(self):
        # self.image = Image.open(self.encoded_image)
        # self.image.thumbnail((500, 500))
        # self.resized_image = io.BytesIO(self.image.tobytes())
        self.resized_image = self.encoded_image

    def _detect_face(self):
        self.face_encodings = face_recognition.face_encodings(self.encoded_image)
        if len(self.face_encodings) == 0:
            raise InvalidImageError(detail="Invalid image, could not detect face")
