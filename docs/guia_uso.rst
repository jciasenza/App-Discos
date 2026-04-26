Guía de Uso - App Discos
=========================

Esta guía explica cómo usar todas las funcionalidades de la aplicación,
incluyendo el sistema de logs cliente-servidor y las nuevas características.

Instalación y Configuración
---------------------------

Requisitos del Sistema
~~~~~~~~~~~~~~~~~~~~~~

- Python 3.8 o superior
- Tkinter (incluido en Python estándar)
- Pillow (PIL) para manejo de imágenes
- Peewee ORM

Instalación de Dependencias
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install peewee pillow

Estructura del Proyecto
~~~~~~~~~~~~~~~~~~~~~~~

::

   App Discos/
   ├── main.py                 # Punto de entrada
   ├── model.py                # Modelos y lógica de negocio
   ├── controller.py           # Controladores y lógica de aplicación
   ├── views.py                # Interfaz gráfica
   ├── validations.py          # Validaciones
   ├── cliente_logs.py         # Cliente de logs TCP
   ├── servidor_logs.py        # Servidor de logs TCP
   ├── config_logs.py          # Configuración del sistema de logs
   ├── docs/                   # Documentación Sphinx
   ├── Views/                  # Vistas específicas
   ├── img/                    # Imágenes y recursos
   └── discos.db               # Base de datos SQLite

Uso Básico de la Aplicación
---------------------------

Inicio de la Aplicación
~~~~~~~~~~~~~~~~~~~~~~~

**Modo Local (Recomendado para desarrollo):**

.. code-block:: bash

   python main.py

La aplicación iniciará y registrará logs automáticamente en ``app_discos.log``.

**Modo Cliente-Servidor (Para producción):**

.. code-block:: bash

   # Terminal 1: Iniciar servidor de logs
   python servidor_logs.py

   # Terminal 2: Iniciar aplicación
   python main.py

La aplicación detectará automáticamente el servidor y enviará logs centralizados.

Interfaz de Usuario
-------------------

La aplicación cuenta con una interfaz gráfica intuitiva dividida en secciones:

Gestión de Artistas
~~~~~~~~~~~~~~~~~~~

**Agregar Artista:**

1. Navegar a la pestaña "Artistas"
2. Hacer clic en "Nuevo Artista"
3. Completar los campos:
   - **Nombre**: Nombre del artista o banda (obligatorio)
   - **Tipo**: Solista, Banda o Dúo
   - **Biografía**: Información adicional
   - **Foto**: Seleccionar imagen (opcional)
4. Hacer clic en "Guardar"

**Editar Artista:**

1. Seleccionar artista de la lista
2. Hacer clic en "Editar Artista"
3. Modificar los campos deseados
4. Hacer clic en "Guardar"

**Eliminar Artista:**

1. Seleccionar artista de la lista
2. Hacer clic en "Eliminar Artista"
3. Confirmar la eliminación

Gestión de Discos
~~~~~~~~~~~~~~~~~

**Agregar Disco:**

1. Navegar a la pestaña "Discos"
2. Seleccionar artista de la lista
3. Hacer clic en "Nuevo Disco"
4. Completar los campos:
   - **Artista**: Seleccionar de la lista desplegable
   - **Título**: Nombre del disco (obligatorio)
   - **Año**: Año de lanzamiento
   - **Formato**: CD, Vinilo, Digital, etc.
   - **Portada**: Seleccionar imagen (opcional)
5. Hacer clic en "Guardar"

**Editar Disco:**

1. Seleccionar disco de la lista
2. Hacer clic en "Editar Disco"
3. Modificar los campos deseados
4. Hacer clic en "Guardar"

**Eliminar Disco:**

1. Seleccionar disco de la lista
2. Hacer clic en "Eliminar Disco"
3. Confirmar la eliminación

Gestión de Canciones
~~~~~~~~~~~~~~~~~~~~

**Agregar Canción:**

1. Seleccionar un disco
2. En la pestaña "Canciones", hacer clic en "Nueva Canción"
3. Completar los campos:
   - **Número de pista**: Orden en el disco
   - **Título**: Nombre de la canción
   - **Duración**: Tiempo de reproducción
4. Hacer clic en "Guardar"

Sistema de Logs
---------------

La aplicación incluye un sistema de logging avanzado con múltiples opciones.

Logs Locales
~~~~~~~~~~~~

**Archivo:** ``app_discos.log``

Siempre activo, registra todas las operaciones localmente:

::

   2026-04-26 10:30:45 - INFO - Evento: artista_agregado | Datos: <Artista object>
   2026-04-26 10:31:12 - WARNING - Evento: disco_actualizado | Datos: {'id': 1, 'data': {'anio': 1969}}
   2026-04-26 10:32:00 - ERROR - Evento: artista_eliminado | Datos: 1

Logs Centralizados (Servidor)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Archivos:**
- ``servidor_logs.log``: Logs del servidor central
- ``cliente_logs.log``: Logs del cliente

Para activar el modo centralizado:

1. Iniciar el servidor:

   .. code-block:: bash

      python servidor_logs.py

2. Iniciar la aplicación normalmente:

   .. code-block:: bash

      python main.py

La aplicación detectará automáticamente el servidor.

Configuración del Sistema de Logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Archivo:** ``config_logs.py``

Personalizar configuración:

.. code-block:: python

   # Cambiar puerto del servidor
   SERVIDOR_CONFIG = {
       'puerto': 8080,  # Cambiar de 5000 a 8080
   }

   # Cambiar nombre del cliente
   CLIENTE_CONFIG = {
       'nombre_cliente': 'Mi-Discoteca-Personal',
   }

Pruebas del Sistema
-------------------

Scripts de Prueba Incluidos
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Prueba del Cliente-Servidor:**

.. code-block:: bash

   # Terminal 1
   python servidor_logs.py

   # Terminal 2
   python prueba_cliente_servidor.py

**Prueba de Serialización JSON:**

.. code-block:: bash

   python prueba_serializacion.py

Verificación de Logs
~~~~~~~~~~~~~~~~~~~~

**Windows PowerShell:**

.. code-block:: powershell

   # Ver logs locales
   Get-Content app_discos.log -Tail 10

   # Ver logs del servidor
   Get-Content servidor_logs.log -Tail 10

   # Monitoreo en tiempo real
   Get-Content app_discos.log -Tail 10 -Wait

Solución de Problemas
---------------------

Problema: "No se puede establecer una conexión"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Síntoma:** ``AttributeError: [WinError 10061] No se puede establecer una conexión``

**Solución:** El servidor de logs no está ejecutándose.

.. code-block:: bash

   # Iniciar servidor en otra terminal
   python servidor_logs.py

   # Luego iniciar la aplicación
   python main.py

Problema: "Object of type set is not JSON serializable"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solución:** Ya está solucionado en la versión actual. El sistema incluye
un ``JSONEncoderPersonalizado`` que maneja automáticamente tipos complejos.

Problema: "AttributeError: 'ArtistaFormView' object has no attribute 'foto_path'"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solución:** Ya está solucionado. El controlador usa ``getattr(form, 'foto_path', None)``
para manejar casos donde no se ha seleccionado imagen.

Problema: Aplicación no inicia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Verificar sintaxis:**

.. code-block:: bash

   python -m py_compile main.py model.py controller.py

**Verificar dependencias:**

.. code-block:: bash

   pip list | findstr "peewee\|Pillow"

Problema: Logs no aparecen
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Verificar archivos:**

.. code-block:: bash

   dir *.log

**Verificar permisos de escritura:**

.. code-block:: bash

   # El directorio debe tener permisos de escritura
   icacls .

Documentación Técnica
---------------------

Generar Documentación
~~~~~~~~~~~~~~~~~~~~~

La documentación se genera con Sphinx:

.. code-block:: bash

   cd docs
   make html  # Windows
   # o
   make.bat html  # Windows alternativo

Abrir documentación:

.. code-block:: bash

   start docs/_build/html/index.html

Estructura de la Base de Datos
------------------------------

La aplicación usa SQLite con Peewee ORM:

**Tabla Artista:**

.. code-block:: sql

   CREATE TABLE artista (
       id INTEGER PRIMARY KEY,
       nombre VARCHAR(255) UNIQUE NOT NULL,
       tipo VARCHAR(255),
       info TEXT,
       foto VARCHAR(255)
   );

**Tabla Discos:**

.. code-block:: sql

   CREATE TABLE discos (
       id INTEGER PRIMARY KEY,
       artista_id INTEGER REFERENCES artista(id) ON DELETE CASCADE,
       titulo VARCHAR(255) NOT NULL,
       anio INTEGER,
       formato VARCHAR(255),
       portada VARCHAR(255)
   );

**Tabla Cancion:**

.. code-block:: sql

   CREATE TABLE cancion (
       id INTEGER PRIMARY KEY,
       numero_pista INTEGER NOT NULL,
       titulo VARCHAR(255) NOT NULL,
       duracion VARCHAR(255),
       disco_id INTEGER REFERENCES discos(id) ON DELETE CASCADE,
       UNIQUE(numero_pista, disco_id)
   );

API de Desarrollo
-----------------

Para desarrolladores que quieran extender la aplicación:

**Agregar Nuevo Observador:**

.. code-block:: python

   class MiObservador:
       def actualizar(self, evento, datos):
           # Mi lógica personalizada
           print(f"Evento personalizado: {evento}")

   # Agregar al modelo
   modelo.agregar_observador(MiObservador())

**Crear Nuevo Decorador:**

.. code-block:: python

   def mi_decorador(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           # Lógica antes
           resultado = func(*args, **kwargs)
           # Lógica después
           return resultado
       return wrapper

**Extender Validaciones:**

.. code-block:: python

   # En validations.py
   def validar_mi_campo(valor):
       if not valor:
           raise ValidationError("Campo obligatorio")
       return valor.strip()

Consideraciones de Producción
-----------------------------

**Configuración para Producción:**

1. **Cambiar puerto del servidor** en ``config_logs.py``
2. **Configurar logging rotativo** para archivos grandes
3. **Implementar autenticación** en el servidor TCP
4. **Usar HTTPS** para comunicaciones seguras
5. **Configurar monitoreo** de logs centralizados

**Recomendaciones de Despliegue:**

- Ejecutar servidor de logs como servicio del sistema
- Configurar backups automáticos de logs
- Implementar rotación de logs para evitar archivos muy grandes
- Monitorear uso de disco y conexiones TCP

**Seguridad:**

- Validar todas las entradas de usuario
- Sanitizar datos antes de logging
- Limitar conexiones concurrentes al servidor
- Implementar timeouts apropiados

Esta guía cubre todas las funcionalidades implementadas. Para más detalles técnicos,
consulta la documentación completa generada con Sphinx.