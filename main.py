import tkinter as tk
from model import DiscoModel, CancionModel, ArtistaModel, ObservadorLog
from controller import DiscoController
from views import View

if __name__ == "__main__":
    root = tk.Tk()
    
    # 1. Los Modelos
    model_disco = DiscoModel()
    model_cancion = CancionModel()
    model_artista = ArtistaModel()

    # Agregar observador de logs a los modelos
    observador_log = ObservadorLog()
    model_artista.agregar_observador(observador_log)
    model_disco.agregar_observador(observador_log)
    model_cancion.agregar_observador(observador_log)

    # 2. La Vista
    view = View(root)

    # 3. El Controlador
    controller = DiscoController(model_disco, model_cancion, model_artista, view)

    root.mainloop()