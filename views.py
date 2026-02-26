"""
Módulo de la Vista Principal (Fachada)
=======================================
"""
"""
Este módulo define la clase :class:`View`, que actúa como el orquestador central 
de la interfaz gráfica. Centraliza el acceso a las sub-vistas (artistas, discos, canciones)
y expone los widgets necesarios para que el controlador pueda vincular eventos.
"""

import os
import tkinter as tk
from dotenv import load_dotenv
from Views.disco_view import DiscoView

# Carga las variables de entorno para la configuración de la UI
load_dotenv()

class View():
    """
    Clase principal de la interfaz de usuario.
    
    Esta clase implementa el patrón Facade para simplificar la comunicación
    entre el Controlador y las múltiples sub-vistas del sistema.
    """

    def __init__(self, root):
        """
        Inicializa la vista principal y configura las sub-vistas.

        Args:
            root (tk.Tk): La instancia principal de Tkinter.
        """
        self.root = root
        
        # --- 1. CONFIGURACIÓN DE LA VENTANA (MVC) ---
        self.configurar_ventana()
        
        # --- 2. INSTANCIAMOS EL ORQUESTADOR PRINCIPAL ---
        self.main_view = DiscoView(root)
        
        # --- 3. REFERENCIAS DIRECTAS A LAS SUB-VISTAS ---
        #: Referencia a la vista de inicio.
        self.home_view = self.main_view.vistas["home"]
        #: Referencia a la lista de discos.
        self.lista_discos_view = self.main_view.vistas["discos"]
        #: Referencia a la lista de artistas.
        self.lista_artistas_view = self.main_view.vistas["artistas"]
        #: Referencia al formulario de discos.
        self.form_view = self.main_view.vistas["formulario"]
        #: Referencia al listado de canciones.
        self.canciones_view = self.main_view.vistas["listado_canciones"]
        #: Referencia al formulario de artistas.
        self.form_artista_view = self.main_view.vistas["form_artista"]

        # --- 4. EXPOSICIÓN DE WIDGETS PARA EL CONTROLADOR ---
        self.btn_nav_discos = self.home_view.btn_discos
        self.btn_nav_artistas = self.home_view.btn_artistas
        self.btn_nav_canciones = self.home_view.btn_canciones
        
        self.btn_nuevo_disco = self.lista_discos_view.btn_nuevo
        self.btn_editar_disco = self.lista_discos_view.btn_editar
        self.btn_eliminar_disco = self.lista_discos_view.btn_eliminar
        
        self.entry_buscar_disco = self.lista_discos_view.entry_buscar
        
        # --- 5. VARIABLE DE BÚSQUEDA ---
        #: Variable de control de Tkinter para el motor de búsqueda.
        self.buscar_var = tk.StringVar()
        self.entry_buscar_disco.configure(textvariable=self.buscar_var)
        self.buscar_var.trace_add("write", lambda *args: self.al_buscar())

    def configurar_ventana(self):
        """
        Configura los parámetros estéticos de la ventana principal.
        
        Extrae el título, versión y colores desde el archivo de configuración 
        ``.env``. Si no existen, utiliza valores por defecto.
        """
        app_name = os.getenv("APP_NAME", "Gestión Musical")
        version = os.getenv("APP_VERSION", "1.0")
        bg_color = os.getenv("APP_BG_COLOR", "#d9d9d9")
        
        self.root.title(f"{app_name} - v{version}")
        self.root.state('zoomed')
        self.root.configure(bg=bg_color)

        # Manejo del Icono
        icon_path = os.path.join(os.path.dirname(__file__), "icono.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

    def al_buscar(self):
        """
        Método 'placeholder' para la acción de búsqueda.
        
        .. note::
           Este método está diseñado para ser sobreescrito por el controlador
           durante la inicialización de la app.
        """
        pass

    def mostrar(self, nombre, titulo_form=None):
        """
        Gestiona el cambio de pantallas en la aplicación.

        Args:
            nombre (str): Clave de la vista a mostrar (e.g., 'home', 'lista', 'form').
            titulo_form (str, optional): Título dinámico si la vista es un formulario.
        """
        mapa = {
            "home": "home",
            "lista": "discos",
            "artistas": "artistas",
            "form": "formulario",
            "canciones": "listado_canciones",
            "form_artista": "form_artista"
        }
        
        vista_destino = mapa.get(nombre, "home")

        if nombre == "form" and titulo_form:
            if hasattr(self.form_view, 'set_titulo'):
                self.form_view.set_titulo(titulo_form)
            
        self.main_view.mostrar_vista(vista_destino)

    # --- MÉTODOS PUENTE PARA DISCOS ---
    def limpiar_tabla(self): 
        """Elimina todos los elementos visuales de la tabla de discos."""
        self.lista_discos_view.limpiar_tabla()
        
    def insertar_en_tabla(self, *args): 
        """Inserta una nueva fila en la tabla de discos."""
        self.lista_discos_view.insertar_en_tabla(*args)
        
    def obtener_id_seleccionado(self): 
        """Retorna el ID del disco seleccionado en la interfaz."""
        return self.lista_discos_view.obtener_id_seleccionado()

    # --- MÉTODOS PUENTE PARA ARTISTAS Y CANCIONES ---
    def cargar_datos_artistas(self, artistas):
        """
        Actualiza visualmente la lista de artistas.
        
        Args:
            artistas (list): Lista de objetos de tipo Artista.
        """
        self.lista_artistas_view.cargar_datos(artistas)

    def cargar_datos_canciones(self, canciones):
        """
        Actualiza visualmente la lista de canciones.
        
        Args:
            canciones (list): Lista de objetos de tipo Cancion.
        """
        self.canciones_view.cargar_datos(canciones)