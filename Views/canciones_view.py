"""
Módulo de Exploración de Canciones
==================================

Este módulo define :class:`CancionListView`, una vista diseñada para la 
visualización global de todas las pistas almacenadas en la base de datos, 
permitiendo búsquedas transversales por artista, disco o título.
"""

import os
import tkinter as tk
from tkinter import ttk

class CancionListView(tk.Frame):
    """
    Vista de listado general de canciones.
    
    Hereda de :class:`tk.Frame`. A diferencia de la vista de discos, esta tabla 
    se enfoca en el detalle de las pistas individuales y su procedencia, 
    utilizando un estilo visual compacto.
    """

    def __init__(self, parent, controlador):
        """
        Inicializa la vista de canciones.

        Args:
            parent (tk.Widget): Contenedor padre.
            controlador: Referencia al orquestador de la aplicación.
        """
        super().__init__(parent, bg="#d9d9d9")
        self.controlador = controlador
        self.crear_widgets()

    def crear_widgets(self):
        """
        Configura la interfaz, incluyendo el buscador dinámico y la tabla 
        con soporte para desplazamiento vertical (Scrollbar).
        """
        # 1. TÍTULO Y BUSCADOR
        top_frame = tk.Frame(self, bg="#d9d9d9")
        top_frame.pack(fill="x", side="top", padx=20, pady=10)

        tk.Label(
            top_frame, text="Listado de Canciones", 
            font=("Segoe UI", 18, "bold"), bg="#d9d9d9"
        ).pack(side="left")

        search_frame = tk.Frame(top_frame, bg="#d9d9d9")
        search_frame.pack(side="right")
        
        tk.Label(search_frame, text="Buscar:", bg="#d9d9d9").pack(side="left")

        #: Variable vinculada al campo de búsqueda para filtrado en tiempo real.
        self.buscar_var = tk.StringVar()
        self.entry_buscar = ttk.Entry(search_frame, width=25, textvariable=self.buscar_var)
        self.entry_buscar.pack(side="left", padx=5)

        # 2. ESTILO PERSONALIZADO
        style = ttk.Style()
        style.configure("Canciones.Treeview", font=("Segoe UI", 10), rowheight=28)
        style.configure("Canciones.Treeview.Heading", font=("Segoe UI", 10, "bold"))

        # 3. CONTENEDOR DE TABLA CON SCROLLBAR
        self.tree_frame = tk.Frame(self, bg="#d9d9d9")
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=5)

        columnas = ("artista", "disco", "n", "titulo", "duracion")
        
        #: Componente Treeview configurado para mostrar solo encabezados (sin columna de iconos).
        self.tree = ttk.Treeview(
            self.tree_frame, 
            columns=columnas, 
            show="headings", 
            height=15,
            style="Canciones.Treeview"
        )

        # AGREGAR SCROLLBAR VERTICAL
        #: Barra de desplazamiento vinculada al movimiento vertical del Treeview.
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Definir encabezados y anchos
        self.tree.heading("artista", text="ARTISTA")
        self.tree.heading("disco", text="DISCO")
        self.tree.heading("n", text="TRACK")
        self.tree.heading("titulo", text="TÍTULO")
        self.tree.heading("duracion", text="DURACIÓN")

        self.tree.column("n", width=60, anchor="center")
        self.tree.column("duracion", width=90, anchor="center")
        self.tree.column("artista", width=180, anchor="w")
        self.tree.column("disco", width=180, anchor="w")
        self.tree.column("titulo", width=300, anchor="w")
            
    def cargar_datos(self, lista_canciones):
        """
        Puebla el Treeview con los objetos de tipo Cancion proporcionados.
        
        Realiza una navegación de objetos para extraer el nombre del artista
        y el título del disco, manejando casos donde las relaciones sean nulas.

        Args:
            lista_canciones (list): Una lista de instancias del modelo Cancion.
        """
        # 1. Limpiar la tabla antes de cargar
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 2. Insertar los nuevos datos
        for c in lista_canciones:
            try:
                # Navegación segura de relaciones: Cancion -> Disco -> Artista
                nombre_artista = c.disco.artista.nombre if c.disco and c.disco.artista else "Desconocido"
                titulo_disco = c.disco.titulo if c.disco else "Sin Disco"
                duracion_text = c.duracion if c.duracion else "N/A"
                
                self.tree.insert("", "end", values=(
                    nombre_artista,
                    titulo_disco,
                    f"{c.numero_pista:02d}",
                    c.titulo,
                    duracion_text
                ))
            except AttributeError as e:
                print(f"Error al cargar canción {getattr(c, 'id', 'S/D')}: {e}")