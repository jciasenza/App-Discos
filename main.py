"""
Módulo Principal
================

Este módulo es el punto de entrada de la aplicación. Se encarga de inicializar
la interfaz gráfica, los modelos de datos y conectar todo a través del controlador.
"""

import tkinter as tk
from model import DiscoModel, CancionModel, ArtistaModel
from controller import DiscoController
from views import View

def main():
    """
    Inicializa la aplicación siguiendo el patrón MVC.
    
    1. Crea la ventana raíz de Tkinter.
    2. Instancia los modelos de Disco, Canción y Artista.
    3. Inicializa la interfaz de usuario (Vista).
    4. Vincula los modelos y la vista mediante el Controlador.
    5. Arranca el bucle principal de la interfaz.
    """
    root = tk.Tk()
    root.title("Gestor de Discos")

    # 1. Los Modelos
    model_disco = DiscoModel()
    model_cancion = CancionModel()
    model_artista = ArtistaModel()

    # 2. La Vista
    view = View(root)

    # 3. El Controlador
    controller = DiscoController(model_disco, model_cancion, model_artista, view)

    # Inicio de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()