"""
Módulo de Orquestación de Vistas
================================

Este módulo define la clase :class:`DiscoView`, que actúa como el contenedor 
principal y gestor de navegación de la interfaz de usuario. Implementa la barra 
de menús superior y el mecanismo para intercambiar entre diferentes pantallas.
"""

import tkinter as tk
import os
from tkinter import messagebox

# Importaciones de sub-vistas
from Views.disco_form_view import DiscoFormView
from Views.canciones_view import CancionListView
from Views.artistas_view import ArtistaListView
from Views.artistas_form_view import ArtistaFormView
from Views.home_view import HomeView
from Views.disco_list_view import DiscoListView

class DiscoView:
    """
    Gestor principal de la interfaz (Router).
    
    Esta clase no es un widget en sí, sino un orquestador que crea un contenedor 
    (:class:`tk.Frame`) donde se apilan y conmutan todas las sub-vistas del sistema.
    """

    def __init__(self, root):
        """
        Inicializa el orquestador de vistas y construye la interfaz base.

        Args:
            root (tk.Tk): Ventana principal de la aplicación.
        """
        self.root = root

        #: Color de fondo recuperado de la configuración de la raíz.
        self.bg_color = self.root.cget("bg")

        self.crear_menu()
        self.crear_widgets()
        self.mostrar_vista("home")

    def crear_menu(self):
        """
        Construye la barra de menús (MenuBar) de la ventana principal.
        
        Define los accesos rápidos para la gestión de Discos, Canciones, Artistas 
        y la sección de Ayuda.
        """
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
        """
        Inicializa el contenedor principal y registra todas las sub-vistas disponibles.
        
        Las vistas se almacenan en el diccionario ``self.vistas`` para permitir 
        un acceso rápido mediante nombres clave.
        """
        # El contenedor principal donde se intercambian las vistas
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)

        #: Diccionario que mapea nombres de vista con sus respectivas instancias de Frame.
        self.vistas = {}
        self.vistas["home"] = HomeView(self.container, self)
        self.vistas["discos"] = DiscoListView(self.container, self)
        self.vistas["artistas"] = ArtistaListView(self.container, self)
        self.vistas["formulario"] = DiscoFormView(self.container)
        self.vistas["listado_canciones"] = CancionListView(self.container, self)
        self.vistas["form_artista"] = ArtistaFormView(self.container, self)

    def mostrar_vista(self, nombre_vista):
        """
        Realiza el intercambio de pantallas (Switching).
        
        Oculta cualquier vista activa mediante ``pack_forget()`` y muestra la 
        vista solicitada expandiéndola en el contenedor principal.

        Args:
            nombre_vista (str): Clave de la vista definida en :attr:`vistas`.
        """
        for vista in self.vistas.values():
            vista.pack_forget()

        if nombre_vista in self.vistas:
            self.vistas[nombre_vista].pack(fill="both", expand=True)

    def mostrar_formulario(self, titulo="Formulario"):
        """
        Acceso directo para mostrar el formulario de discos con un título dinámico.

        Args:
            titulo (str): Título que se mostrará en la cabecera del formulario.
        """
        if hasattr(self.vistas["formulario"], 'set_titulo'):
            self.vistas["formulario"].set_titulo(titulo)
        self.mostrar_vista("formulario")

    def mostrar_formulario_artista(self):
        """Muestra la vista del formulario para creación de artistas."""
        self.mostrar_vista("form_artista")

    def mostrar_acerca_de(self):
        """
        Muestra un cuadro de diálogo con información sobre la autoría y 
        versión del software, extraída de las variables de entorno.
        """
        app_name = os.getenv("APP_NAME", "App")
        version = os.getenv("APP_VERSION", "1.0")
        author = os.getenv("APP_AUTHOR", "Author")
        
        messagebox.showinfo(
            "Acerca de", 
            f"{app_name} v{version}\n\nDesarrollado por: {author}"
        )