Módulo de Modelos y Patrón Observador
=====================================

.. automodule:: model
   :members:
   :undoc-members:
   :show-inheritance:

Clases de Base de Datos
-----------------------

BaseModel
~~~~~~~~~

Clase base para todos los modelos de Peewee.

.. code-block:: python

   class BaseModel(Model):
       class Meta:
           database = db_discos

Artista
~~~~~~~

Modelo para artistas y bandas musicales.

**Campos:**
- ``id``: Identificador único (autoincremental)
- ``nombre``: Nombre del artista (único, obligatorio)
- ``tipo``: Tipo de artista (Solista, Banda, Dúo)
- ``info``: Información biográfica (opcional)
- ``foto``: Ruta a la imagen de perfil (opcional)

Discos
~~~~~~

Modelo para discos musicales.

**Campos:**
- ``id``: Identificador único (autoincremental)
- ``artista``: ForeignKey al artista (con CASCADE)
- ``titulo``: Título del disco (obligatorio)
- ``anio``: Año de lanzamiento (opcional)
- ``formato``: Formato físico/digital (obligatorio)
- ``portada``: Ruta a la imagen de portada (opcional)

Cancion
~~~~~~~

Modelo para canciones individuales.

**Campos:**
- ``id``: Identificador único (autoincremental)
- ``numero_pista``: Número de pista en el disco
- ``titulo``: Título de la canción (obligatorio)
- ``duracion``: Duración en formato string (opcional)
- ``disco``: ForeignKey al disco (con CASCADE)

**Restricciones:**
- UNIQUE(numero_pista, disco) - No puede haber dos pistas con mismo número en un disco

Patrón Observador
-----------------

El módulo implementa el patrón observador para logging automático de operaciones.

Observable
~~~~~~~~~~

Clase base que permite ser observada por múltiples observadores.

.. code-block:: python

   class Observable:
       def __init__(self):
           self._observadores = []

       def agregar_observador(self, observador):
           """Agrega un observador a la lista"""
           self._observadores.append(observador)

       def eliminar_observador(self, observador):
           """Elimina un observador de la lista"""
           self._observadores.remove(observador)

       def notificar(self, evento, datos):
           """Notifica a todos los observadores sobre un evento"""
           for obs in self._observadores:
               obs.actualizar(evento, datos)

ObservadorLog
~~~~~~~~~~~~~~

Observador que registra eventos en archivo local usando logging de Python.

**Niveles de log por evento:**

- **INFO**: Eventos de creación (``*_agregado``, ``*_agregada``)
- **WARNING**: Eventos de actualización (``*_actualizado``, ``*_actualizada``)
- **ERROR**: Eventos de eliminación (``*_eliminado``, ``*_eliminada``)

**Archivo generado:** ``app_discos.log``

ObservadorClienteLogs
~~~~~~~~~~~~~~~~~~~~~

Observador que envía eventos a un servidor TCP remoto para logging centralizado.

**Características:**

- Conexión TCP automática al servidor de logs
- Serialización JSON personalizada para objetos complejos
- Conversión automática de modelos Peewee a diccionarios
- Manejo de tipos especiales (sets, datetime, etc.)
- Reconexión automática en caso de fallo

**Método ``_convertir_datos()``:**

Convierte objetos de cualquier tipo a formato serializable:

.. code-block:: python

   @staticmethod
   def _convertir_datos(datos):
       # Maneja modelos Peewee
       if hasattr(datos, '_meta'):
           return {campo: getattr(datos, campo) for campo in datos._meta.fields}
       # Maneja diccionarios con sets
       elif isinstance(datos, dict):
           return {k: v for k, v in datos.items() if not isinstance(v, set)}
       # Otros tipos
       else:
           return str(datos)

Clases CRUD
-----------

ArtistaModel
~~~~~~~~~~~~

Modelo de negocio para operaciones CRUD con artistas.

**Hereda de:** ``Observable``

**Métodos principales:**

agregar(data)
^^^^^^^^^^^^^

Crea un nuevo artista y notifica a los observadores.

.. code-block:: python

   artista = ArtistaModel()
   nuevo_artista = artista.agregar({
       'nombre': 'The Beatles',
       'tipo': 'Banda',
       'info': 'Banda legendaria de rock'
   })

listar()
^^^^^^^^

Retorna todos los artistas ordenados por nombre.

.. code-block:: python

   artistas = ArtistaModel().listar()
   for artista in artistas:
       print(artista.nombre)

obtener(artista_id)
^^^^^^^^^^^^^^^^^^^

Obtiene un artista específico por ID.

.. code-block:: python

   artista = ArtistaModel().obtener(1)
   if artista:
       print(f"Encontrado: {artista.nombre}")

actualizar(artista_id, data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Actualiza los datos de un artista.

.. code-block:: python

   resultado = ArtistaModel().actualizar(1, {'tipo': 'Super Banda'})

eliminar(artista_id)
^^^^^^^^^^^^^^^^^^^^

Elimina un artista de la base de datos.

.. code-block:: python

   resultado = ArtistaModel().eliminar(1)

buscar(texto)
^^^^^^^^^^^^^

Busca artistas por nombre (búsqueda insensible a mayúsculas).

.. code-block:: python

   resultados = ArtistaModel().buscar('beatles')

DiscoModel
~~~~~~~~~~

Modelo de negocio para operaciones CRUD con discos.

**Hereda de:** ``Observable``

**Métodos principales:**

agregar(data)
^^^^^^^^^^^^^

Crea un nuevo disco.

.. code-block:: python

   disco = DiscoModel()
   nuevo_disco = disco.agregar({
       'artista': 1,  # ID del artista
       'titulo': 'Abbey Road',
       'anio': 1969,
       'formato': 'Vinilo'
   })

listar()
^^^^^^^^

Retorna todos los discos con información del artista, ordenados por ID descendente.

obtener(disco_id)
^^^^^^^^^^^^^^^^^

Obtiene un disco específico con su artista relacionado.

actualizar(disco_id, data)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Actualiza los datos de un disco.

eliminar(disco_id)
^^^^^^^^^^^^^^^^^^

Elimina un disco y todas sus canciones asociadas (CASCADE).

buscar(texto)
^^^^^^^^^^^^^

Busca discos por título o nombre de artista.

CancionModel
~~~~~~~~~~~~

Modelo de negocio para operaciones CRUD con canciones.

**Hereda de:** ``Observable``

**Métodos principales:**

agregar(data)
^^^^^^^^^^^^^

Crea una nueva canción.

.. code-block:: python

   cancion = CancionModel()
   nueva_cancion = cancion.agregar({
       'numero_pista': 1,
       'titulo': 'Come Together',
       'disco': 1  # ID del disco
   })

listar_por_disco(disco_id)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Obtiene todas las canciones de un disco específico, ordenadas por número de pista.

listar_todas_con_disco()
^^^^^^^^^^^^^^^^^^^^^^^^

Obtiene todas las canciones con información de disco y artista.

actualizar(cancion_id, data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Actualiza los datos de una canción.

eliminar(cancion_id)
^^^^^^^^^^^^^^^^^^^^

Elimina una canción específica.

buscar(texto)
^^^^^^^^^^^^^

Busca canciones por título, nombre de artista o título de disco.

Funciones de Inicialización
---------------------------

inicializar_db()
~~~~~~~~~~~~~~~~

Función que inicializa la conexión a la base de datos y crea las tablas si no existen.

.. code-block:: python

   inicializar_db()  # Se ejecuta automáticamente al importar el módulo

**Operaciones realizadas:**
1. Verifica si la conexión está cerrada
2. Conecta a la base de datos SQLite
3. Activa claves foráneas (PRAGMA foreign_keys = ON)
4. Crea las tablas Artista, Discos y Cancion si no existen

Configuración de Logging
------------------------

El módulo configura logging global para toda la aplicación:

.. code-block:: python

   logging.basicConfig(
       filename='app_discos.log',
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s - %(message)s',
       datefmt='%Y-%m-%d %H:%M:%S'
   )

**Archivo generado:** ``app_discos.log``

**Ejemplo de salida:**

::

   2026-04-26 10:30:45 - INFO - Evento: artista_agregado | Datos: <Artista object>
   2026-04-26 10:31:12 - WARNING - Evento: disco_actualizado | Datos: {'id': 1, 'data': {'anio': 1969}}
   2026-04-26 10:32:00 - ERROR - Evento: artista_eliminado | Datos: 1

Integración con Sistema de Logs
-------------------------------

Los modelos se integran automáticamente con el sistema de logs:

.. code-block:: python

   # En main.py
   model_artista = ArtistaModel()

   # Agregar observadores
   observador_log = ObservadorLog()
   model_artista.agregar_observador(observador_log)

   # Si hay servidor disponible
   cliente_logs = ClienteLogs()
   if cliente_logs.conectar():
       observador_cliente = ObservadorClienteLogs(cliente_logs)
       model_artista.agregar_observador(observador_cliente)

**Flujo de notificación:**

1. Usuario ejecuta operación (ej: ``agregar()``)
2. Modelo ejecuta lógica de negocio
3. Modelo llama ``notificar(evento, datos)``
4. Todos los observadores reciben la notificación
5. ``ObservadorLog`` escribe en archivo local
6. ``ObservadorClienteLogs`` envía al servidor remoto

Consideraciones de Rendimiento
------------------------------

**Optimizaciones implementadas:**

1. **Lazy Loading**: Peewee carga datos solo cuando se necesitan
2. **Joins eficientes**: Consultas con JOIN para evitar N+1 queries
3. **Índices**: Índice único en (numero_pista, disco) para Cancion
4. **Conexión persistente**: Reutilización de conexión a BD
5. **Logging asíncrono**: Los observadores no bloquean operaciones principales

**Recomendaciones:**

- Usar ``select()`` en lugar de ``get()`` para múltiples registros
- Implementar paginación para listados grandes
- Considerar índices adicionales según patrones de consulta comunes
- Monitorear uso de memoria en operaciones con muchos datos
