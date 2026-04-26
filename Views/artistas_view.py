import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class ArtistaListView(tk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent, bg="#d9d9d9")
        self.controlador = controlador
        self.imagenes_refs = [] 
        self.crear_widgets()

    def crear_widgets(self):
        # 1. CABECERA
        self.header_frame = tk.Frame(self, bg="#d9d9d9")
        self.header_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_titulo = tk.Label(
            self.header_frame, text="Listado de Artistas", 
            font=("sans-serif", 14, "bold"), bg="#d9d9d9"
        )
        self.lbl_titulo.pack(side="left")

        self.search_frame = tk.Frame(self.header_frame, bg="#d9d9d9")
        self.search_frame.pack(side="right")

        tk.Label(self.search_frame, text="Buscar:", bg="#d9d9d9").pack(side="left")
        self.buscar_var = tk.StringVar()
        self.entry_buscar = tk.Entry(self.search_frame, textvariable=self.buscar_var)
        self.entry_buscar.pack(side="left", padx=5)

        # 2. ESTILO
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=65, font=("Segoe UI", 11), background="white")
        style.configure("Treeview.Heading", background="#eeeeee", font=("Segoe UI", 10, "bold"), relief="ridge")

        # 3. TREEVIEW
        cols = ("nombre", "tipo", "id_art")
        self.tree = ttk.Treeview(self, columns=cols, show="tree headings", height=15)

        self.tree.heading("#0", text="FOTO")
        self.tree.column("#0", width=100, anchor="center")
        self.tree.heading("nombre", text="ARTISTA / BANDA")
        self.tree.column("nombre", width=300, anchor="w")
        self.tree.heading("tipo", text="TIPO")
        self.tree.column("tipo", width=120, anchor="center")
        self.tree.heading("id_art", text="ID")
        self.tree.column("id_art", width=80, anchor="center")

        # Scrollbar integrada
        scrolly = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrolly.set)
        self.tree.pack(side="top", fill="both", expand=True, padx=20)
        scrolly.pack(in_=self.tree, side="right", fill="y")

        # 4. BOTONES DE ACCIÓN
        self.frame_acciones = tk.Frame(self, bg="#d9d9d9")
        self.frame_acciones.pack(side="bottom", fill="x", pady=20, padx=20)

        self.btn_agregar = tk.Button(
            self.frame_acciones, text="Nuevo Artista", bg="#28a745", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8, 
            cursor="hand2", command=self.on_nuevo
        )
        self.btn_agregar.pack(side="left", padx=5)

        self.btn_editar = tk.Button(
            self.frame_acciones, text="Editar Seleccionado", bg="#17a2b8", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8, 
            cursor="hand2", command=self.on_editar
        )
        self.btn_editar.pack(side="left", padx=5)

        self.btn_eliminar = tk.Button(
            self.frame_acciones, text="Eliminar", bg="#dc3545", fg="white", 
            font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8, 
            cursor="hand2", command=self.on_eliminar
        )
        self.btn_eliminar.pack(side="right", padx=5)
        self.tree.bind("<Double-1>", lambda e: self.on_editar())

    # --- MÉTODOS DE ACCIÓN (CALLBACKS) ---

    def on_nuevo(self):
        if self.controlador and hasattr(self.controlador, 'nuevo_artista'):
            self.controlador.nuevo_artista()

    def on_editar(self):
        id_sel = self.obtener_seleccionado()
        if id_sel:
            if self.controlador and hasattr(self.controlador, 'editar_artista'):
                self.controlador.editar_artista()
        else:
            messagebox.showwarning("Atención", "Por favor, selecciona un artista de la lista.")

    def on_eliminar(self):
        id_sel = self.obtener_seleccionado()
        if id_sel:
            respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar al artista #{id_sel}?\nEsta acción no se puede deshacer.")
            if respuesta:
                if self.controlador and hasattr(self.controlador, 'eliminar_artista_accion'):
                    self.controlador.eliminar_artista_accion()
        else:
            messagebox.showwarning("Atención", "Selecciona el artista que deseas eliminar.")

    def obtener_seleccionado(self):
        item = self.tree.selection()
        if item:
            return int(item[0])
        return None

    def cargar_datos(self, artistas):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.imagenes_refs = [] 

        for a in artistas:
            foto_tk = "" 
            try:
                ruta = getattr(a, 'foto', None)
                if ruta and os.path.exists(ruta):
                    img = Image.open(ruta)
                    img.thumbnail((55, 55)) # Escalamiento proporcional
                    foto_tk = ImageTk.PhotoImage(img)
                    self.imagenes_refs.append(foto_tk) 
            except Exception:
                foto_tk = ""

            self.tree.insert("", "end", iid=str(a.id), text="", image=foto_tk, values=(
                a.nombre.upper(), 
                a.tipo,
                f"{a.id}"
            ))