import re
from datetime import datetime

class ValidationError(Exception):
    pass

class Validations:

    def validar_anio(self, anio: str):
        if not anio.strip():
            return None

        if not re.match(r'^\d{4}$', anio):
            raise ValidationError(
                "El campo Año debe contener exactamente 4 números.\nEjemplo: 2001"
            )

        anio_int = int(anio)
        current_year = datetime.now().year

        if not (1900 <= anio_int <= current_year):
            raise ValidationError(
                f"El año debe estar entre 1900 y {current_year}."
            )

        return anio_int

    def validar_titulo(self, titulo: str):
        patron = r"^[A-Za-z]+(?:[ _-][A-Za-z]+)*$"

        if not re.match(patron, titulo):
            raise ValidationError(
                "El título solo puede contener letras y separadores (espacio, - o _).\n"
                "Ejemplo: Dark Side, Back-In_Black"
            )
