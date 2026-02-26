"""
Módulo del Controlador Principal
================================

Este módulo define la clase :class:`DiscoController`, que actúa como el mediador
entre la interfaz gráfica (Tkinter) y la persistencia de datos (Peewee).
Gestiona el flujo de información para artistas, discos y canciones.
"""

from tkinter import messagebox, filedialog
import tkinter as tk
from peewee import IntegrityError
from model import Artista

class DiscoController:
    """
    Controlador principal de la aplicación.
    
    Se encarga de reaccionar a los eventos de la vista, solicitar datos a los 
    modelos y actualizar la interfaz en consecuencia.
    """

    def __init__(self, model, cancion_model, artista_model, view):
        """
        Inicializa el controlador y establece los vínculos con la vista.

        Args:
            model (DiscoModel): Instancia para la gestión de discos.
            cancion_model (CancionModel): Instancia para la gestión de canciones.
            artista_model (ArtistaModel): Instancia para la gestión de artistas.
            view (View): Instancia de la fachada de la interfaz gráfica.
        """
        self.model = model
        self.cancion_model = cancion_model
        self.artista_model = artista_model
        self.view = view

        # --- ESTADOS TEMPORALES DE EDICIÓN ---
        #: ID del disco que se está editando actualmente (None si es nuevo).
        self.disco_actual_id = None
        #: ID del artista en edición.
        self.artista_actual_id = None 
        #: Ruta temporal de la imagen seleccionada para el disco/artista.
        self.imagen_actual_path = None
        #: ID de la canción que se está modificando en el formulario.
        self.cancion_en_edicion_id = None

        # Inyección de comportamiento en la vista
        self.view.al_buscar = self.ejecutar_busqueda
        
        self._configurar_botones()
        self.inicializar_datos()
        self.view.mostrar("home")

    def inicializar_datos(self):
        """
        Realiza la carga inicial de información desde la base de datos 
        hacia todos los componentes de la vista.
        """
        self.refrescar_datos_silencioso()
        artistas = self.artista_model.listar()
        self.view.lista_artistas_view.cargar_datos(artistas)
        
        todas_canciones = self.cancion_model.listar_todas_con_disco()
        self.view.canciones_view.cargar_datos(todas_canciones)

    def refrescar_datos_silencioso(self):
        """Actualiza la tabla principal de discos sin cambiar la pantalla actual."""
        self.view.limpiar_tabla()
        for d in self.model.listar():
            self.view.insertar_en_tabla(d.id, d.artista.nombre, d.titulo, d.anio, d.formato, d.portada)

    def _configurar_botones(self):
        """Vincula los métodos del controlador con los comandos de los botones en la vista."""
        # Navegación principal
        self.view.btn_nav_discos.config(command=self.refrescar)
        self.view.btn_nav_artistas.config(command=self.refrescar_artistas)
        self.view.btn_nav_canciones.config(command=self.mostrar_listado_canciones)

        # Acciones de Discos
        lista_d = self.view.lista_discos_view
        lista_d.btn_nuevo.config(command=self.nuevo)
        lista_d.btn_editar.config(command=self.editar)
        lista_d.btn_eliminar.config(command=self.eliminar)

        # Formulario de Discos
        form_d = self.view.form_view
        form_d.btn_guardar.config(command=self.guardar)
        form_d.btn_cancelar.config(command=self.refrescar)
        form_d.btn_imagen.config(command=self.seleccionar_imagen)
        form_d.btn_agregar_cancion.config(command=self.agregar_cancion)
        form_d.btn_editar_cancion.config(command=self.preparar_edicion_cancion)
        form_d.btn_eliminar_cancion.config(command=self.eliminar_cancion)

        # Acciones de Artistas
        lista_a = self.view.lista_artistas_view
        lista_a.btn_agregar.config(command=self.nuevo_artista)
        lista_a.btn_editar.config(command=self.editar_artista)
        lista_a.btn_eliminar.config(command=self.eliminar_artista_accion)
    
        # Eventos de búsqueda (Triggers)
        lista_a.buscar_var.trace_add("write", lambda *args: self.ejecutar_busqueda_artistas())
        self.view.canciones_view.buscar_var.trace_add(
            "write", lambda *args: self.ejecutar_busqueda_canciones()
        )

        # Formulario de Artistas
        form_a = self.view.form_artista_view
        form_a.btn_guardar.config(command=self.guardar_artista)
        form_a.btn_cancelar.config(command=self.refrescar_artistas)
        form_a.btn_foto.config(command=self.seleccionar_foto_artista)

    # --- LÓGICA DE ARTISTAS ---

    def refrescar_artistas(self):
        """Recarga la lista de artistas y cambia la pantalla a la vista de artistas."""
        artistas = self.artista_model.listar()
        self.view.lista_artistas_view.cargar_datos(artistas)
        self.view.mostrar("artistas")

    def guardar_artista(self):
        """
        Extrae datos del formulario de artistas y los persiste en la DB.
        Maneja errores de duplicados (IntegrityError).
        """
        form = self.view.form_artista_view
        data = {
            "nombre": form.nombre_var.get().strip(),
            "tipo": form.tipo_var.get(),
            "info": form.txt_info.get("1.0", tk.END).strip(),
            "foto": form.foto_path
        }
        if not data["nombre"]:
            messagebox.showwarning("Aviso", "Nombre obligatorio.")
            return
        try:
            if self.artista_actual_id is None:
                self.artista_model.agregar(data)
            else:
                self.artista_model.actualizar(self.artista_actual_id, data)
            messagebox.showinfo("Éxito", "Artista guardado.")
            self.refrescar_artistas()
        except IntegrityError:
            messagebox.showerror("Error", "El artista ya existe.")

    # --- LÓGICA DE DISCOS ---

    def editar(self):
        """
        Prepara el formulario de discos con los datos de un disco seleccionado
        para su modificación.
        """
        disco_id = self.view.lista_discos_view.obtener_id_seleccionado()
        if not disco_id:
            messagebox.showwarning("Aviso", "Seleccione un disco de la lista.")
            return
        
        disco = self.model.obtener(disco_id)
        if disco is None:
            messagebox.showerror("Error", f"No se encontró el disco con ID: {disco_id}")
            return

        self.disco_actual_id = disco.id
        self.imagen_actual_path = disco.portada
        self.actualizar_dropdown_artistas()
        self.view.form_view.cargar_datos(disco)
        self.cargar_canciones()
        self.view.mostrar("form", "Editar Disco")

    def guardar(self):
        """
        Valida y guarda los datos de un disco. 
        Si el disco es nuevo, recupera el ID generado para permitir añadir canciones.
        """
        nombre_artista = self.view.form_view.artista_var.get().strip()
        if nombre_artista == "Artista" or not nombre_artista:
            messagebox.showwarning("Error", "Debe seleccionar un artista.")
            return

        artista_obj = Artista.get_or_none(Artista.nombre == nombre_artista)
        if not artista_obj:
            messagebox.showwarning("Error", "Artista no encontrado.")
            return
        
        data = {
            "artista": artista_obj.id,
            "titulo": self.view.form_view.titulo_var.get().strip(),
            "anio": self.view.form_view.anio_var.get().strip(),
            "formato": self.view.form_view.formato_var.get(),
            "portada": self.imagen_actual_path
        }
        try:
            if self.disco_actual_id is None:
                nuevo_disco = self.model.agregar(data)
                self.disco_actual_id = nuevo_disco.id
            else:
                self.model.actualizar(self.disco_actual_id, data)
            
            messagebox.showinfo("Éxito", "Disco guardado correctamente.")
            self.refrescar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    # --- LÓGICA DE CANCIONES ---

    def agregar_cancion(self):
        """
        Añade una canción al disco actual. 
        Requiere que el disco haya sido guardado previamente para tener un ID de referencia.
        """
        if not self.disco_actual_id:
            messagebox.showwarning("Aviso", "Primero guarde el disco.")
            return
        
        titulo = self.view.form_view.input_cancion.get().strip()
        numero_str = self.view.form_view.numero_pista_var.get().strip()
        duracion = self.view.form_view.duracion_var.get().strip()

        if not titulo or not numero_str:
            messagebox.showwarning("Aviso", "N° y Título obligatorios.")
            return

        try:
            data = {
                "numero_pista": int(numero_str),
                "titulo": titulo,
                "duracion": duracion if duracion else "N/A",
                "disco": self.disco_actual_id
            }
            if self.cancion_en_edicion_id:
                self.cancion_model.actualizar(self.cancion_en_edicion_id, data)
                self.cancion_en_edicion_id = None
                self.view.form_view.btn_agregar_cancion.config(text="✔")
            else:
                self.cancion_model.agregar(data)
            
            self.cargar_canciones()
            todas = self.cancion_model.listar_todas_con_disco()
            self.view.canciones_view.cargar_datos(todas)
            
            self.view.form_view.numero_pista_var.set("")
            self.view.form_view.input_cancion.delete(0, "end")
            self.view.form_view.duracion_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Error en canción: {str(e)}")

    def cargar_canciones(self):
        """Refresca visualmente el Listbox de canciones dentro del formulario de discos."""
        self.view.form_view.lista_canciones.delete(0, tk.END)
        if not self.disco_actual_id: return
        canciones = self.cancion_model.listar_por_disco(self.disco_actual_id)
        for c in canciones:
            texto = f"{c.numero_pista:02d} - {c.titulo} ({c.duracion})"
            self.view.form_view.lista_canciones.insert(tk.END, texto)