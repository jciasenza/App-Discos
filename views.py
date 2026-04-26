import os
import tkinter as tk
from dotenv import load_dotenv
from Views.disco_view import DiscoView

# Carga las variables de entorno para la configuración de la UI
load_dotenv()

class View():
    def __init__(self, root):
        self.root = root
        
        # --- 1. CONFIGURACIÓN DE LA VENTANA (MVC) ---
        self.configurar_ventana()
        
        # --- 2. INSTANCIAMOS EL ORQUESTADOR PRINCIPAL ---
        self.main_view = DiscoView(root)
        
        # --- 3. REFERENCIAS DIRECTAS A LAS SUB-VISTAS ---
        self.home_view = self.main_view.vistas["home"]
        self.lista_discos_view = self.main_view.vistas["discos"]
        self.lista_artistas_view = self.main_view.vistas["artistas"]
        self.form_view = self.main_view.vistas["formulario"]
        self.canciones_view = self.main_view.vistas["listado_canciones"]
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
        self.buscar_var = tk.StringVar()
        self.entry_buscar_disco.configure(textvariable=self.buscar_var)
        self.buscar_var.trace_add("write", lambda *args: self.al_buscar())

    def configurar_ventana(self):
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
        pass

    def mostrar(self, nombre, titulo_form=None):
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
        self.lista_discos_view.limpiar_tabla()
        
    def insertar_en_tabla(self, *args): 
        self.lista_discos_view.insertar_en_tabla(*args)
        
    def obtener_id_seleccionado(self): 
        return self.lista_discos_view.obtener_id_seleccionado()

    # --- MÉTODOS PUENTE PARA ARTISTAS Y CANCIONES ---
    def cargar_datos_artistas(self, artistas):
        self.lista_artistas_view.cargar_datos(artistas)

    def cargar_datos_canciones(self, canciones):
        self.canciones_view.cargar_datos(canciones)