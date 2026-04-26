import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ArtistaFormView(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#d9d9d9")
        self.controlador = controlador
        self.crear_widgets()

    def crear_widgets(self):
        # 1. TÍTULO SUPERIOR
        tk.Label(
            self, text="Ficha del Artista", 
            font=("Segoe UI", 18, "bold"), bg="#d9d9d9"
        ).pack(pady=(40, 30))

        # 2. CONTENEDOR MAESTRO (Diseño de 3 columnas)
        master_container = tk.Frame(self, bg="#d9d9d9")
        master_container.pack(expand=True, padx=50)

        # --- COLUMNA 1: IMAGEN DE PERFIL ---
        self.frame_izquierda = tk.Frame(master_container, bg="#d9d9d9")
        self.frame_izquierda.grid(row=0, column=0, padx=(0, 30), sticky="n")

        self.container_foto = tk.Frame(self.frame_izquierda, bg="#bbb", width=250, height=250)
        self.container_foto.pack()
        self.container_foto.pack_propagate(False) # Evita que el frame colapse al tamaño de la etiqueta

        self.lbl_foto = tk.Label(
            self.container_foto, text="Sin Imagen", 
            font=("Segoe UI", 12, "italic"),
            bg="#bbb", bd=0, highlightthickness=0
        )
        self.lbl_foto.pack(expand=True, fill="both")

        self.btn_foto = ttk.Button(self.frame_izquierda, text="Seleccionar Imagen")
        self.btn_foto.pack(pady=15, fill="x")

        # --- COLUMNA 2: FORMULARIO DE DATOS ---
        self.frame_datos = tk.Frame(master_container, bg="#d9d9d9")
        self.frame_datos.grid(row=0, column=1, padx=30, sticky="n")

        estilo_lbl = {"bg": "#d9d9d9", "font": ("Segoe UI", 10, "bold")}
        
        # ID (Solo lectura)
        tk.Label(self.frame_datos, text="ID:", **estilo_lbl).pack(anchor="w", pady=(0, 5))
        self.id_var = tk.StringVar(value="-")
        ttk.Entry(self.frame_datos, textvariable=self.id_var, width=35, state="readonly", font=("Segoe UI", 11)).pack(pady=(0, 20))

        # Nombre
        tk.Label(self.frame_datos, text="Nombre del Artista / Banda:", **estilo_lbl).pack(anchor="w", pady=(0, 5))
        self.nombre_var = tk.StringVar()
        ttk.Entry(self.frame_datos, textvariable=self.nombre_var, width=35, font=("Segoe UI", 11)).pack(pady=(0, 20))

        # Tipo (Combobox)
        tk.Label(self.frame_datos, text="Tipo de Artista:", **estilo_lbl).pack(anchor="w", pady=(0, 5))
        self.tipo_var = tk.StringVar(value="Solista")
        self.combo_tipo = ttk.Combobox(self.frame_datos, textvariable=self.tipo_var, 
                                     values=["Solista", "Banda", "Dúo"], 
                                     state="readonly", width=33, font=("Segoe UI", 10))
        self.combo_tipo.pack()

        # --- COLUMNA 3: ÁREA DE BIOGRAFÍA ---
        self.frame_info = tk.Frame(master_container, bg="#d9d9d9")
        self.frame_info.grid(row=0, column=2, padx=(30, 0), sticky="n")

        tk.Label(self.frame_info, text="Biografia / Informacion:", **estilo_lbl).pack(anchor="w", pady=(0, 5))
        
        text_scroll_frame = tk.Frame(self.frame_info, bg="#d9d9d9")
        text_scroll_frame.pack()

        self.txt_info = tk.Text(text_scroll_frame, width=35, height=18, font=("Segoe UI", 10), 
                                relief="flat", highlightthickness=1, highlightbackground="#ccc")
        
        scroll_y = ttk.Scrollbar(text_scroll_frame, orient="vertical", command=self.txt_info.yview)
        self.txt_info.configure(yscrollcommand=scroll_y.set)

        self.txt_info.pack(side="left")
        scroll_y.pack(side="right", fill="y")

        # 3. BOTONES INFERIORES
        self.frame_btns = tk.Frame(self, bg="#d9d9d9")
        self.frame_btns.pack(side="bottom", pady=40)

        self.btn_guardar = ttk.Button(self.frame_btns, text="Guardar", style="Add.TButton")
        self.btn_guardar.pack(side="left", padx=15, ipadx=20, ipady=5) 
        
        self.btn_cancelar = ttk.Button(self.frame_btns, text="Cancelar", style="Delete.TButton")
        self.btn_cancelar.pack(side="left", padx=15, ipadx=20, ipady=5)

    def set_foto(self, path):
        if path and os.path.exists(path):
            img = Image.open(path)
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(img)
            self.lbl_foto.config(image=foto, text="")
            self.lbl_foto.image = foto
            self.foto_path = path
        else:
            self.lbl_foto.config(image="", text="Sin Imagen", font=("Segoe UI", 12, "italic"))
            self.foto_path = None

    def cargar_datos(self, artista):
        self.id_var.set(str(artista.id))
        self.nombre_var.set(artista.nombre)
        self.tipo_var.set(artista.tipo)
        self.txt_info.delete("1.0", tk.END)
        self.txt_info.insert("1.0", artista.info if artista.info else "")

        self.foto_path = artista.foto
        self.set_foto(artista.foto)

    def limpiar_campos(self):
        self.id_var.set("-")
        self.nombre_var.set("")
        self.tipo_var.set("Solista")
        self.txt_info.delete("1.0", tk.END)
        self.set_foto(None)