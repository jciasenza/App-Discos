import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class DiscoListView(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#d9d9d9")
        self.controlador = controlador
        self.imagenes_tabla = {}
        self.crear_widgets()

    def crear_widgets(self):
        # 1. FRAME SUPERIOR
        top_frame = tk.Frame(self, bg="#d9d9d9")
        top_frame.pack(fill="x", side="top", padx=20, pady=10)

        tk.Label(top_frame, text="Listado de Discos", font=("Segoe UI", 18, "bold"), bg="#d9d9d9").pack(side="left")
        
        search_frame = tk.Frame(top_frame, bg="#d9d9d9")
        search_frame.pack(side="right")
        tk.Label(search_frame, text="Buscar:", bg="#d9d9d9").pack(side="left")
        self.entry_buscar = ttk.Entry(search_frame, width=25)
        self.entry_buscar.pack(side="left", padx=5)

        # 2. FRAME DE BOTONES
        self.btns_frame = tk.Frame(self, bg="#d9d9d9")
        self.btns_frame.pack(fill="x", side="bottom", pady=20, padx=20)

        # Botón Nuevo
        self.btn_nuevo = tk.Button(
            self.btns_frame, text="Nuevo Disco", bg="#28a745", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8
        )
        self.btn_nuevo.pack(side="left", padx=5)

        # Botón Editar
        self.btn_editar = tk.Button(
            self.btns_frame, text="Editar Seleccionado", bg="#17a2b8", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8
        )
        self.btn_editar.pack(side="left", padx=5)

        # Botón Eliminar
        self.btn_eliminar = tk.Button(
            self.btns_frame, text="Eliminar", bg="#dc3545", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8
        )
        self.btn_eliminar.pack(side="right", padx=5)
        
        # 3. TREEVIEW
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20)

        cols = ("artista", "titulo", "anio", "formato")
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, height=10)
        
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
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.imagenes_tabla.clear()

    def insertar_en_tabla(self, id, artista, titulo, anio, formato, portada):
        imagen = ""
        if portada and os.path.exists(portada):
            try:
                img = Image.open(portada)
                img = img.resize((50, 50))
                photo = ImageTk.PhotoImage(img)
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
        """Retorna el ID del disco seleccionado (usando el iid de la fila)"""
        seleccion = self.tree.selection()
        if not seleccion:
            return None
        return seleccion[0]