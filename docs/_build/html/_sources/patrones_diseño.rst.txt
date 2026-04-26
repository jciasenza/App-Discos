Patrones de Diseño Implementados
================================

La aplicación implementa varios patrones de diseño modernos para lograr un código
mantenible, extensible y bien estructurado.

Patrón Observador (Observer Pattern)
------------------------------------

El patrón observador permite que objetos interesados sean notificados automáticamente
cuando ocurre un cambio en el estado de otro objeto.

Implementación en el Sistema de Logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Clase Observable Base:**

.. code-block:: python

   class Observable:
       def __init__(self):
           self._observadores = []

       def agregar_observador(self, observador):
           self._observadores.append(observador)

       def eliminar_observador(self, observador):
           self._observadores.remove(observador)

       def notificar(self, evento, datos):
           for obs in self._observadores:
               obs.actualizar(evento, datos)

**Modelos que Heredan de Observable:**

.. code-block:: python

   class ArtistaModel(Observable):
       def __init__(self):
           super().__init__()
           # Agregar observadores automáticamente
           self.agregar_observador(ObservadorLog())
           # Agregar cliente de logs si está disponible
           if cliente_logs.conectado:
               self.agregar_observador(ObservadorClienteLogs(cliente_logs))

       def agregar(self, data):
           artista = Artista.create(**data)
           self.notificar("artista_agregado", artista)
           return artista

**Observadores Concretos:**

1. **ObservadorLog**: Registra eventos en archivo local
2. **ObservadorClienteLogs**: Envía eventos a servidor remoto

Ventajas del Patrón Observador
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

✅ **Desacoplamiento**: Los modelos no conocen los detalles de logging
✅ **Extensibilidad**: Fácil agregar nuevos tipos de observadores
✅ **Mantenibilidad**: Cambios en logging no afectan la lógica de negocio
✅ **Reutilización**: Múltiples observadores pueden coexistir

Decoradores de Logging
----------------------

Los decoradores permiten agregar funcionalidad transversal (logging) sin modificar
el código de las funciones principales.

Decorador @log_alta
~~~~~~~~~~~~~~~~~~~

Registra automáticamente operaciones de creación (alta).

.. code-block:: python

   def log_alta(func):
       @wraps(func)
       def wrapper(self, *args, **kwargs):
           try:
               resultado = func(self, *args, **kwargs)
               # Logging exitoso
               logger.info(f"ALTA - {func.__name__}: {args} -> {resultado}")
               return resultado
           except Exception as e:
               # Logging de error
               logger.error(f"ERROR ALTA - {func.__name__}: {e}")
               raise
       return wrapper

**Uso en Controlador:**

.. code-block:: python

   class DiscoController:
       @log_alta
       def guardar_disco(self):
           # Lógica de guardar disco
           pass

Decorador @log_actualizacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Registra operaciones de modificación.

.. code-block:: python

   def log_actualizacion(func):
       @wraps(func)
       def wrapper(self, *args, **kwargs):
           try:
               resultado = func(self, *args, **kwargs)
               logger.warning(f"ACTUALIZACION - {func.__name__}: {args}")
               return resultado
           except Exception as e:
               logger.error(f"ERROR ACTUALIZACION - {func.__name__}: {e}")
               raise
       return wrapper

Decorador @log_baja
~~~~~~~~~~~~~~~~~~~

Registra operaciones de eliminación.

.. code-block:: python

   def log_baja(func):
       @wraps(func)
       def wrapper(self, *args, **kwargs):
           try:
               resultado = func(self, *args, **kwargs)
               logger.error(f"BAJA - {func.__name__}: {args}")
               return resultado
           except Exception as e:
               logger.critical(f"ERROR BAJA - {func.__name__}: {e}")
               raise
       return wrapper

Ventajas de los Decoradores
~~~~~~~~~~~~~~~~~~~~~~~~~~~

✅ **No invasivo**: No modifica la lógica de negocio
✅ **Reutilizable**: Mismo decorador para múltiples funciones
✅ **Configurable**: Fácil cambiar niveles de logging
✅ **Debugging**: Trazabilidad automática de operaciones

Patrón MVC (Model-View-Controller)
----------------------------------

La aplicación sigue estrictamente el patrón MVC para separar responsabilidades.

Model (Modelo)
~~~~~~~~~~~~~~

**Responsabilidades:**
- Gestión de datos y lógica de negocio
- Interacción con la base de datos
- Validaciones de negocio
- Notificación de cambios (patrón observador)

**Clases principales:**
- ``ArtistaModel``, ``DiscoModel``, ``CancionModel``
- Heredan de ``Observable`` para logging
- Usan Peewee ORM para persistencia

View (Vista)
~~~~~~~~~~~~

**Responsabilidades:**
- Interfaz de usuario gráfica
- Presentación de datos
- Captura de eventos del usuario
- Actualización visual

**Clases principales:**
- ``View``: Contenedor principal
- ``ArtistaFormView``, ``DiscoFormView``: Formularios
- ``ArtistaListView``, ``DiscoListView``: Listados

Controller (Controlador)
~~~~~~~~~~~~~~~~~~~~~~~~

**Responsabilidades:**
- Coordinación entre modelo y vista
- Manejo de eventos de usuario
- Lógica de aplicación
- Validaciones transversales
- Logging automático con decoradores

**Clases principales:**
- ``DiscoController``: Controlador principal
- Decoradores ``@log_alta``, ``@log_actualizacion``, ``@log_baja``

Ventajas del Patrón MVC
~~~~~~~~~~~~~~~~~~~~~~~

✅ **Separación clara**: Cada capa tiene responsabilidades definidas
✅ **Mantenibilidad**: Cambios en UI no afectan lógica de negocio
✅ **Testabilidad**: Cada capa se puede probar independientemente
✅ **Reutilización**: Modelos y controladores reutilizables

Patrón Singleton (Configuración)
--------------------------------

La configuración del sistema usa un patrón singleton implícito.

.. code-block:: python

   # config_logs.py - Configuración centralizada
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

**Ventajas:**
- Configuración centralizada
- Fácil modificación
- No instanciación accidental
- Compartida entre módulos

Manejo de Errores Robusto
-------------------------

El sistema implementa manejo de errores en múltiples niveles.

Try-Except en Operaciones Críticas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def guardar_artista(self):
       try:
           if self.artista_actual_id is None:
               artista = self.artista_model.agregar(data)
               messagebox.showinfo("Éxito", "Artista agregado correctamente")
           else:
               self.artista_model.actualizar(self.artista_actual_id, data)
               messagebox.showinfo("Éxito", "Artista actualizado correctamente")
       except Exception as e:
           logger.error(f"Error guardando artista: {e}")
           messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")

Validaciones Proactivas
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def guardar_artista(self):
       # Validación antes de procesar
       if not data["nombre"]:
           messagebox.showwarning("Aviso", "Nombre obligatorio.")
           return

       # Validación de unicidad
       if Artista.select().where(Artista.nombre == data["nombre"]).exists():
           messagebox.showwarning("Aviso", "Ya existe un artista con ese nombre.")
           return

Manejo de Conexiones TCP
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def enviar_log(self, evento, datos, nivel='INFO'):
       if not self.conectado:
           if not self.conectar():
               logger.error(f"No se puede enviar log {evento} - no conectado")
               return False

       try:
           # Envío de datos
           mensaje = json.dumps(mensaje, cls=JSONEncoderPersonalizado)
           self.socket.send(mensaje.encode('utf-8'))

           # Confirmación de recepción
           respuesta = self.socket.recv(1024).decode('utf-8')
           return True
       except Exception as e:
           logger.error(f"Error enviando log: {e}")
           self.conectado = False  # Marcar para reconexión
           return False

Beneficios de los Patrones Implementados
----------------------------------------

🔄 **Observador**: Logging automático sin acoplamiento
🎨 **Decoradores**: Funcionalidad transversal no invasiva
🏗️ **MVC**: Arquitectura clara y mantenible
⚙️ **Singleton**: Configuración centralizada
🛡️ **Manejo de Errores**: Robustez y recuperación automática

Estos patrones hacen que el código sea:
- **Extensible**: Fácil agregar nuevas funcionalidades
- **Mantenible**: Cambios localizados
- **Testable**: Separación clara de responsabilidades
- **Escalable**: Arquitectura preparada para crecimiento