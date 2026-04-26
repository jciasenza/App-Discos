from tkinter import messagebox, filedialog
import tkinter as tk
from peewee import IntegrityError
from model import Artista

def log_alta(func):
    def wrapper(self, *args, **kwargs):
        es_alta = self.disco_actual_id is None
        if es_alta:
            print("ALTA de disco en proceso...")
        resultado = func(self, *args, **kwargs)
        if es_alta:
            print("Disco creado correctamente")
        return resultado
    return wrapper


def log_actualizacion(func):
    def wrapper(self, *args, **kwargs):
        es_update = self.disco_actual_id is not None
        if es_update:
            print(f"Actualizando disco ID {self.disco_actual_id}...")
        resultado = func(self, *args, **kwargs)
        if es_update:
            print(f"Disco ID {self.disco_actual_id} actualizado")
        return resultado
    return wrapper

def log_eliminacion(func):
    def wrapper(self, *args, **kwargs):
        disco_id = self.view.lista_discos_view.obtener_id_seleccionado()
        if not disco_id:
            return func(self, *args, **kwargs)
        print(f"Eliminando disco ID {disco_id}...")
        resultado = func(self, *args, **kwargs)
        print(f"Disco ID {disco_id} eliminado")
        return resultado
    return wrapper

class DiscoController:
    def __init__(self, model, cancion_model, artista_model, view):
        self.model = model
        self.cancion_model = cancion_model
        self.artista_model = artista_model
        self.view = view

        # --- ESTADOS TEMPORALES DE EDICIÓN ---
        #: ID del disco que se está editando actualmente (None si es nuevo).
        self.disco_actual_id = None
        #: ID del artista en edición.
        self.artista_actual_id = None 
        #: Ruta temporal de la imagen seleccionada para el disco/artista.
        self.imagen_actual_path = None
        #: ID de la canción que se está modificando en el formulario.
        self.cancion_en_edicion_id = None

        # Inyección de comportamiento en la vista (Eventos globales)
        self.view.al_buscar = self.ejecutar_busqueda
        
        self._configurar_botones()
        self.inicializar_datos()
        self.view.mostrar("home")

    def inicializar_datos(self):
        self.refrescar_datos_silencioso()
        artistas = self.artista_model.listar()
        self.view.lista_artistas_view.cargar_datos(artistas)
        
        # Sincroniza el listado general de canciones
        todas_canciones = self.cancion_model.listar_todas_con_disco()
        self.view.canciones_view.cargar_datos(todas_canciones)

    def refrescar_datos_silencioso(self):
        self.view.limpiar_tabla()
        for d in self.model.listar():
            self.view.insertar_en_tabla(d.id, d.artista.nombre, d.titulo, d.anio, d.formato, d.portada)

    def _configurar_botones(self):
        # Navegación principal
        self.view.btn_nav_discos.config(command=self.refrescar)
        self.view.btn_nav_artistas.config(command=self.refrescar_artistas)
        self.view.btn_nav_canciones.config(command=self.mostrar_listado_canciones)

        # Acciones de la Lista de Discos
        lista_d = self.view.lista_discos_view
        lista_d.btn_nuevo.config(command=self.nuevo)
        lista_d.btn_editar.config(command=self.editar)
        lista_d.btn_eliminar.config(command=self.eliminar)

        # Acciones del Formulario de Discos
        form_d = self.view.form_view
        form_d.btn_guardar.config(command=self.guardar)
        form_d.btn_cancelar.config(command=self.refrescar)
        form_d.btn_imagen.config(command=self.seleccionar_imagen)
        
        form_d.btn_agregar_cancion.config(command=self.agregar_cancion)
        form_d.btn_editar_cancion.config(command=self.preparar_edicion_cancion)
        form_d.btn_eliminar_cancion.config(command=self.eliminar_cancion)

        # Acciones de la Lista de Artistas
        lista_a = self.view.lista_artistas_view
        lista_a.btn_agregar.config(command=self.nuevo_artista)
        lista_a.btn_editar.config(command=self.editar_artista)
        lista_a.btn_eliminar.config(command=self.eliminar_artista_accion)
    
        # Eventos de búsqueda en tiempo real (Traces)
        lista_a.buscar_var.trace_add("write", lambda *args: self.ejecutar_busqueda_artistas())
        self.view.canciones_view.buscar_var.trace_add(
            "write", lambda *args: self.ejecutar_busqueda_canciones()
        )

        # Acciones del Formulario de Artistas
        form_a = self.view.form_artista_view
        form_a.btn_guardar.config(command=self.guardar_artista)
        form_a.btn_cancelar.config(command=self.refrescar_artistas)
        form_a.btn_foto.config(command=self.seleccionar_foto_artista)

    # --- LÓGICA DE ARTISTAS ---

    def refrescar_artistas(self):
        artistas = self.artista_model.listar()
        self.view.lista_artistas_view.cargar_datos(artistas)
        self.view.mostrar("artistas")

    def nuevo_artista(self):
        self.artista_actual_id = None
        self.view.form_artista_view.limpiar_campos()
        self.view.mostrar("form_artista")

    def seleccionar_foto_artista(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if path: self.view.form_artista_view.set_foto(path)

    def editar_artista(self):
        id_sel = self.view.lista_artistas_view.obtener_seleccionado()
        if not id_sel:
            messagebox.showwarning("Aviso", "Seleccione un artista.")
            return
        artista = self.artista_model.obtener(id_sel)
        self.artista_actual_id = artista.id
        self.view.form_artista_view.cargar_datos(artista)
        self.view.mostrar("form_artista")

    def eliminar_artista_accion(self):
        id_sel = self.view.lista_artistas_view.obtener_seleccionado()
        if id_sel and messagebox.askyesno("Confirmar", "¿Eliminar artista?"):
            self.artista_model.eliminar(id_sel)
            self.refrescar_artistas()

    def guardar_artista(self):
        form = self.view.form_artista_view
        data = {
            "nombre": form.nombre_var.get().strip(),
            "tipo": form.tipo_var.get(),
            "info": form.txt_info.get("1.0", tk.END).strip(),
            "foto": getattr(form, 'foto_path', None)  # Usar getattr para evitar AttributeError
        }
        if not data["nombre"]:
            messagebox.showwarning("Aviso", "Nombre obligatorio.")
            return
        try:
            if self.artista_actual_id is None:
                self.artista_model.agregar(data)
            else:
                self.artista_model.actualizar(self.artista_actual_id, data)
            messagebox.showinfo("Éxito", "Artista guardado.")
            self.refrescar_artistas()
        except IntegrityError:
            messagebox.showerror("Error", "El artista ya existe.")

    def ejecutar_busqueda_artistas(self):
        texto = self.view.lista_artistas_view.buscar_var.get().strip()
        resultados = self.artista_model.buscar(texto) 
        self.view.lista_artistas_view.cargar_datos(resultados)

    # --- LÓGICA DE DISCOS ---

    def refrescar(self):
        self.refrescar_datos_silencioso()
        self.view.mostrar("lista")

    def nuevo(self):
        self.disco_actual_id = None
        self.imagen_actual_path = None
        self.view.form_view.limpiar_campos()
        self.actualizar_dropdown_artistas()
        self.view.form_view.artista_var.set("Artista")
        self.cargar_canciones() 
        self.view.mostrar("form", "Nuevo Disco")

    def editar(self):
        disco_id = self.view.lista_discos_view.obtener_id_seleccionado()
        if not disco_id:
            messagebox.showwarning("Aviso", "Seleccione un disco de la lista.")
            return
        
        disco = self.model.obtener(disco_id)
        if disco is None:
            messagebox.showerror("Error", f"No se encontró el disco con ID: {disco_id}")
            return

        self.disco_actual_id = disco.id
        self.imagen_actual_path = disco.portada
        self.actualizar_dropdown_artistas()
        self.view.form_view.cargar_datos(disco)
        self.cargar_canciones()
        self.view.mostrar("form", "Editar Disco")

    @log_alta
    @log_actualizacion
    def guardar(self):
        nombre_artista = self.view.form_view.artista_var.get().strip()
        if nombre_artista == "Artista" or not nombre_artista:
            messagebox.showwarning("Error", "Debe seleccionar un artista.")
            return

        artista_obj = Artista.get_or_none(Artista.nombre == nombre_artista)
        if not artista_obj:
            messagebox.showwarning("Error", "Artista no encontrado.")
            return
        
        data = {
            "artista": artista_obj.id,
            "titulo": self.view.form_view.titulo_var.get().strip(),
            "anio": self.view.form_view.anio_var.get().strip(),
            "formato": self.view.form_view.formato_var.get(),
            "portada": self.imagen_actual_path
        }
        try:
            if self.disco_actual_id is None:
                nuevo_disco = self.model.agregar(data)
                self.disco_actual_id = nuevo_disco.id
            else:
                self.model.actualizar(self.disco_actual_id, data)
            
            messagebox.showinfo("Éxito", "Disco guardado correctamente.")
            self.refrescar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    @log_eliminacion
    def eliminar(self):
        disco_id = self.view.lista_discos_view.obtener_id_seleccionado()
        if disco_id and messagebox.askyesno("Confirmar", "¿Eliminar disco?"):
            self.model.eliminar(disco_id)
            self.refrescar()

    def seleccionar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if path:
            self.imagen_actual_path = path
            self.view.form_view.set_imagen(path)

    def ejecutar_busqueda(self):
        texto = self.view.buscar_var.get().strip()
        self.view.limpiar_tabla()
        for d in self.model.buscar(texto):
            self.view.insertar_en_tabla(d.id, d.artista.nombre, d.titulo, d.anio, d.formato, d.portada)

    def actualizar_dropdown_artistas(self):
        artistas = self.artista_model.listar()
        nombres = [a.nombre for a in artistas]
        self.view.form_view.combo_artista['values'] = nombres if nombres else ["Artista"]

    # --- LÓGICA DE CANCIONES ---

    def mostrar_listado_canciones(self):
        todas = self.cancion_model.listar_todas_con_disco()
        self.view.mostrar("canciones")
        self.view.canciones_view.cargar_datos(todas)

    def ejecutar_busqueda_canciones(self):
        texto = self.view.canciones_view.buscar_var.get().strip()
        resultados = self.cancion_model.buscar(texto) 
        self.view.canciones_view.cargar_datos(resultados)

    def agregar_cancion(self):
        if not self.disco_actual_id:
            messagebox.showwarning("Aviso", "Primero guarde el disco.")
            return
        
        titulo = self.view.form_view.input_cancion.get().strip()
        numero_str = self.view.form_view.numero_pista_var.get().strip()
        duracion = self.view.form_view.duracion_var.get().strip()

        if not titulo or not numero_str:
            messagebox.showwarning("Aviso", "N° y Título obligatorios.")
            return

        try:
            data = {
                "numero_pista": int(numero_str),
                "titulo": titulo,
                "duracion": duracion if duracion else "N/A",
                "disco": self.disco_actual_id
            }
            if self.cancion_en_edicion_id:
                self.cancion_model.actualizar(self.cancion_en_edicion_id, data)
                self.cancion_en_edicion_id = None
                self.view.form_view.btn_agregar_cancion.config(text="✔")
            else:
                self.cancion_model.agregar(data)
            
            self.cargar_canciones() 
            todas = self.cancion_model.listar_todas_con_disco()
            self.view.canciones_view.cargar_datos(todas) 
            
            self.view.form_view.numero_pista_var.set("")
            self.view.form_view.input_cancion.delete(0, "end")
            self.view.form_view.duracion_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Error en canción: {str(e)}")

    def cargar_canciones(self):
        self.view.form_view.lista_canciones.delete(0, tk.END)
        if not self.disco_actual_id: return
        canciones = self.cancion_model.listar_por_disco(self.disco_actual_id)
        for c in canciones:
            texto = f"{c.numero_pista:02d} - {c.titulo} ({c.duracion})"
            self.view.form_view.lista_canciones.insert(tk.END, texto)

    def preparar_edicion_cancion(self):
        seleccion = self.view.form_view.lista_canciones.curselection()
        if not seleccion: return
        canciones = list(self.cancion_model.listar_por_disco(self.disco_actual_id))
        cancion = canciones[seleccion[0]]
        self.cancion_en_edicion_id = cancion.id
        self.view.form_view.numero_pista_var.set(cancion.numero_pista)
        self.view.form_view.input_cancion.delete(0, "end")
        self.view.form_view.input_cancion.insert(0, cancion.titulo)
        self.view.form_view.duracion_var.set(cancion.duracion)
        self.view.form_view.btn_agregar_cancion.config(text="💾")

    def eliminar_cancion(self):
        seleccion = self.view.form_view.lista_canciones.curselection()
        if not seleccion: return
        if messagebox.askyesno("Confirmar", "¿Eliminar pista?"):
            canciones = list(self.cancion_model.listar_por_disco(self.disco_actual_id))
            self.cancion_model.eliminar(canciones[seleccion[0]].id)
            self.cargar_canciones()
            self.mostrar_listado_canciones()