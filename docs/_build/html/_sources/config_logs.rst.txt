config_logs module
==================

.. automodule:: config_logs
   :members:
   :undoc-members:
   :show-inheritance:

Configuración Centralizada del Sistema de Logs
===============================================

Este módulo contiene toda la configuración del sistema de logs cliente-servidor,
permitiendo personalizar el comportamiento sin modificar el código fuente.

SERVIDOR_CONFIG
---------------

Configuración del servidor TCP de logs.

.. code-block:: python

   SERVIDOR_CONFIG = {
       'host': 'localhost',      # Dirección IP del servidor
       'puerto': 5000,           # Puerto TCP para conexiones
       'max_conexiones': 5,      # Máximo de conexiones en cola
   }

**Parámetros:**

host
^^^^

- **Tipo:** ``str``
- **Default:** ``'localhost'``
- **Descripción:** Dirección IP o hostname donde el servidor escuchará conexiones
- **Ejemplos:**
  - ``'localhost'`` - Solo conexiones locales
  - ``'0.0.0.0'`` - Todas las interfaces de red
  - ``'192.168.1.100'`` - IP específica

puerto
^^^^^^

- **Tipo:** ``int``
- **Default:** ``5000``
- **Descripción:** Puerto TCP para el servidor
- **Rango recomendado:** 1024-65535 (evitar puertos bien conocidos)
- **Ejemplos:** 5000, 8080, 9000

max_conexiones
^^^^^^^^^^^^^^

- **Tipo:** ``int``
- **Default:** ``5``
- **Descripción:** Número máximo de conexiones en cola de espera
- **Recomendación:** 5-10 para aplicaciones pequeñas

CLIENTE_CONFIG
--------------

Configuración del cliente TCP de logs.

.. code-block:: python

   CLIENTE_CONFIG = {
       'host': 'localhost',           # Servidor al que conectar
       'puerto': 5000,                # Puerto del servidor
       'nombre_cliente': 'App-Discos', # Identificador único
       'timeout': 5,                  # Timeout en segundos
   }

**Parámetros:**

host
^^^^

- **Tipo:** ``str``
- **Default:** ``'localhost'``
- **Descripción:** Dirección del servidor de logs
- **Debe coincidir** con ``SERVIDOR_CONFIG['host']``

puerto
^^^^^^

- **Tipo:** ``int``
- **Default:** ``5000``
- **Descripción:** Puerto del servidor de logs
- **Debe coincidir** con ``SERVIDOR_CONFIG['puerto']``

nombre_cliente
^^^^^^^^^^^^^^

- **Tipo:** ``str``
- **Default:** ``'App-Discos'``
- **Descripción:** Identificador único del cliente
- **Aparece en logs** para distinguir orígenes
- **Ejemplos:** ``'App-Discos'``, ``'Mi-Tienda'``, ``'Sistema-Ventas'``

timeout
^^^^^^^

- **Tipo:** ``int``
- **Default:** ``5``
- **Descripción:** Segundos de espera para conexiones
- **Recomendación:** 5-30 segundos

LOGGING_CONFIG
--------------

Configuración del sistema de logging de Python.

.. code-block:: python

   LOGGING_CONFIG = {
       'archivo_servidor': 'servidor_logs.log',
       'archivo_cliente': 'cliente_logs.log',
       'archivo_local': 'app_discos.log',
       'level': 'INFO',
       'formato': '%(asctime)s - %(levelname)s - %(message)s',
       'fecha_formato': '%Y-%m-%d %H:%M:%S',
   }

**Parámetros:**

archivo_servidor
^^^^^^^^^^^^^^^^

- **Tipo:** ``str``
- **Default:** ``'servidor_logs.log'``
- **Descripción:** Archivo donde el servidor guarda logs centralizados
- **Ubicación:** Directorio del servidor

archivo_cliente
^^^^^^^^^^^^^^^

- **Tipo:** ``str``
- **Default:** ``'cliente_logs.log'``
- **Descripción:** Archivo donde el cliente registra operaciones de envío
- **Ubicación:** Directorio del cliente

archivo_local
^^^^^^^^^^^^^

- **Tipo:** ``str``
- **Default:** ``'app_discos.log'``
- **Descripción:** Archivo de logs locales de la aplicación
- **Ubicación:** Directorio de la aplicación

level
^^^^^

- **Tipo:** ``str``
- **Valores:** ``'DEBUG'``, ``'INFO'``, ``'WARNING'``, ``'ERROR'``, ``'CRITICAL'``
- **Default:** ``'INFO'``
- **Descripción:** Nivel mínimo de logs a registrar

formato
^^^^^^^

- **Tipo:** ``str``
- **Default:** ``'%(asctime)s - %(levelname)s - %(message)s'``
- **Descripción:** Formato de las líneas de log
- **Variables disponibles:**
  - ``%(asctime)s`` - Timestamp
  - ``%(levelname)s`` - Nivel (INFO, WARNING, etc.)
  - ``%(message)s`` - Mensaje del log
  - ``%(name)s`` - Nombre del logger
  - ``%(filename)s`` - Archivo fuente

fecha_formato
^^^^^^^^^^^^^

- **Tipo:** ``str``
- **Default:** ``'%Y-%m-%d %H:%M:%S'``
- **Descripción:** Formato de fecha en ``%(asctime)s``
- **Códigos de formato:** Ver ``datetime.strftime()``

MENSAJES
--------

Mensajes de estado predefinidos para consistencia.

.. code-block:: python

   MENSAJES = {
       'servidor_iniciado': '✓ Servidor iniciado en {host}:{puerto}',
       'cliente_conectado': '✓ Cliente conectado desde {direccion}',
       'error_servidor': '✗ Error al iniciar servidor: {error}',
       'error_cliente': '✗ Error conectando al servidor: {error}',
       'conexion_perdida': '✗ Conexión perdida con el servidor',
   }

**Uso:**

.. code-block:: python

   from config_logs import MENSAJES
   print(MENSAJES['servidor_iniciado'].format(host='localhost', puerto=5000))

Configuraciones de Ejemplo
--------------------------

Desarrollo Local
~~~~~~~~~~~~~~~~

.. code-block:: python

   SERVIDOR_CONFIG = {
       'host': 'localhost',
       'puerto': 5000,
       'max_conexiones': 5,
   }

   CLIENTE_CONFIG = {
       'host': 'localhost',
       'puerto': 5000,
       'nombre_cliente': 'App-Discos-Dev',
       'timeout': 5,
   }

   LOGGING_CONFIG = {
       'level': 'DEBUG',  # Más verboso en desarrollo
       'archivo_servidor': 'servidor_dev.log',
       'archivo_cliente': 'cliente_dev.log',
       'archivo_local': 'app_dev.log',
   }

Producción con Red
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   SERVIDOR_CONFIG = {
       'host': '0.0.0.0',  # Todas las interfaces
       'puerto': 9000,     # Puerto no estándar
       'max_conexiones': 10,
   }

   CLIENTE_CONFIG = {
       'host': 'logs.empresa.com',  # Servidor central
       'puerto': 9000,
       'nombre_cliente': 'Sucursal-Norte',
       'timeout': 10,
   }

   LOGGING_CONFIG = {
       'level': 'WARNING',  # Solo warnings y errores en prod
       'formato': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
   }

Múltiples Entornos
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os

   entorno = os.getenv('ENTORNO', 'desarrollo')

   if entorno == 'produccion':
       SERVIDOR_CONFIG = {
           'host': 'logs-prod.empresa.com',
           'puerto': 443,  # Puerto seguro
       }
   else:  # desarrollo
       SERVIDOR_CONFIG = {
           'host': 'localhost',
           'puerto': 5000,
       }

Validación de Configuración
---------------------------

Función auxiliar para validar configuración al inicio:

.. code-block:: python

   def validar_config():
       """Valida que la configuración sea correcta"""
       # Validar puertos
       if not (1024 <= SERVIDOR_CONFIG['puerto'] <= 65535):
           raise ValueError("Puerto del servidor inválido")

       if not (1024 <= CLIENTE_CONFIG['puerto'] <= 65535):
           raise ValueError("Puerto del cliente inválido")

       # Validar niveles de log
       niveles_validos = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
       if LOGGING_CONFIG['level'] not in niveles_validos:
           raise ValueError(f"Nivel de log inválido: {LOGGING_CONFIG['level']}")

       # Validar timeout
       if CLIENTE_CONFIG['timeout'] < 1:
           raise ValueError("Timeout debe ser al menos 1 segundo")

       print("✓ Configuración validada correctamente")

Modificación en Tiempo de Ejecución
------------------------------------

Cambiar configuración dinámicamente:

.. code-block:: python

   from config_logs import CLIENTE_CONFIG

   # Cambiar configuración en runtime
   CLIENTE_CONFIG['timeout'] = 15
   CLIENTE_CONFIG['nombre_cliente'] = 'App-Modificada'

   # Nota: Los cambios no afectan instancias ya creadas
   # Es mejor reiniciar la aplicación

Persistencia de Configuración
-----------------------------

Para persistir cambios en archivo:

.. code-block:: python

   import json

   def guardar_config():
       config = {
           'SERVIDOR_CONFIG': SERVIDOR_CONFIG,
           'CLIENTE_CONFIG': CLIENTE_CONFIG,
           'LOGGING_CONFIG': LOGGING_CONFIG,
       }
       with open('config_personalizada.json', 'w') as f:
           json.dump(config, f, indent=2)

   def cargar_config():
       try:
           with open('config_personalizada.json', 'r') as f:
               config = json.load(f)
               globals().update(config)
               print("✓ Configuración personalizada cargada")
       except FileNotFoundError:
           print("⚠ Usando configuración por defecto")

Consideraciones de Seguridad
----------------------------

**No incluir información sensible:**

.. code-block:: python

   # ❌ MAL - Credenciales expuestas
   CLIENTE_CONFIG = {
       'usuario': 'admin',
       'password': 'secreto123',
   }

   # ✅ BIEN - Usar variables de entorno
   import os
   CLIENTE_CONFIG = {
       'usuario': os.getenv('LOG_USER'),
       'password': os.getenv('LOG_PASS'),
   }

**Recomendaciones:**

1. Usar variables de entorno para credenciales
2. No commitear archivos con configuración sensible
3. Usar ``.env`` files para desarrollo local
4. Validar configuración al inicio de la aplicación