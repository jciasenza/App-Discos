Módulo Controlador
==================

.. automodule:: controller
   :members:
   :undoc-members:
   :show-inheritance:
Clase Controlador
-----------------

La clase principal que maneja la lógica de negocio y la interacción con la interfaz de usuario.

.. code-block:: python

   class Controlador:
       def __init__(self):
           self.model_artista = ArtistaModel()
           self.model_disco = DiscoModel()
           self.model_cancion = CancionModel()
           self.view = None

Decoradores de Logging
---------------------

El controlador utiliza decoradores para logging automático de operaciones.

log_alta
~~~~~~~~

Decorador para operaciones de creación (alta).

.. code-block:: python

   @log_alta
   def agregar_artista(self, data):
       """Agrega un nuevo artista con logging automático"""
       return self.model_artista.agregar(data)

**Características:**
- Registra evento ``artista_agregado`` con datos del nuevo artista
- Nivel de log: INFO
- Se ejecuta después de la operación exitosa

log_actualizacion
~~~~~~~~~~~~~~~~~

Decorador para operaciones de actualización.

.. code-block:: python

   @log_actualizacion
   def actualizar_artista(self, artista_id, data):
       """Actualiza un artista con logging automático"""
       return self.model_artista.actualizar(artista_id, data)

**Características:**
- Registra evento ``artista_actualizado`` con ID y datos nuevos
- Nivel de log: WARNING
- Se ejecuta después de la operación exitosa

log_baja
~~~~~~~~

Decorador para operaciones de eliminación (baja).

.. code-block:: python

   @log_baja
   def eliminar_artista(self, artista_id):
       """Elimina un artista con logging automático"""
       return self.model_artista.eliminar(artista_id)

**Características:**
- Registra evento ``artista_eliminado`` con ID del artista eliminado
- Nivel de log: ERROR
- Se ejecuta después de la operación exitosa

Implementación de Decoradores
-----------------------------

Los decoradores están implementados como funciones que retornan decoradores:

.. code-block:: python

   def log_alta(func):
       def wrapper(self, *args, **kwargs):
           resultado = func(self, *args, **kwargs)
           if resultado:
               # Logging de la operación exitosa
               logging.info(f"Operación de alta exitosa: {func.__name__}")
           return resultado
       return wrapper

**Ventajas:**
- Transparente: No modifica la lógica de negocio
- Automático: Se ejecuta en cada llamada decorada
- Configurable: Fácil cambiar comportamiento de logging
- Reutilizable: Mismo decorador para diferentes métodos

Métodos de Artistas
-------------------

agregar_artista(data)
~~~~~~~~~~~~~~~~~~~~~

Agrega un nuevo artista a la base de datos.

**Parámetros:**
- ``data`` (dict): Diccionario con datos del artista
  - ``nombre`` (str): Nombre del artista (requerido)
  - ``tipo`` (str): Tipo de artista (opcional)
  - ``info`` (str): Información biográfica (opcional)
  - ``foto`` (str): Ruta a imagen (opcional)

**Retorna:**
- ``Artista``: Instancia del artista creado, o ``None`` si falla

**Ejemplo:**

.. code-block:: python

   controlador = Controlador()
   nuevo_artista = controlador.agregar_artista({
       'nombre': 'Queen',
       'tipo': 'Banda',
       'info': 'Banda británica de rock'
   })

listar_artistas()
~~~~~~~~~~~~~~~~~

Obtiene todos los artistas ordenados alfabéticamente.

**Retorna:**
- ``list``: Lista de instancias ``Artista``

buscar_artistas(texto)
~~~~~~~~~~~~~~~~~~~~~~

Busca artistas por nombre.

**Parámetros:**
- ``texto`` (str): Texto a buscar (insensible a mayúsculas)

**Retorna:**
- ``list``: Lista de artistas que coinciden con la búsqueda

obtener_artista(artista_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtiene un artista específico por su ID.

**Parámetros:**
- ``artista_id`` (int): ID del artista

**Retorna:**
- ``Artista`` o ``None``: El artista encontrado o None

actualizar_artista(artista_id, data)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Actualiza los datos de un artista.

**Parámetros:**
- ``artista_id`` (int): ID del artista a actualizar
- ``data`` (dict): Campos a actualizar

**Retorna:**
- ``bool``: True si se actualizó correctamente

eliminar_artista(artista_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Elimina un artista de la base de datos.

**Parámetros:**
- ``artista_id`` (int): ID del artista a eliminar

**Retorna:**
- ``bool``: True si se eliminó correctamente

Métodos de Discos
-----------------

agregar_disco(data)
~~~~~~~~~~~~~~~~~~~

Agrega un nuevo disco.

**Parámetros:**
- ``data`` (dict): Datos del disco
  - ``artista`` (int): ID del artista
  - ``titulo`` (str): Título del disco
  - ``anio`` (int): Año de lanzamiento (opcional)
  - ``formato`` (str): Formato del disco
  - ``portada`` (str): Ruta a imagen de portada (opcional)

**Retorna:**
- ``Discos``: Instancia del disco creado

listar_discos()
~~~~~~~~~~~~~~~

Obtiene todos los discos con información del artista.

**Retorna:**
- ``list``: Lista de discos con artista relacionado

buscar_discos(texto)
~~~~~~~~~~~~~~~~~~~~

Busca discos por título o nombre de artista.

**Parámetros:**
- ``texto`` (str): Texto a buscar

**Retorna:**
- ``list``: Lista de discos que coinciden

obtener_disco(disco_id)
~~~~~~~~~~~~~~~~~~~~~~~

Obtiene un disco específico con su artista.

**Parámetros:**
- ``disco_id`` (int): ID del disco

**Retorna:**
- ``Discos``: Disco con artista relacionado

actualizar_disco(disco_id, data)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Actualiza los datos de un disco.

**Parámetros:**
- ``disco_id`` (int): ID del disco
- ``data`` (dict): Campos a actualizar

**Retorna:**
- ``bool``: True si se actualizó correctamente

eliminar_disco(disco_id)
~~~~~~~~~~~~~~~~~~~~~~~~

Elimina un disco y todas sus canciones.

**Parámetros:**
- ``disco_id`` (int): ID del disco

**Retorna:**
- ``bool``: True si se eliminó correctamente

Métodos de Canciones
--------------------

agregar_cancion(data)
~~~~~~~~~~~~~~~~~~~~~

Agrega una nueva canción.

**Parámetros:**
- ``data`` (dict): Datos de la canción
  - ``numero_pista`` (int): Número de pista
  - ``titulo`` (str): Título de la canción
  - ``duracion`` (str): Duración (opcional)
  - ``disco`` (int): ID del disco

**Retorna:**
- ``Cancion``: Instancia de la canción creada

listar_canciones_por_disco(disco_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtiene todas las canciones de un disco específico.

**Parámetros:**
- ``disco_id`` (int): ID del disco

**Retorna:**
- ``list``: Lista de canciones ordenadas por número de pista

listar_todas_canciones()
~~~~~~~~~~~~~~~~~~~~~~~~

Obtiene todas las canciones con información de disco y artista.

**Retorna:**
- ``list``: Lista completa de canciones

buscar_canciones(texto)
~~~~~~~~~~~~~~~~~~~~~~~

Busca canciones por título, artista o disco.

**Parámetros:**
- ``texto`` (str): Texto a buscar

**Retorna:**
- ``list``: Lista de canciones que coinciden

actualizar_cancion(cancion_id, data)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Actualiza los datos de una canción.

**Parámetros:**
- ``cancion_id`` (int): ID de la canción
- ``data`` (dict): Campos a actualizar

**Retorna:**
- ``bool``: True si se actualizó correctamente

eliminar_cancion(cancion_id)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Elimina una canción específica.

**Parámetros:**
- ``cancion_id`` (int): ID de la canción

**Retorna:**
- ``bool``: True si se eliminó correctamente

Métodos de Validación
---------------------

validar_artista(data)
~~~~~~~~~~~~~~~~~~~~~

Valida los datos de un artista antes de guardarlo.

**Parámetros:**
- ``data`` (dict): Datos del artista

**Retorna:**
- ``bool``: True si los datos son válidos

**Validaciones realizadas:**
- Nombre requerido y no vacío
- Tipo debe ser uno de los valores permitidos
- Nombre único en la base de datos

validar_disco(data)
~~~~~~~~~~~~~~~~~~~

Valida los datos de un disco.

**Parámetros:**
- ``data`` (dict): Datos del disco

**Retorna:**
- ``bool``: True si los datos son válidos

**Validaciones realizadas:**
- Artista ID debe existir
- Título requerido
- Formato debe ser válido
- Año debe ser un número válido si se proporciona

validar_cancion(data)
~~~~~~~~~~~~~~~~~~~~~

Valida los datos de una canción.

**Parámetros:**
- ``data`` (dict): Datos de la canción

**Retorna:**
- ``bool``: True si los datos son válidos

**Validaciones realizadas:**
- Disco ID debe existir
- Número de pista debe ser positivo
- Título requerido
- No puede haber dos pistas con mismo número en un disco

Manejo de Imágenes
------------------

El controlador incluye métodos para manejar rutas de imágenes de forma segura.

obtener_ruta_imagen(objeto, campo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtiene la ruta de imagen de un objeto de forma segura.

.. code-block:: python

   def obtener_ruta_imagen(self, objeto, campo):
       """Obtiene ruta de imagen usando getattr para evitar AttributeError"""
       return getattr(objeto, campo, None)

**Parámetros:**
- ``objeto``: Instancia del modelo (Artista, Discos)
- ``campo`` (str): Nombre del campo de imagen ('foto', 'portada')

**Retorna:**
- ``str`` o ``None``: Ruta de la imagen o None si no existe

**Ventajas:**
- Evita ``AttributeError`` si el campo no existe
- Maneja objetos que pueden no tener el atributo
- Compatible con versiones anteriores del modelo

Manejo de Errores
-----------------

El controlador implementa manejo robusto de errores:

.. code-block:: python

   try:
       resultado = self.model_artista.agregar(data)
       if resultado:
           # Operación exitosa
           return True
       else:
           # Validación fallida
           return False
   except Exception as e:
       # Error inesperado
       logging.error(f"Error en agregar_artista: {e}")
       return False

**Estrategias de manejo:**
- Captura de excepciones específicas de base de datos
- Logging de errores con contexto
- Retorno de valores booleanos para indicar éxito/fallo
- Mensajes de error descriptivos para la UI

Integración con Vistas
-----------------------

El controlador se conecta con las vistas Tkinter:

.. code-block:: python

   def set_view(self, view):
       """Establece la referencia a la vista principal"""
       self.view = view

   def actualizar_vista_artistas(self):
       """Actualiza la lista de artistas en la vista"""
       if self.view:
           artistas = self.listar_artistas()
           self.view.actualizar_lista_artistas(artistas)

**Patrón implementado:**
- Controlador mantiene referencia a la vista
- Métodos específicos para actualizar diferentes secciones
- Separación clara entre lógica de negocio y presentación

Consideraciones de Diseño
-------------------------

**Principios SOLID aplicados:**

1. **Single Responsibility**: Cada método tiene una responsabilidad clara
2. **Open/Closed**: Decoradores permiten extender funcionalidad sin modificar código existente
3. **Liskov Substitution**: Los decoradores son compatibles con cualquier método
4. **Interface Segregation**: Métodos específicos para cada entidad
5. **Dependency Inversion**: El controlador no depende de implementaciones concretas

**Patrones de diseño utilizados:**

- **Decorator Pattern**: Para logging automático
- **Observer Pattern**: Integración con sistema de logs (en modelos)
- **MVC Pattern**: Separación entre modelo, vista y controlador
- **Factory Pattern**: Creación de instancias de modelos

**Buenas prácticas implementadas:**

- Validación de entrada antes de operaciones
- Manejo consistente de errores
- Logging automático de operaciones
- Nombres descriptivos de métodos
- Documentación completa con docstrings