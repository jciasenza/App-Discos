servidor_logs module
===================

.. automodule:: servidor_logs
   :members:
   :undoc-members:
   :show-inheritance:

Clase ServidorLogs
------------------

Servidor TCP multihilo que recibe conexiones de clientes y registra eventos
en un archivo centralizado de logs.

Métodos Principales
~~~~~~~~~~~~~~~~~~~

__init__(host, puerto)
^^^^^^^^^^^^^^^^^^^^^^

Inicializa el servidor con configuración específica.

.. code-block:: python

   servidor = ServidorLogs(host='localhost', puerto=5000)

**Parámetros:**
- ``host`` (str): Dirección IP o hostname (default: 'localhost')
- ``puerto`` (int): Puerto TCP para escuchar (default: 5000)

iniciar()
^^^^^^^^^

Inicia el servidor y comienza a aceptar conexiones.

.. code-block:: python

   servidor = ServidorLogs()
   try:
       servidor.iniciar()
   except KeyboardInterrupt:
       servidor.detener()

Este método bloquea la ejecución hasta que se detiene el servidor.

manejar_cliente(cliente_socket, direccion_cliente)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Maneja la comunicación con un cliente específico (ejecutado en hilo separado).

**Parámetros:**
- ``cliente_socket``: Socket del cliente conectado
- ``direccion_cliente``: Tupla (IP, puerto) del cliente

**Proceso:**
1. Recibe datos JSON del cliente
2. Parsea el mensaje
3. Registra en archivo de logs
4. Envía confirmación al cliente
5. Maneja errores y desconexiones

detener()
^^^^^^^^^

Detiene el servidor y cierra todas las conexiones.

.. code-block:: python

   servidor.detener()

Formato de Mensajes
-------------------

Mensajes Recibidos
~~~~~~~~~~~~~~~~~~

Los clientes envían mensajes en formato JSON:

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

**Campos:**
- ``evento`` (str): Nombre del evento
- ``datos`` (dict): Datos asociados al evento
- ``nivel`` (str): Nivel de logging (INFO, WARNING, ERROR)
- ``cliente`` (str): Identificador del cliente origen

Mensajes de Respuesta
~~~~~~~~~~~~~~~~~~~~~

El servidor responde confirmando recepción:

.. code-block:: json

   {
       "estado": "recibido",
       "evento": "artista_agregado"
   }

Manejo de Múltiples Clientes
----------------------------

El servidor usa threading para manejar múltiples conexiones simultáneamente:

.. code-block:: python

   def iniciar(self):
       self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       self.servidor.bind((self.host, self.puerto))
       self.servidor.listen(5)  # Máximo 5 conexiones en cola

       while self.activo:
           cliente_socket, direccion_cliente = self.servidor.accept()
           hilo_cliente = threading.Thread(
               target=self.manejar_cliente,
               args=(cliente_socket, direccion_cliente)
           )
           hilo_cliente.daemon = True
           hilo_cliente.start()

Configuración de Logging
------------------------

El servidor configura logging automáticamente:

.. code-block:: python

   logging.basicConfig(
       filename='servidor_logs.log',
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s - %(message)s',
       datefmt='%Y-%m-%d %H:%M:%S'
   )

**Archivo generado:** ``servidor_logs.log``

Ejemplo de salida:

::

   2026-04-26 10:30:45 - INFO - Servidor iniciado en localhost:5000
   2026-04-26 10:30:47 - INFO - Cliente conectado desde ('127.0.0.1', 54321)
   2026-04-26 10:30:50 - INFO - [App-Discos] Evento: artista_agregado | Datos: {'id': 1, 'nombre': 'The Beatles'}
   2026-04-26 10:31:00 - WARNING - [App-Discos] Evento: disco_actualizado | Datos: {'id': 1, 'data': {'anio': 1969}}

Manejo de Errores
-----------------

El servidor maneja varios tipos de errores:

JSON Inválido
~~~~~~~~~~~~~

.. code-block:: python

   try:
       mensaje = json.loads(datos)
   except json.JSONDecodeError:
       logger.error(f"JSON inválido recibido de {direccion_cliente}")
       return

Conexión Perdida
~~~~~~~~~~~~~~~~

.. code-block:: python

   try:
       datos = cliente_socket.recv(1024).decode('utf-8')
       if not datos:
           break  # Cliente cerró conexión
   except Exception as e:
       logger.error(f"Error recibiendo datos: {e}")
       break

Socket Errors
~~~~~~~~~~~~~

.. code-block:: python

   try:
       self.servidor.bind((self.host, self.puerto))
   except OSError as e:
       print(f"Error iniciando servidor: {e}")
       return False

Configuración
-------------

La configuración se lee desde ``config_logs.py``:

.. code-block:: python

   SERVIDOR_CONFIG = {
       'host': 'localhost',
       'puerto': 5000,
       'max_conexiones': 5,
   }

Ejecución como Servicio
-----------------------

Para ejecutar el servidor como servicio del sistema:

**Linux (systemd):**

.. code-block:: bash

   # Crear archivo de servicio
   sudo nano /etc/systemd/system/servidor-logs.service

   [Unit]
   Description=Servidor de Logs App Discos
   After=network.target

   [Service]
   Type=simple
   User=appuser
   WorkingDirectory=/path/to/app
   ExecStart=/usr/bin/python3 /path/to/servidor_logs.py
   Restart=always

   [Install]
   WantedBy=multi-user.target

   # Habilitar y iniciar
   sudo systemctl enable servidor-logs
   sudo systemctl start servidor-logs

**Windows (como servicio):**

Usar ``nssm`` o ``sc`` para crear servicio Windows.

Monitoreo
---------

Comandos útiles para monitoreo:

.. code-block:: bash

   # Ver conexiones activas
   netstat -tlnp | grep :5000

   # Ver logs en tiempo real
   tail -f servidor_logs.log

   # Contar eventos por tipo
   grep "Evento:" servidor_logs.log | cut -d'|' -f1 | sort | uniq -c

Consideraciones de Seguridad
----------------------------

**Recomendaciones:**

1. **Firewall**: Limitar acceso al puerto solo a IPs autorizadas
2. **Autenticación**: Implementar tokens de autenticación
3. **Encriptación**: Usar TLS para comunicaciones sensibles
4. **Rate limiting**: Limitar frecuencia de mensajes por cliente
5. **Validación**: Validar formato y contenido de mensajes JSON

**Configuración básica de firewall (Linux):**

.. code-block:: bash

   # Permitir solo desde red local
   sudo ufw allow from 192.168.1.0/24 to any port 5000

   # O permitir solo IPs específicas
   sudo ufw allow from 192.168.1.100 to any port 5000