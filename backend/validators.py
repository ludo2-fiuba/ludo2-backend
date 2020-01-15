# custom validators

from django.core.exceptions import ValidationError
from stdnum.ar import dni
from stdnum.exceptions import InvalidFormat, InvalidLength


def validate_dni(value):
    try:
        dni.validate(value)
    except (InvalidFormat, InvalidLength):
        raise ValidationError(f"{value} is not a valid DNI")
