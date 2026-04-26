import tkinter as tk
from model import DiscoModel, CancionModel, ArtistaModel, ObservadorLog, ObservadorClienteLogs
from cliente_logs import ClienteLogs
from controller import DiscoController
from views import View

if __name__ == "__main__":
    root = tk.Tk()
    
    # 1. Los Modelos
    model_disco = DiscoModel()
    model_cancion = CancionModel()
    model_artista = ArtistaModel()

    # 2. Agregar observador de logs local
    observador_log = ObservadorLog()
    model_artista.agregar_observador(observador_log)
    model_disco.agregar_observador(observador_log)
    model_cancion.agregar_observador(observador_log)
    
    # 3. Agregar observador de cliente logs remoto (opcional)
    cliente_logs = ClienteLogs(nombre_cliente='App-Discos')
    if cliente_logs.conectar():
        observador_cliente_logs = ObservadorClienteLogs(cliente_logs)
        model_artista.agregar_observador(observador_cliente_logs)
        model_disco.agregar_observador(observador_cliente_logs)
        model_cancion.agregar_observador(observador_cliente_logs)
        print("✓ Conectado al servidor de logs remoto")
    else:
        print("⚠ No se pudo conectar al servidor remoto - funcionando solo con logs locales")

    # 4. La Vista
    view = View(root)

    # 5. El Controlador
    controller = DiscoController(model_disco, model_cancion, model_artista, view)

    root.mainloop()
    
    # Desconectar del servidor al cerrar
    if cliente_logs.conectado:
        cliente_logs.desconectar()