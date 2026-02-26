"""
Módulo de la Vista de Listado de Discos
======================================

Este módulo define :class:`DiscoListView`, un componente encargado de mostrar 
la colección de discos en formato de tabla (Treeview), incluyendo las portadas.
"""

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class DiscoListView(tk.Frame):
    """
    Vista que presenta los discos en un componente Treeview.
    
    Hereda de :class:`tk.Frame`. Permite la visualización, selección y 
    búsqueda de discos, además de mostrar miniaturas de las portadas.
    """

    def __init__(self, parent, controlador):
        """
        Inicializa la vista de listado.

        Args:
            parent (tk.Widget): El contenedor padre.
            controlador: Referencia al controlador de la lógica de negocio.
        """
        super().__init__(parent, bg="#d9d9d9")
        self.controlador = controlador
        
        #: Diccionario para mantener la referencia a las imágenes (evita el Garbage Collector).
        self.imagenes_tabla = {}
        
        self.crear_widgets()

    def crear_widgets(self):
        """
        Construye la interfaz del listado.
        
        Divide la vista en tres áreas: Superior (Título y Búsqueda), 
        Central (Tabla Treeview) y Inferior (Acciones CRUD).
        """
        # 1. FRAME SUPERIOR (Cabecera y Buscador)
        top_frame = tk.Frame(self, bg="#d9d9d9")
        top_frame.pack(fill="x", side="top", padx=20, pady=10)

        tk.Label(top_frame, text="Listado de Discos", font=("Segoe UI", 18, "bold"), bg="#d9d9d9").pack(side="left")
        
        search_frame = tk.Frame(top_frame, bg="#d9d9d9")
        search_frame.pack(side="right")
        tk.Label(search_frame, text="Buscar:", bg="#d9d9d9").pack(side="left")
        
        #: Widget de entrada para el motor de búsqueda en tiempo real.
        self.entry_buscar = ttk.Entry(search_frame, width=25)
        self.entry_buscar.pack(side="left", padx=5)

        # 2. FRAME DE BOTONES (Acciones)
        self.btns_frame = tk.Frame(self, bg="#d9d9d9")
        self.btns_frame.pack(fill="x", side="bottom", pady=20, padx=20)

        self.btn_nuevo = tk.Button(
            self.btns_frame, text="Nuevo Disco", bg="#28a745", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8
        )
        self.btn_nuevo.pack(side="left", padx=5)

        self.btn_editar = tk.Button(
            self.btns_frame, text="Editar Seleccionado", bg="#17a2b8", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8
        )
        self.btn_editar.pack(side="left", padx=5)

        self.btn_eliminar = tk.Button(
            self.btns_frame, text="Eliminar", bg="#dc3545", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8
        )
        self.btn_eliminar.pack(side="right", padx=5)
        
        # 3. TREEVIEW (Tabla de datos)
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20)

        cols = ("artista", "titulo", "anio", "formato")
        #: Componente de tabla para mostrar los registros.
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, height=10)
        
        # Configuración de estilos y columnas
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", rowheight=60, font=("Segoe UI", 10))
        
        self.tree.heading("#0", text="PORTADA")
        self.tree.column("#0", width=90, anchor="center")
        self.tree.heading("artista", text="ARTISTA")
        self.tree.column("artista", width=200, anchor="center")
        self.tree.heading("titulo", text="TÍTULO")
        self.tree.column("titulo", width=200, anchor="center")
        self.tree.heading("anio", text="AÑO")
        self.tree.column("anio", width=80, anchor="center")
        self.tree.heading("formato", text="FORMATO")
        self.tree.column("formato", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True)

    def limpiar_tabla(self):
        """
        Elimina todos los registros del Treeview y vacía la caché de imágenes.
        """
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.imagenes_tabla.clear()

    def insertar_en_tabla(self, id, artista, titulo, anio, formato, portada):
        """
        Inserta una fila en la tabla, procesando la imagen de portada si existe.

        Args:
            id (int): ID de la base de datos (usado como iid del Treeview).
            artista (str): Nombre del artista.
            titulo (str): Título del álbum.
            anio (int): Año de lanzamiento.
            formato (str): Formato físico/digital.
            portada (str): Ruta al archivo de imagen en el disco.
        """
        imagen = ""
        if portada and os.path.exists(portada):
            try:
                img = Image.open(portada)
                img = img.resize((50, 50))
                photo = ImageTk.PhotoImage(img)
                # Guardamos la referencia para que no se pierda al salir de la función
                self.imagenes_tabla[id] = photo
                imagen = photo
            except Exception as e: 
                print(f"Error cargando imagen: {e}")
                imagen = ""

        self.tree.insert(
            "", 
            "end", 
            iid=str(id), 
            text="", 
            image=imagen, 
            values=(artista, titulo, anio, formato)
        )
        
    def obtener_id_seleccionado(self):
        """
        Retorna el ID del registro seleccionado por el usuario.

        Returns:
            str or None: El identificador único de la fila seleccionada o None.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            return None
        return seleccion[0]