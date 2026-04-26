Módulo Principal
==================

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:
Función main()
--------------

Punto de entrada principal de la aplicación.

.. code-block:: python

   def main():
       """Función principal que inicializa y ejecuta la aplicación"""
       try:
           # Inicialización del sistema de logs
           inicializar_logs()

           # Crear instancias de modelos con observadores
           model_artista = ArtistaModel()
           model_disco = DiscoModel()
           model_cancion = CancionModel()

           # Configurar observadores
           configurar_observadores(model_artista, model_disco, model_cancion)

           # Crear controlador
           controlador = Controlador()

           # Crear vista principal
           root = tk.Tk()
           app = HomeView(root, controlador)

           # Configurar cierre graceful
           root.protocol("WM_DELETE_WINDOW", lambda: cerrar_aplicacion(root))

           # Iniciar bucle de eventos
           root.mainloop()

       except Exception as e:
           logging.critical(f"Error crítico en main(): {e}")
           sys.exit(1)

Inicialización del Sistema de Logs
----------------------------------

inicializar_logs()
~~~~~~~~~~~~~~~~~~

Configura el sistema de logging distribuido cliente-servidor.

.. code-block:: python

   def inicializar_logs():
       """Inicializa el sistema de logs cliente-servidor"""
       try:
           # Iniciar servidor de logs en hilo separado
           servidor_thread = threading.Thread(target=iniciar_servidor_logs, daemon=True)
           servidor_thread.start()

           # Pequeña pausa para que el servidor inicie
           time.sleep(0.1)

           # Configurar cliente de logs
           global cliente_logs
           cliente_logs = ClienteLogs()

           logging.info("Sistema de logs inicializado correctamente")

       except Exception as e:
           logging.error(f"Error inicializando sistema de logs: {e}")
           # Continuar sin logs remotos si falla
           pass

**Componentes inicializados:**

1. **Servidor TCP**: Hilo daemon que acepta conexiones de logging
2. **Cliente TCP**: Instancia para enviar logs al servidor local
3. **Logging básico**: Configuración de logging de Python como respaldo

iniciar_servidor_logs()
~~~~~~~~~~~~~~~~~~~~~~~

Función que ejecuta el servidor de logs en un hilo separado.

.. code-block:: python

   def iniciar_servidor_logs():
       """Inicia el servidor de logs en puerto 9999"""
       servidor = ServidorLogs()
       servidor.iniciar()

**Características:**
- Puerto fijo: 9999
- Multihilo: Maneja múltiples conexiones simultáneas
- Daemon thread: Se cierra automáticamente al terminar la aplicación

Configuración de Observadores
-----------------------------

configurar_observadores(model_artista, model_disco, model_cancion)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configura el patrón observador para logging automático en todos los modelos.

.. code-block:: python

   def configurar_observadores(model_artista, model_disco, model_cancion):
       """Configura observadores para logging automático"""

       # Crear observadores
       observador_log = ObservadorLog()

       # Agregar observador local a todos los modelos
       model_artista.agregar_observador(observador_log)
       model_disco.agregar_observador(observador_log)
       model_cancion.agregar_observador(observador_log)

       # Si hay cliente de logs disponible, agregar observador remoto
       if cliente_logs and cliente_logs.conectar():
           observador_cliente = ObservadorClienteLogs(cliente_logs)
           model_artista.agregar_observador(observador_cliente)
           model_disco.agregar_observador(observador_cliente)
           model_cancion.agregar_observador(observador_cliente)

           logging.info("Observador remoto configurado")
       else:
           logging.warning("Cliente de logs no disponible, usando solo logging local")

**Observadores configurados:**

- **ObservadorLog**: Logging a archivo local (``app_discos.log``)
- **ObservadorClienteLogs**: Logging remoto via TCP (opcional)

Manejo de Cierre de Aplicación
------------------------------

cerrar_aplicacion(root)
~~~~~~~~~~~~~~~~~~~~~~~

Función para cerrar la aplicación de forma graceful.

.. code-block:: python

   def cerrar_aplicacion(root):
       """Cierra la aplicación limpiamente"""
       try:
           # Cerrar conexión del cliente de logs
           if cliente_logs:
               cliente_logs.cerrar()

           # Cerrar ventana principal
           root.quit()

           logging.info("Aplicación cerrada correctamente")

       except Exception as e:
           logging.error(f"Error cerrando aplicación: {e}")
       finally:
           sys.exit(0)

**Operaciones de limpieza:**
1. Cierra conexiones TCP del cliente de logs
2. Cierra la ventana Tkinter
3. Registra el cierre en logs
4. Sale del programa con código 0

Arquitectura General
--------------------

**Flujo de inicialización:**

1. **Configuración de logs**: Servidor y cliente TCP
2. **Modelos observables**: Instancias con patrón observador
3. **Controlador**: Lógica de negocio con decoradores
4. **Vista principal**: Interfaz gráfica Tkinter
5. **Bucle de eventos**: Espera interacciones del usuario

**Componentes principales:**

- **main.py**: Punto de entrada y orquestación
- **model.py**: Modelos de datos con observadores
- **controller.py**: Lógica de negocio con decoradores
- **views/**: Interfaces gráficas Tkinter
- **cliente_logs.py**: Cliente TCP para logs remotos
- **servidor_logs.py**: Servidor TCP para recepción de logs
- **config_logs.py**: Configuraciones centralizadas

Sistema de Logging Distribuido
------------------------------

La aplicación implementa un sistema de logging de dos niveles:

**Nivel Local:**
- Archivo: ``app_discos.log``
- Formato: timestamp - nivel - mensaje
- Eventos: Todas las operaciones CRUD

**Nivel Remoto (opcional):**
- Protocolo: TCP/IP
- Puerto: 9999
- Serialización: JSON personalizado
- Eventos: Mismos que local, enviados al servidor

**Beneficios del sistema distribuido:**
- **Centralización**: Logs de múltiples instancias en un servidor
- **Respaldo**: Logging local como fallback
- **Monitoreo**: Posibilidad de monitoreo en tiempo real
- **Escalabilidad**: Arquitectura cliente-servidor extensible

Manejo de Errores Global
------------------------

**Estrategias implementadas:**

1. **Try-catch en main()**: Captura errores críticos de inicialización
2. **Logging de errores**: Todos los errores se registran
3. **Cierre graceful**: Limpieza de recursos al salir
4. **Fallbacks**: Continúa funcionando sin componentes opcionales

**Ejemplo de manejo:**

.. code-block:: python

   try:
       # Operación que puede fallar
       resultado = operacion_riesgosa()
   except Exception as e:
       logging.error(f"Error en operacion_riesgosa: {e}")
       # Continuar con operación alternativa
       resultado = operacion_alternativa()

Configuración de Entorno
------------------------

**Dependencias requeridas:**

- Python 3.7+
- peewee (ORM)
- tkinter (interfaz gráfica)
- Módulos estándar: socket, threading, json, logging

**Archivos de configuración:**

- ``config_logs.py``: Configuraciones de logging
- Base de datos SQLite creada automáticamente

**Variables globales:**

- ``cliente_logs``: Instancia global del cliente TCP (None si no disponible)

Consideraciones de Rendimiento
------------------------------

**Optimizaciones implementadas:**

1. **Hilos separados**: Servidor de logs no bloquea UI
2. **Conexiones lazy**: Cliente se conecta solo cuando hay observadores remotos
3. **Logging asíncrono**: Operaciones de logging no bloquean operaciones principales
4. **Daemon threads**: Threads se cierran automáticamente

**Recomendaciones:**

- Monitorear uso de memoria en operaciones intensivas
- Considerar pool de conexiones para múltiples clientes
- Implementar timeouts en conexiones TCP
- Usar compresión para logs grandes si es necesario

Modo de Desarrollo vs Producción
---------------------------------

**Modo Desarrollo:**
- Servidor de logs local incluido
- Logging verbose activado
- Errores mostrados en consola

**Modo Producción:**
- Servidor de logs dedicado recomendado
- Logging configurado según necesidades
- Errores solo en archivos de log

**Configuración por entorno:**

.. code-block:: python

   import os

   if os.getenv('ENV') == 'production':
       # Configuración de producción
       configurar_logging_produccion()
   else:
       # Configuración de desarrollo
       configurar_logging_desarrollo()