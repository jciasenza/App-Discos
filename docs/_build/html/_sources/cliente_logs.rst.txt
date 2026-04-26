cliente_logs module
===================

.. automodule:: cliente_logs
   :members:
   :undoc-members:
   :show-inheritance:

Clase ClienteLogs
-----------------

La clase ``ClienteLogs`` maneja la conexión TCP con el servidor de logs y el envío
de eventos serializados en JSON.

Métodos Principales
~~~~~~~~~~~~~~~~~~~

conectar()
^^^^^^^^^^

Establece conexión TCP con el servidor de logs.

.. code-block:: python

   cliente = ClienteLogs()
   if cliente.conectar():
       print("Conectado exitosamente")
   else:
       print("Error de conexión")

**Retorna:** ``bool`` - True si la conexión fue exitosa

enviar_log(evento, datos, nivel)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Envía un evento de log al servidor.

.. code-block:: python

   cliente.enviar_log(
       evento="usuario_registrado",
       datos={"id": 1, "email": "user@example.com"},
       nivel="INFO"
   )

**Parámetros:**
- ``evento`` (str): Nombre del evento
- ``datos`` (dict): Datos del evento
- ``nivel`` (str): Nivel de log (INFO, WARNING, ERROR)

**Retorna:** ``bool`` - True si el envío fue exitoso

desconectar()
^^^^^^^^^^^^^

Cierra la conexión TCP con el servidor.

.. code-block:: python

   cliente.desconectar()

JSONEncoderPersonalizado
------------------------

Codificador JSON personalizado que maneja tipos complejos de Python.

Tipos Soportados
~~~~~~~~~~~~~~~~

- **Objetos Peewee**: Convierte modelos a diccionarios
- **Sets**: Convierte a listas
- **Datetime**: Convierte a formato ISO
- **Objetos personalizados**: Convierte a string

Ejemplo de Uso
~~~~~~~~~~~~~~

.. code-block:: python

   import json
   from cliente_logs import JSONEncoderPersonalizado

   datos_complejos = {
       "usuario": {"id": 1, "tags": {"admin", "premium"}},
       "fecha": datetime.now()
   }

   json_str = json.dumps(datos_complejos, cls=JSONEncoderPersonalizado)
   print(json_str)
   # {"usuario": {"id": 1, "tags": ["admin", "premium"]}, "fecha": "2026-04-26T10:30:00"}

Manejo de Errores
-----------------

La clase maneja automáticamente varios tipos de errores:

- **Conexión perdida**: Intenta reconectar automáticamente
- **JSON inválido**: Registra error y continúa
- **Timeout**: Cancela operación y marca como desconectado
- **Socket errors**: Registra error y marca conexión como perdida

Configuración
-------------

La configuración se lee desde ``config_logs.py``:

.. code-block:: python

   CLIENTE_CONFIG = {
       'host': 'localhost',
       'puerto': 5000,
       'nombre_cliente': 'App-Discos',
       'timeout': 5,
   }

Logging Local
-------------

Además del envío remoto, el cliente mantiene logs locales en ``cliente_logs.log``
para trazabilidad de las operaciones de envío.

Ejemplo Completo
----------------

.. code-block:: python

   from cliente_logs import ClienteLogs

   # Crear cliente
   cliente = ClienteLogs(nombre_cliente='Mi-Aplicacion')

   # Conectar
   if cliente.conectar():
       # Enviar varios logs
       cliente.enviar_log('inicio_sesion', {'usuario': 'admin'}, 'INFO')
       cliente.enviar_log('operacion_exitosa', {'tipo': 'backup'}, 'INFO')
       cliente.enviar_log('error_critico', {'codigo': 500}, 'ERROR')

       # Desconectar
       cliente.desconectar()
   else:
       print("No se pudo conectar al servidor")