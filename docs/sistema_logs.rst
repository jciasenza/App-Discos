Sistema de Logs Cliente-Servidor
=================================

El sistema de logs implementa un patrón observador avanzado que permite registrar
eventos tanto localmente como en un servidor centralizado, proporcionando trazabilidad
completa de todas las operaciones del sistema.

Arquitectura General
--------------------

.. code-block:: text

   ┌─────────────────┐
   │   App Discos    │
   │   (main.py)     │
   └────────┬────────┘
            │
            ├─► ObservadorLog ──► app_discos.log (local)
            │
            └─► ObservadorClienteLogs ──► ClienteLogs
                                           │
                                           └─► ServidorLogs
                                                    │
                                                    └─► servidor_logs.log

Componentes del Sistema
-----------------------

ObservadorLog
~~~~~~~~~~~~~

Clase que registra eventos en un archivo local usando el módulo estándar ``logging``.

.. code-block:: python

   class ObservadorLog:
       def actualizar(self, evento, datos):
           if "agregado" in evento or "agregada" in evento:
               logger.info(f"Evento: {evento} | Datos: {datos}")
           elif "actualizado" in evento:
               logger.warning(f"Evento: {evento} | Datos: {datos}")
           elif "eliminado" in evento:
               logger.error(f"Evento: {evento} | Datos: {datos}")
           else:
               logger.info(f"Evento: {evento} | Datos: {datos}")

**Niveles de Log por Operación:**

- **INFO**: Operaciones de creación (agregar)
- **WARNING**: Operaciones de actualización
- **ERROR**: Operaciones de eliminación

ObservadorClienteLogs
~~~~~~~~~~~~~~~~~~~~~

Envía eventos a un servidor remoto TCP para logging centralizado.

.. code-block:: python

   class ObservadorClienteLogs:
       def __init__(self, cliente_logs):
           self.cliente_logs = cliente_logs

       def actualizar(self, evento, datos):
           # Convertir datos a formato serializable
           datos_dict = self._convertir_datos(datos)
           # Enviar al servidor
           self.cliente_logs.enviar_log(evento, datos_dict, nivel)

**Características:**

- Conversión automática de objetos Peewee a diccionarios
- Manejo de tipos complejos (sets, datetime, etc.)
- Conexión TCP persistente
- Reconexión automática en caso de fallo

ClienteLogs
~~~~~~~~~~~

Cliente TCP que se conecta al servidor de logs y envía eventos serializados en JSON.

**Métodos principales:**

- ``conectar()``: Establece conexión TCP con el servidor
- ``enviar_log(evento, datos, nivel)``: Envía un evento de log
- ``desconectar()``: Cierra la conexión TCP

**Formato JSON enviado:**

.. code-block:: json

   {
       "evento": "artista_agregado",
       "datos": {
           "id": 1,
           "nombre": "The Beatles",
           "tipo": "Banda"
       },
       "nivel": "INFO",
       "cliente": "App-Discos"
   }

ServidorLogs
~~~~~~~~~~~~

Servidor TCP multihilo que recibe conexiones de clientes y registra eventos en un archivo centralizado.

**Características:**

- Puerto configurable (por defecto: 5000)
- Manejo de múltiples clientes simultáneos
- Logging estructurado con timestamps
- Recuperación automática de errores de conexión

**Respuesta al cliente:**

.. code-block:: json

   {
       "estado": "recibido",
       "evento": "artista_agregado"
   }

Serialización JSON Personalizada
--------------------------------

El sistema incluye un codificador JSON personalizado para manejar tipos complejos:

.. code-block:: python

   class JSONEncoderPersonalizado(json.JSONEncoder):
       def default(self, o):
           # Manejar objetos Peewee
           if hasattr(o, '__dict__') and hasattr(o, '_meta'):
               return {
                   'id': getattr(o, 'id', None),
                   'tipo': o.__class__.__name__,
                   **{k: str(v) if isinstance(v, set) else v
                      for k, v in o.__dict__.items()
                      if not k.startswith('_')}
               }
           # Manejar sets
           elif isinstance(o, set):
               return list(o)
           # Manejar datetime
           elif isinstance(o, datetime):
               return o.isoformat()
           else:
               return str(o)

Configuración
-------------

**Archivo de configuración centralizado** (``config_logs.py``):

.. code-block:: python

   SERVIDOR_CONFIG = {
       'host': 'localhost',
       'puerto': 5000,
       'max_conexiones': 5,
   }

   CLIENTE_CONFIG = {
       'host': 'localhost',
       'puerto': 5000,
       'nombre_cliente': 'App-Discos',
       'timeout': 5,
   }

   LOGGING_CONFIG = {
       'archivo_servidor': 'servidor_logs.log',
       'archivo_cliente': 'cliente_logs.log',
       'archivo_local': 'app_discos.log',
       'level': 'INFO',
       'formato': '%(asctime)s - %(levelname)s - %(message)s',
       'fecha_formato': '%Y-%m-%d %H:%M:%S',
   }

Modos de Operación
------------------

**Modo Local (Siempre disponible):**

.. code-block:: bash

   python main.py
   # Registra solo en app_discos.log

**Modo Cliente-Servidor:**

.. code-block:: bash

   # Terminal 1 - Servidor
   python servidor_logs.py

   # Terminal 2 - Cliente
   python main.py
   # Registra en app_discos.log + servidor_logs.log + cliente_logs.log

Archivos de Log Generados
-------------------------

1. **app_discos.log** (Local)
   ::

      2026-04-26 10:30:45 - INFO - Evento: artista_agregado | Datos: <Artista object>
      2026-04-26 10:31:12 - WARNING - Evento: disco_actualizado | Datos: {'id': 1, 'data': {'anio': 1969}}
      2026-04-26 10:32:00 - ERROR - Evento: artista_eliminado | Datos: 1

2. **servidor_logs.log** (Centralizado)
   ::

      2026-04-26 10:30:45 - INFO - Servidor iniciado en localhost:5000
      2026-04-26 10:30:47 - INFO - Cliente conectado desde ('127.0.0.1', 54321)
      2026-04-26 10:30:50 - INFO - [App-Discos] Evento: artista_agregado | Datos: {'id': 1, 'nombre': 'The Beatles'}

3. **cliente_logs.log** (Cliente)
   ::

      2026-04-26 10:30:47 - INFO - Conectado al servidor en localhost:5000
      2026-04-26 10:30:50 - INFO - Log enviado: artista_agregado

Ejemplo de Uso Programático
---------------------------

.. code-block:: python

   from cliente_logs import ClienteLogs

   # Crear cliente
   cliente = ClienteLogs(nombre_cliente='Mi-App')

   # Conectar
   if cliente.conectar():
       # Enviar eventos
       cliente.enviar_log('usuario_registrado', {'id': 1, 'email': 'user@example.com'}, 'INFO')
       cliente.enviar_log('pago_procesado', {'monto': 99.99, 'metodo': 'tarjeta'}, 'INFO')
       cliente.enviar_log('error_sistema', {'codigo': 500, 'mensaje': 'Error interno'}, 'ERROR')

       # Desconectar
       cliente.desconectar()

Ventajas del Sistema
-------------------

✅ **Escalabilidad**: Múltiples clientes pueden conectarse simultáneamente
✅ **Resiliencia**: Funciona sin servidor (modo local)
✅ **Trazabilidad**: Logs completos con contexto y timestamps
✅ **Flexibilidad**: Niveles de log automáticos según operación
✅ **Robustez**: Manejo automático de tipos complejos y errores
✅ **Centralización**: Un único punto para monitoreo de todos los eventos