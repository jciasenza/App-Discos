Módulo de Vistas
==================

.. automodule:: views
   :members:
   :undoc-members:
   :show-inheritance:
Arquitectura de Vistas
----------------------

El módulo implementa la interfaz gráfica usando Tkinter con arquitectura MVC.

HomeView
~~~~~~~~

Vista principal que coordina todas las demás vistas.

.. code-block:: python

   class HomeView:
       def __init__(self, root, controlador):
           self.root = root
           self.controlador = controlador
           self.controlador.set_view(self)

           # Crear frames para diferentes secciones
           self.frame_artistas = ArtistasView(self.root, self.controlador)
           self.frame_discos = DiscosView(self.root, self.controlador)
           self.frame_canciones = CancionesView(self.root, self.controlador)

           # Configurar navegación
           self.setup_navigation()

**Responsabilidades:**
- Coordinar entre diferentes vistas
- Gestionar navegación entre secciones
- Configurar ventana principal
- Manejar eventos de cierre

Vista de Artistas
-----------------

ArtistasView
~~~~~~~~~~~~

Vista para gestión de artistas.

**Componentes principales:**

- **Lista de artistas:** Treeview con columnas (ID, Nombre, Tipo)
- **Formulario de artista:** Campos para nombre, tipo, info, foto
- **Botones de acción:** Nuevo, Editar, Eliminar, Buscar

**Métodos clave:**

mostrar_artistas()
^^^^^^^^^^^^^^^^^^

Muestra la lista de artistas en el Treeview.

.. code-block:: python

   def mostrar_artistas(self):
       # Limpiar lista actual
       for item in self.tree_artistas.get_children():
           self.tree_artistas.delete(item)

       # Obtener artistas del controlador
       artistas = self.controlador.listar_artistas()

       # Agregar a Treeview
       for artista in artistas:
           self.tree_artistas.insert('', 'end', values=(
               artista.id,
               artista.nombre,
               artista.tipo or ''
           ))

nuevo_artista()
^^^^^^^^^^^^^^^

Abre el formulario para crear un nuevo artista.

editar_artista()
^^^^^^^^^^^^^^^^

Carga datos del artista seleccionado en el formulario para edición.

guardar_artista()
^^^^^^^^^^^^^^^^^

Guarda los datos del formulario (crear o actualizar).

eliminar_artista()
^^^^^^^^^^^^^^^^^^

Elimina el artista seleccionado después de confirmación.

buscar_artistas()
^^^^^^^^^^^^^^^^^

Filtra la lista de artistas según el texto de búsqueda.

Vista de Discos
---------------

DiscosView
~~~~~~~~~~

Vista para gestión de discos.

**Componentes:**

- **Lista de discos:** Treeview con (ID, Título, Artista, Año, Formato)
- **Formulario de disco:** Campos para título, artista, año, formato, portada
- **Botones:** Nuevo, Editar, Eliminar, Buscar, Ver Canciones

**Funcionalidades especiales:**

- **Selector de artista:** Combobox con lista de artistas disponibles
- **Vista de canciones:** Botón para ver canciones del disco seleccionado
- **Validación de artista:** Verifica que el artista seleccionado existe

Vista de Canciones
------------------

CancionesView
~~~~~~~~~~~~~

Vista para gestión de canciones.

**Componentes:**

- **Lista de canciones:** Treeview con (ID, Pista, Título, Duración, Disco)
- **Formulario de canción:** Campos para número de pista, título, duración, disco
- **Filtros:** Por disco específico o todas las canciones

**Características:**

- **Modo contextual:** Puede mostrar solo canciones de un disco o todas
- **Validación de pistas:** Evita números de pista duplicados en el mismo disco
- **Selector de disco:** Combobox con discos disponibles

Formularios Especializados
-------------------------

ArtistasFormView
~~~~~~~~~~~~~~~~

Vista especializada para el formulario de artistas.

**Campos del formulario:**

- ``nombre``: Entry obligatorio
- ``tipo``: Combobox con opciones ['Solista', 'Banda', 'Dúo']
- ``info``: Text para información biográfica
- ``foto``: Entry con botón para seleccionar archivo

**Métodos:**

seleccionar_foto()
^^^^^^^^^^^^^^^^^^

Abre diálogo para seleccionar archivo de imagen.

.. code-block:: python

   def seleccionar_foto(self):
       filename = filedialog.askopenfilename(
           title="Seleccionar foto",
           filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.gif *.bmp")]
       )
       if filename:
           self.entry_foto.delete(0, tk.END)
           self.entry_foto.insert(0, filename)

validar_formulario()
^^^^^^^^^^^^^^^^^^^^

Valida que todos los campos requeridos estén completos.

DiscoFormView
~~~~~~~~~~~~~

Vista especializada para el formulario de discos.

**Campos:**

- ``titulo``: Entry obligatorio
- ``artista``: Combobox con artistas disponibles
- ``anio``: Entry numérico opcional
- ``formato``: Combobox con formatos disponibles
- ``portada``: Entry con selector de archivo

DiscoListView
~~~~~~~~~~~~~

Vista de lista especializada para discos.

**Características:**

- **Columnas expandibles:** Ajusta automáticamente al contenido
- **Ordenamiento:** Click en headers para ordenar
- **Selección múltiple:** Para operaciones masivas
- **Contexto menú:** Menú derecho con opciones

Navegación y Layout
-------------------

setup_navigation()
~~~~~~~~~~~~~~~~~~

Configura el sistema de navegación entre vistas.

.. code-block:: python

   def setup_navigation(self):
       # Crear botones de navegación
       self.btn_artistas = tk.Button(self.root, text="Artistas",
                                   command=self.mostrar_artistas)
       self.btn_discos = tk.Button(self.root, text="Discos",
                                 command=self.mostrar_discos)
       self.btn_canciones = tk.Button(self.root, text="Canciones",
                                    command=self.mostrar_canciones)

       # Posicionar botones
       self.btn_artistas.pack(side=tk.TOP, fill=tk.X)
       self.btn_discos.pack(side=tk.TOP, fill=tk.X)
       self.btn_canciones.pack(side=tk.TOP, fill=tk.X)

**Navegación implementada:**
- Botones en la parte superior
- Ocultar/mostrar frames según la selección
- Mantener estado entre navegaciones

Manejo de Eventos
-----------------

**Eventos del Treeview:**

- ``<<TreeviewSelect>>``: Selección de elemento
- ``<Double-1>``: Doble click para editar
- ``<Button-3>``: Menú contextual

**Eventos de formulario:**

- ``<Return>``: Enter en campos para guardar
- ``<FocusOut>``: Validación al salir de campos
- ``<KeyRelease>``: Búsqueda en tiempo real

Validación en Interfaz
-----------------------

**Validaciones implementadas:**

1. **Campos requeridos:** Resaltados en rojo si están vacíos
2. **Tipos de datos:** Validación numérica para años y pistas
3. **Referencias foráneas:** Verificación de existencia de artistas/discos
4. **Unicidad:** Verificación de nombres únicos y pistas únicas
5. **Formatos:** Validación de duraciones y rutas de archivo

**Feedback al usuario:**

- **Colores:** Verde para válido, rojo para inválido
- **Mensajes:** Labels con mensajes de error descriptivos
- **Estados:** Habilitar/deshabilitar botones según validez

Gestión de Imágenes
-------------------

**Funcionalidades de imagen:**

- **Selección de archivo:** Diálogos nativos del sistema
- **Vista previa:** Miniaturas en la interfaz (futuro)
- **Validación:** Verificación de existencia y formato
- **Rutas relativas:** Conversión a rutas relativas al proyecto

**Formatos soportados:**
- JPG, JPEG, PNG, GIF, BMP

Manejo de Errores
-----------------

**Estrategias de manejo:**

1. **Try-catch en operaciones:** Captura errores de base de datos
2. **Mensajes de error:** Diálogos informativos para el usuario
3. **Logging:** Registro de errores en sistema de logs
4. **Recuperación:** Estado consistente después de errores

**Ejemplo:**

.. code-block:: python

   try:
       self.controlador.agregar_artista(data)
       messagebox.showinfo("Éxito", "Artista agregado correctamente")
       self.mostrar_artistas()  # Actualizar lista
   except Exception as e:
       logging.error(f"Error agregando artista: {e}")
       messagebox.showerror("Error", f"No se pudo agregar el artista: {str(e)}")

Consideraciones de UI/UX
------------------------

**Principios aplicados:**

1. **Intuitivo:** Layouts lógicos y consistentes
2. **Responsive:** Ajuste automático a diferentes tamaños
3. **Accesible:** Labels descriptivos, tab order correcto
4. **Feedback:** Indicadores visuales de estado y progreso

**Buenas prácticas:**

- **Navegación clara:** Siempre visible dónde está el usuario
- **Estados consistentes:** Botones habilitados/deshabilitados apropiadamente
- **Confirmaciones:** Diálogos para operaciones destructivas
- **Atajos de teclado:** Soporte para usuarios avanzados

Integración con Controlador
---------------------------

**Patrón de comunicación:**

.. code-block:: python

   # Vista notifica al controlador
   def guardar_artista(self):
       data = self.obtener_datos_formulario()
       if self.controlador.agregar_artista(data):
           self.limpiar_formulario()
           self.mostrar_artistas()

   # Controlador actualiza la vista
   def actualizar_vista_artistas(self):
       if self.view:
           artistas = self.listar_artistas()
           self.view.actualizar_lista_artistas(artistas)

**Beneficios:**
- Separación clara de responsabilidades
- Fácil testing de lógica de negocio
- Reutilización de vistas con diferentes controladores
- Mantenibilidad del código

Rendimiento y Optimización
--------------------------

**Optimizaciones implementadas:**

1. **Lazy loading:** Cargar datos solo cuando necesario
2. **Paginación:** Para listas grandes (futuro)
3. **Cache:** Mantener datos en memoria cuando posible
4. **Actualizaciones selectivas:** Refrescar solo lo necesario

**Recomendaciones:**

- Implementar virtualización para listas muy grandes
- Usar hilos para operaciones que puedan bloquear la UI
- Optimizar consultas de base de datos
- Considerar compresión para imágenes grandes

Extensibilidad
--------------

**Arquitectura extensible:**

- **Vistas modulares:** Fácil agregar nuevas secciones
- **Formularios genéricos:** Base común para diferentes entidades
- **Eventos desacoplados:** Sistema de eventos para comunicación
- **Configuración externa:** Layouts y estilos configurables

**Posibles extensiones:**

- **Temas:** Soporte para diferentes temas visuales
- **Plugins:** Sistema de plugins para funcionalidades adicionales
- **Multi-ventana:** Soporte para múltiples ventanas
- **Internacionalización:** Soporte para múltiples idiomas