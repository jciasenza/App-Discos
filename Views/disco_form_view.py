import tkinter as tk
from tkinter import ttk, StringVar, Listbox, Scrollbar
from PIL import Image, ImageTk

class DiscoFormView(ttk.Frame):

    COLOR_BACKGROUND = "#f0f0f0"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # --- Configuración de Estilos ---
        style = ttk.Style()
        style.configure("Main.TFrame", background=self.COLOR_BACKGROUND)
        style.configure("TLabel", background=self.COLOR_BACKGROUND) 
        
        self.configure(style="Main.TFrame")
        style.configure("Add.TButton", foreground="green", font=("Segoe UI", 12, "bold"))
        style.configure("Edit.TButton", foreground="blue", font=("Segoe UI", 12))
        style.configure("Delete.TButton", foreground="red", font=("Segoe UI", 12, "bold"))

        self.img_tk = None
        self.crear_widgets()

    def crear_widgets(self):
        # --- Título Superior ---
        self.form_title = tk.Label(
            self, text="Nuevo Disco", font=("Segoe UI", 20, "bold"),
            bg=self.COLOR_BACKGROUND, fg="#222"
        )
        self.form_title.pack(pady=(20, 30))

        # --- Contenedor Principal ---
        main_container = ttk.Frame(self, style="Main.TFrame")
        main_container.pack(expand=True, fill="both", padx=20)

        # 1. IZQUIERDA: Portada
        col_izquierda = ttk.Frame(main_container, style="Main.TFrame")
        col_izquierda.grid(row=0, column=0, padx=30, sticky="n")

        self.contenedor_img = tk.Frame(col_izquierda, width=300, height=300, bg="#dcdcdc")
        self.contenedor_img.pack(pady=10)
        self.contenedor_img.pack_propagate(False)
        
        self.label_imagen = tk.Label(
            self.contenedor_img, text="Sin Imagen", bg="#dcdcdc",
            font=("Segoe UI", 10, "italic")
        )
        self.label_imagen.pack(expand=True, fill="both")
        
        self.btn_imagen = ttk.Button(col_izquierda, text="Seleccionar Imagen")
        self.btn_imagen.pack(fill="x", ipady=5)

        # 2. CENTRO: Formulario de Datos del Disco
        col_central = ttk.Frame(main_container, style="Main.TFrame")
        col_central.grid(row=0, column=1, padx=30, sticky="n")

        #: Variables de control (StringVar) para los campos del disco.
        self.id_var = StringVar(value="-")
        self.artista_var = StringVar(value="Artista")
        self.titulo_var = StringVar()
        self.anio_var = StringVar()
        self.formato_var = StringVar(value="CD")

        lbl_font = ("Segoe UI", 11, "bold")
        entry_width = 30

        # --- Construcción dinámica de campos ---
        ttk.Label(col_central, text="ID:", font=lbl_font).grid(row=0, column=0, sticky="e", pady=10)
        ttk.Entry(col_central, textvariable=self.id_var, width=entry_width, font=("Segoe UI", 11), state="readonly").grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(col_central, text="Artista:", font=lbl_font).grid(row=1, column=0, sticky="e", pady=10)
        self.combo_artista = ttk.Combobox(
            col_central, 
            textvariable=self.artista_var, 
            state="readonly", 
            width=28, 
            font=("Segoe UI", 11)
        )
        self.combo_artista.grid(row=1, column=1, pady=10, padx=10)

        campos = [
            ("Título:", self.titulo_var, 2),
            ("Año:", self.anio_var, 3)
        ]
        for label, var, fila in campos:
            ttk.Label(col_central, text=label, font=lbl_font).grid(row=fila, column=0, sticky="e", pady=10)
            ttk.Entry(col_central, textvariable=var, width=entry_width, font=("Segoe UI", 11)).grid(row=fila, column=1, pady=10, padx=10)

        ttk.Label(col_central, text="Formato:", font=lbl_font).grid(row=4, column=0, sticky="e", pady=10)
        self.combo_formato = ttk.Combobox(col_central, textvariable=self.formato_var, 
                                          values=["CD", "Vinilo", "Cassette", "Digital"],
                                          state="readonly", width=28, font=("Segoe UI", 11))
        self.combo_formato.grid(row=4, column=1, pady=10, padx=10)

        # 3. DERECHA: Gestión de Canciones
        col_derecha = ttk.Frame(main_container, style="Main.TFrame")
        col_derecha.grid(row=0, column=2, padx=30, sticky="n")

        ttk.Label(col_derecha, text="Canciones", font=lbl_font).pack(anchor="w")

        # Sub-frame para entrada de pistas
        input_song_frame = ttk.Frame(col_derecha, style="Main.TFrame")
        input_song_frame.pack(fill="x", pady=5)

        self.numero_pista_var = StringVar()
        ttk.Label(input_song_frame, text="N°:").pack(side="left")
        ttk.Entry(input_song_frame, textvariable=self.numero_pista_var, width=4).pack(side="left", padx=2)
        
        ttk.Label(input_song_frame, text="Título:").pack(side="left")
        self.input_cancion = ttk.Entry(input_song_frame, width=15)
        self.input_cancion.pack(side="left", padx=2)

        self.duracion_var = StringVar()
        ttk.Label(input_song_frame, text="Duración:").pack(side="left")
        ttk.Entry(input_song_frame, textvariable=self.duracion_var, width=6).pack(side="left", padx=2)

        self.btn_agregar_cancion = ttk.Button(input_song_frame, text="✔", width=2, style="Add.TButton")
        self.btn_agregar_cancion.pack(side="left", padx=5)

        # --- Lista de Canciones con Scrollbar ---
        list_container = ttk.Frame(col_derecha, style="Main.TFrame")
        list_container.pack(pady=10, fill="both", expand=True)

        self.scrollbar = Scrollbar(list_container, orient="vertical")
        self.lista_canciones = Listbox(
            list_container, width=35, height=10, font=("Segoe UI", 10),
            yscrollcommand=self.scrollbar.set,
            relief="flat", highlightthickness=1, highlightcolor="#ddd"
        )
        self.scrollbar.config(command=self.lista_canciones.yview)
        self.lista_canciones.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="left", fill="y")

        # Botones laterales para editar/eliminar de la lista
        acciones_lista_frame = ttk.Frame(list_container, style="Main.TFrame")
        acciones_lista_frame.pack(side="left", padx=5, fill="y")

        self.btn_editar_cancion = ttk.Button(acciones_lista_frame, text="✎", width=2, style="Edit.TButton")
        self.btn_editar_cancion.pack(pady=2)

        self.btn_eliminar_cancion = ttk.Button(acciones_lista_frame, text="✖", width=2, style="Delete.TButton")
        self.btn_eliminar_cancion.pack(pady=2)

        # --- Botones Inferiores del Formulario ---
        botones_frame = ttk.Frame(self, style="Main.TFrame")
        botones_frame.pack(pady=40, side="bottom")

        self.btn_guardar = ttk.Button(botones_frame, text="Guardar", style="Add.TButton")
        self.btn_guardar.pack(side="left", padx=20, ipadx=20, ipady=5)

        self.btn_cancelar = ttk.Button(botones_frame, text="Cancelar", style="Delete.TButton")
        self.btn_cancelar.pack(side="left", padx=20, ipadx=20, ipady=5)

    # ------------------ MÉTODOS DE SOPORTE ------------------

    def limpiar_campos(self):
        """Restablece todos los campos del formulario a sus valores iniciales."""
        self.id_var.set("-")
        self.artista_var.set("Artista")
        self.titulo_var.set("")
        self.anio_var.set("")
        self.formato_var.set("CD")
        self.numero_pista_var.set("")
        self.duracion_var.set("")
        self.input_cancion.delete(0, "end")
        self.lista_canciones.delete(0, "end")
        self.label_imagen.config(image="", text="Sin Imagen")
        self.img_tk = None

    def cargar_datos(self, disco):
        self.id_var.set(str(disco.id))
        if disco.artista:
            self.artista_var.set(disco.artista.nombre)
        else:
            self.artista_var.set("Artista")
        self.titulo_var.set(disco.titulo)
        self.anio_var.set(disco.anio)
        self.formato_var.set(disco.formato)
        if hasattr(disco, 'portada') and disco.portada:
            self.set_imagen(disco.portada)

    def set_titulo(self, texto):
        self.form_title.config(text=texto)

    def set_imagen(self, path):
        if not path:
            self.label_imagen.config(image="", text="Sin Imagen")
            self.img_tk = None
            return
        try:
            img = Image.open(path)
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            self.label_imagen.config(image=self.img_tk, text="")
        except:
            self.label_imagen.config(image="", text="Error Imagen")