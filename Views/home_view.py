"""
Módulo de la Vista de Inicio
============================

Este módulo define la pantalla principal de bienvenida y navegación del sistema.
Proporciona el acceso centralizado a los módulos de discos, artistas y canciones.
"""

import tkinter as tk
from tkinter import ttk

class HomeView(tk.Frame):
    """
    Clase que representa el menú principal de la aplicación.
    
    Hereda de :class:`tk.Frame` y organiza los botones de navegación 
    utilizando un diseño centrado y efectos visuales interactivos.
    """

    def __init__(self, parent, controlador):
        """
        Inicializa la vista de inicio.

        Args:
            parent (tk.Widget): El contenedor padre (usualmente el contenedor de vistas).
            controlador: Referencia al objeto que gestiona la lógica de navegación.
        """
        super().__init__(parent, bg="#d9d9d9")
        self.controlador = controlador
        
        #: Diccionario con parámetros estéticos comunes para los botones de la home.
        self.btn_params = {
            "font": ("Segoe UI", 12, "bold"),
            "width": 25,
            "height": 2,
            "relief": "flat",
            "fg": "white",
            "cursor": "hand2"
        }
        
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y posiciona los elementos visuales en la pantalla.
        
        Incluye el título principal, los botones de acceso a módulos y el botón de salida.
        """
        main_frame = tk.Frame(self, bg="#d9d9d9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 1. TÍTULO
        tk.Label(
            main_frame, text="SISTEMA DE GESTIÓN MUSICAL", 
            font=("Segoe UI", 24, "bold"), bg="#d9d9d9", fg="#2c3e50"
        ).pack(pady=(0, 40))

        # 2. BOTONES DE GESTIÓN
        #: Botón para acceder al listado de discos.
        self.btn_discos = self.crear_boton_hover(
            main_frame, "💿 GESTIONAR DISCOS", "#34495e", "#4b6584", 
            lambda: self.controlador.mostrar_vista("discos")
        )
        
        #: Botón para acceder al listado de artistas.
        self.btn_artistas = self.crear_boton_hover(
            main_frame, "👤 GESTIONAR ARTISTAS", "#34495e", "#4b6584", 
            lambda: self.controlador.mostrar_vista("artistas")
        )
        
        #: Botón para acceder al listado global de canciones.
        self.btn_canciones = self.crear_boton_hover(
            main_frame, "🎵 EXPLORAR CANCIONES", "#34495e", "#4b6584", 
            lambda: self.controlador.mostrar_vista("listado_canciones")
        )

        # 3. BOTÓN SALIR
        #: Botón para cerrar la aplicación.
        self.btn_salir = self.crear_boton_hover(
            main_frame, "🛑 SALIR DEL SISTEMA", "#dc3545", "#ff4757", 
            self.quit
        )
        self.btn_salir.pack(pady=(30, 0))

    def crear_boton_hover(self, parent, texto, color_base, color_hover, comando):
        """
        Crea un botón personalizado con efectos de cambio de color al pasar el ratón.

        Args:
            parent (tk.Widget): Contenedor donde se alojará el botón.
            texto (str): Texto que mostrará el botón.
            color_base (str): Color de fondo normal (hex).
            color_hover (str): Color de fondo cuando el mouse está encima (hex).
            comando (callable): Función a ejecutar al hacer clic.

        Returns:
            tk.Button: El objeto botón creado.
        """
        btn = tk.Button(parent, text=texto, bg=color_base, command=comando, **self.btn_params)
        btn.pack(pady=10)

        # Eventos para el efecto Hover
        btn.bind("<Enter>", lambda e: btn.config(bg=color_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=color_base))
        
        return btn