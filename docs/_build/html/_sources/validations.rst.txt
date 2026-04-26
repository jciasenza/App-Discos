Módulo de Validaciones
=======================

.. automodule:: validations
   :members:
   :undoc-members:
   :show-inheritance:
Funciones de Validación
-----------------------

El módulo proporciona funciones para validar datos antes de operaciones CRUD.

validar_artista(data)
~~~~~~~~~~~~~~~~~~~~~

Valida los datos de un artista antes de guardarlo en la base de datos.

**Parámetros:**
- ``data`` (dict): Diccionario con los datos del artista

**Retorna:**
- ``bool``: True si los datos son válidos, False en caso contrario

**Validaciones realizadas:**

1. **Nombre requerido:**
   - No puede ser None o vacío
   - Debe ser string

2. **Nombre único:**
   - Verifica que no exista otro artista con el mismo nombre
   - Insensible a mayúsculas/minúsculas

3. **Tipo válido (opcional):**
   - Debe ser uno de: 'Solista', 'Banda', 'Dúo'
   - Si se proporciona, debe ser string

**Ejemplo de uso:**

.. code-block:: python

   from validations import validar_artista

   # Datos válidos
   data_valido = {
       'nombre': 'The Rolling Stones',
       'tipo': 'Banda',
       'info': 'Banda legendaria de rock'
   }
   es_valido = validar_artista(data_valido)  # Retorna True

   # Datos inválidos - nombre vacío
   data_invalido = {'nombre': '', 'tipo': 'Banda'}
   es_valido = validar_artista(data_invalido)  # Retorna False

validar_disco(data)
~~~~~~~~~~~~~~~~~~~

Valida los datos de un disco antes de guardarlo.

**Parámetros:**
- ``data`` (dict): Diccionario con los datos del disco

**Retorna:**
- ``bool``: True si los datos son válidos

**Validaciones realizadas:**

1. **Artista requerido:**
   - ID del artista debe existir en la base de datos
   - Debe ser un número entero positivo

2. **Título requerido:**
   - No puede ser None o vacío
   - Debe ser string

3. **Año válido (opcional):**
   - Si se proporciona, debe ser un número entero
   - Debe estar en rango razonable (1900-actual+1)

4. **Formato válido:**
   - Debe ser uno de los formatos permitidos
   - Actualmente: 'Vinilo', 'CD', 'Digital', 'Cassette', 'Otro'

**Ejemplo:**

.. code-block:: python

   data_disco = {
       'artista': 1,  # ID existente
       'titulo': 'Exile on Main St.',
       'anio': 1972,
       'formato': 'Vinilo'
   }
   valido = validar_disco(data_disco)

validar_cancion(data)
~~~~~~~~~~~~~~~~~~~~~

Valida los datos de una canción.

**Parámetros:**
- ``data`` (dict): Diccionario con los datos de la canción

**Retorna:**
- ``bool``: True si los datos son válidos

**Validaciones realizadas:**

1. **Disco requerido:**
   - ID del disco debe existir en la base de datos

2. **Número de pista requerido:**
   - Debe ser un número entero positivo
   - No puede haber dos canciones con mismo número en el mismo disco

3. **Título requerido:**
   - No puede ser None o vacío

4. **Duración válida (opcional):**
   - Si se proporciona, debe tener formato válido (ej: "3:45")

**Ejemplo:**

.. code-block:: python

   data_cancion = {
       'numero_pista': 1,
       'titulo': 'Sympathy for the Devil',
       'duracion': '6:18',
       'disco': 1
   }
   valido = validar_cancion(data_cancion)

Funciones Auxiliares
--------------------

existe_artista(artista_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verifica si existe un artista con el ID especificado.

**Parámetros:**
- ``artista_id`` (int): ID del artista a verificar

**Retorna:**
- ``bool``: True si el artista existe

**Implementación:**

.. code-block:: python

   def existe_artista(artista_id):
       try:
           Artista.get_by_id(artista_id)
           return True
       except Artista.DoesNotExist:
           return False

existe_disco(disco_id)
~~~~~~~~~~~~~~~~~~~~~~

Verifica si existe un disco con el ID especificado.

**Parámetros:**
- ``disco_id`` (int): ID del disco a verificar

**Retorna:**
- ``bool``: True si el disco existe

existe_cancion(cancion_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Verifica si existe una canción con el ID especificado.

**Parámetros:**
- ``cancion_id`` (int): ID del canción a verificar

**Retorna:**
- ``bool``: True si la canción existe

Validaciones de Formato
-----------------------

validar_formato_duracion(duracion)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Valida que una duración tenga formato correcto (MM:SS).

**Parámetros:**
- ``duracion`` (str): String con la duración

**Retorna:**
- ``bool``: True si el formato es válido

**Formatos aceptados:**
- "3:45" (3 minutos, 45 segundos)
- "1:23:45" (1 hora, 23 minutos, 45 segundos)
- "45" (45 segundos)

**Implementación:**

.. code-block:: python

   import re

   def validar_formato_duracion(duracion):
       """Valida formato de duración MM:SS o H:MM:SS"""
       patron = re.compile(r'^(\d+:)?\d+:\d+$')
       return bool(patron.match(duracion))

validar_anio(anio)
~~~~~~~~~~~~~~~~~~

Valida que un año esté en rango válido.

**Parámetros:**
- ``anio`` (int): Año a validar

**Retorna:**
- ``bool``: True si el año es válido

**Rango válido:** 1900 hasta el año actual + 1

**Implementación:**

.. code-block:: python

   from datetime import datetime

   def validar_anio(anio):
       anio_actual = datetime.now().year
       return 1900 <= anio <= anio_actual + 1

Constantes de Validación
------------------------

FORMATOS_DISCO_VALIDOS
~~~~~~~~~~~~~~~~~~~~~~~

Lista de formatos de disco válidos.

.. code-block:: python

   FORMATOS_DISCO_VALIDOS = [
       'Vinilo',
       'CD',
       'Digital',
       'Cassette',
       'Otro'
   ]

TIPOS_ARTISTA_VALIDOS
~~~~~~~~~~~~~~~~~~~~~

Lista de tipos de artista válidos.

.. code-block:: python

   TIPOS_ARTISTA_VALIDOS = [
       'Solista',
       'Banda',
       'Dúo'
   ]

Mensajes de Error
-----------------

El módulo incluye mensajes de error descriptivos para validaciones fallidas.

**Ejemplos de mensajes:**

- "El nombre del artista es obligatorio"
- "Ya existe un artista con ese nombre"
- "El tipo de artista debe ser: Solista, Banda o Dúo"
- "El artista especificado no existe"
- "El formato del disco debe ser: Vinilo, CD, Digital, Cassette u Otro"
- "El año debe estar entre 1900 y {anio_actual + 1}"
- "El número de pista debe ser un entero positivo"
- "Ya existe una canción con ese número de pista en este disco"
- "El formato de duración debe ser MM:SS o H:MM:SS"

Integración con Controlador
---------------------------

Las funciones de validación se integran con el controlador:

.. code-block:: python

   class Controlador:
       def agregar_artista(self, data):
           if not validar_artista(data):
               return None
           return self.model_artista.agregar(data)

**Beneficios:**
- Validación antes de operaciones de base de datos
- Mensajes de error consistentes
- Prevención de datos corruptos
- Separación de responsabilidades

Consideraciones de Diseño
-------------------------

**Principios aplicados:**

1. **Validación temprana:** Verificar datos antes de operaciones costosas
2. **Mensajes descriptivos:** Errores claros para el usuario
3. **Reutilización:** Funciones auxiliares compartidas
4. **Consistencia:** Reglas de validación uniformes
5. **Extensibilidad:** Fácil agregar nuevas validaciones

**Buenas prácticas:**

- Validar tipos de datos
- Verificar restricciones de unicidad
- Validar referencias foráneas
- Proporcionar valores por defecto cuando sea apropiado
- Manejar casos edge (valores límite, strings vacíos, etc.)

**Rendimiento:**

- Consultas eficientes para verificar existencia
- Validación en memoria cuando posible
- Evitar validaciones redundantes
- Cache de resultados cuando apropiado