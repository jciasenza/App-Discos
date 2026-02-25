import tkinter as tk
import os
from tkinter import messagebox

# Importaciones de tus sub-vistas
from Views.disco_form_view import DiscoFormView
from Views.canciones_view import CancionListView
from Views.artistas_view import ArtistaListView
from Views.artistas_form_view import ArtistaFormView
from Views.home_view import HomeView
from Views.disco_list_view import DiscoListView

class DiscoView:
    def __init__(self, root):
        self.root = root

        self.bg_color = self.root.cget("bg")

        self.crear_menu()
        self.crear_widgets()
        self.mostrar_vista("home")

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        
        # --- ITEM INICIO ---
        menubar.add_command(
            label="Inicio", 
            command=lambda: self.mostrar_vista("home")
        )

        # Menú Discos
        self.menu_discos = tk.Menu(menubar, tearoff=0)
        self.menu_discos.add_command(label="Nuevo Disco", command=lambda: self.mostrar_formulario("Nuevo Disco"))
        self.menu_discos.add_command(label="Ver Listado", command=lambda: self.mostrar_vista("discos"))
        menubar.add_cascade(label="Discos", menu=self.menu_discos)

        # Menú Canciones
        self.menu_canciones = tk.Menu(menubar, tearoff=0)
        self.menu_canciones.add_command(label="Listado de Canciones", command=lambda: self.mostrar_vista("listado_canciones"))
        menubar.add_cascade(label="Canciones", menu=self.menu_canciones)

        # Menú Artistas
        self.menu_artistas = tk.Menu(menubar, tearoff=0)
        self.menu_artistas.add_command(label="Nuevo Artista", command=self.mostrar_formulario_artista)
        self.menu_artistas.add_command(label="Listado de Artistas", command=lambda: self.mostrar_vista("artistas"))
        menubar.add_cascade(label="Artistas", menu=self.menu_artistas)

        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        
        # --- ITEM SALIR ---
        menubar.add_command(label="Salir", command=self.root.quit)

        self.root.config(menu=menubar)

    def crear_widgets(self):
        # El contenedor principal donde se intercambian las vistas
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)

        # Diccionario para gestionar las vistas
        self.vistas = {}
        self.vistas["home"] = HomeView(self.container, self)
        self.vistas["discos"] = DiscoListView(self.container, self)
        self.vistas["artistas"] = ArtistaListView(self.container, self)
        self.vistas["formulario"] = DiscoFormView(self.container)
        self.vistas["listado_canciones"] = CancionListView(self.container, self)
        self.vistas["form_artista"] = ArtistaFormView(self.container, self)

    def mostrar_vista(self, nombre_vista):
        """Oculta todas las vistas y muestra la solicitada."""
        for vista in self.vistas.values():
            vista.pack_forget()

        if nombre_vista in self.vistas:
            self.vistas[nombre_vista].pack(fill="both", expand=True)

    def mostrar_formulario(self, titulo="Formulario"):
        if hasattr(self.vistas["formulario"], 'set_titulo'):
            self.vistas["formulario"].set_titulo(titulo)
        self.mostrar_vista("formulario")

    def mostrar_formulario_artista(self):
        self.mostrar_vista("form_artista")

    def mostrar_acerca_de(self):
        app_name = os.getenv("APP_NAME", "App")
        version = os.getenv("APP_VERSION", "1.0")
        author = os.getenv("APP_AUTHOR", "Author")
        
        messagebox.showinfo(
            "Acerca de", 
            f"{app_name} v{version}\n\nDesarrollado por: {author}"
        )