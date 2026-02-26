"""
Módulo de Validaciones
======================

Este módulo proporciona lógica para la validación de datos de entrada mediante 
expresiones regulares y reglas de negocio, asegurando que la información sea
consistente antes de ser procesada por el controlador o guardada en la base de datos.
"""

import re
from datetime import datetime

class ValidationError(Exception):
    """ Excepción personalizada para errores de validación en la interfaz. """
    pass

class Validations:
    """
    Contiene métodos estáticos y de instancia para validar campos específicos
    del formulario de música.
    """

    def validar_anio(self, anio: str):
        """
        Valida que el año de lanzamiento sea coherente.
        
        El año debe ser un número de 4 dígitos y estar comprendido entre 
        1900 y el año actual.

        Args:
            anio (str): Cadena de texto con el año a validar.

        Returns:
            int or None: El año convertido a entero si es válido, 
            None si el campo está vacío.

        Raises:
            ValidationError: Si el formato no es de 4 dígitos o está fuera de rango.
        """
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
        """
        Valida el formato del título de un disco o canción.
        
        Utiliza una expresión regular para permitir letras y separadores comunes,
        evitando caracteres especiales que puedan romper la interfaz o la lógica.

        Args:
            titulo (str): El título a validar.

        Raises:
            ValidationError: Si el título contiene caracteres no permitidos o 
            formatos inválidos (ej. empezar con un espacio).
        """
        # Explicación del patrón:
        # ^[A-Za-z]+ : Empieza con una o más letras
        # (?:[ _-][A-Za-z]+)*$ : Seguido opcionalmente por un separador y más letras
        patron = r"^[A-Za-z]+(?:[ _-][A-Za-z]+)*$"

        if not re.match(patron, titulo):
            raise ValidationError(
                "El título solo puede contener letras y separadores (espacio, - o _).\n"
                "Ejemplo: Dark Side, Back-In_Black"
            )