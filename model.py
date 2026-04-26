from peewee import *
import logging

# Configuración de logging
logging.basicConfig(
    filename='app_discos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuración de la Base de Datos
DB_NAME = "discos.db"
db_discos = SqliteDatabase(DB_NAME)

class BaseModel(Model):
    class Meta:
        database = db_discos

# --- TABLA: ARTISTA ---
class Artista(BaseModel):
    nombre = CharField(unique=True)
    tipo = CharField()
    info = TextField(null=True)
    foto = CharField(null=True)

# --- TABLA: DISCOS ---
class Discos(BaseModel):
    artista = ForeignKeyField(Artista, backref='discos', on_delete='CASCADE')
    titulo = CharField()
    anio = IntegerField(null=True)
    formato = CharField()
    portada = CharField(null=True)

# --- TABLA: CANCION ---
class Cancion(BaseModel):
    numero_pista = IntegerField() 
    titulo = CharField()
    duracion = CharField(null=True)
    disco = ForeignKeyField(Discos, backref="canciones", on_delete="CASCADE")

    class Meta:
        indexes = ((("numero_pista", "disco"), True),)

# --- INICIALIZACIÓN DE LA DB ---
def inicializar_db():
    if db_discos.is_closed():
        db_discos.connect()
    db_discos.execute_sql("PRAGMA foreign_keys = ON;")
    db_discos.create_tables([Artista, Discos, Cancion])

inicializar_db()

class Observable:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        self._observadores.append(observador)

    def eliminar_observador(self, observador):
        self._observadores.remove(observador)

    def notificar(self, evento, datos):
        for obs in self._observadores:
            obs.actualizar(evento, datos)

class ObservadorLog:
    def actualizar(self, evento, datos):
        if "agregado" in evento or "agregada" in evento:
            logger.info(f"Evento: {evento} | Datos: {datos}")
        elif "actualizado" in evento:
            logger.warning(f"Evento: {evento} | Datos: {datos}")
        elif "eliminado" in evento:
            logger.error(f"Evento: {evento} | Datos: {datos}")
        else:
            logger.info(f"Evento: {evento} | Datos: {datos}")

class ObservadorClienteLogs:
    """Observador que envía eventos a un servidor remoto de logs"""
    def __init__(self, cliente_logs):
        self.cliente_logs = cliente_logs
    
    @staticmethod
    def _convertir_datos(datos):
        """Convierte objetos Peewee y otros tipos a diccionarios serializables"""
        try:
            # Si es un modelo Peewee
            if hasattr(datos, '_meta'):  # Tiene atributo _meta (típico de Peewee)
                resultado = {}
                for campo in datos._meta.fields:
                    valor = getattr(datos, campo)
                    # Evitar objetos complejos, convertir a string
                    if isinstance(valor, (str, int, float, bool, type(None))):
                        resultado[campo] = valor
                    else:
                        resultado[campo] = str(valor)
                return resultado
            # Si es un diccionario
            elif isinstance(datos, dict):
                return {k: v for k, v in datos.items() if not isinstance(v, set)}
            # Si es una lista o tupla
            elif isinstance(datos, (list, tuple)):
                return str(datos)
            # Si es un tipo primitivo (int, str, etc)
            elif isinstance(datos, (str, int, float, bool, type(None))):
                return datos
            # Para otros tipos, convertir a string
            else:
                return str(datos)
        except Exception as e:
            return f"Error convertiendo datos: {str(e)}"
    
    def actualizar(self, evento, datos):
        # Determinar nivel según el tipo de evento
        if "agregado" in evento or "agregada" in evento:
            nivel = "INFO"
        elif "actualizado" in evento:
            nivel = "WARNING"
        elif "eliminado" in evento:
            nivel = "ERROR"
        else:
            nivel = "INFO"
        
        # Convertir datos a formato serializable
        datos_dict = self._convertir_datos(datos)
        
        self.cliente_logs.enviar_log(evento, datos_dict, nivel)

# --- CLASES CRUD ---
class ArtistaModel(Observable):
    def __init__(self):
        super().__init__()

    def agregar(self, data):
        artista = Artista.create(**data)
        self.notificar("artista_agregado", artista)
        return artista

    def listar(self):
        return Artista.select().order_by(Artista.nombre)

    def obtener(self, artista_id):
        return Artista.get_or_none(Artista.id == artista_id)

    def actualizar(self, artista_id, data):
        result = Artista.update(**data).where(Artista.id == artista_id).execute()
        self.notificar("artista_actualizado", {"id": artista_id, "data": data})
        return result

    def eliminar(self, artista_id):
        result = Artista.delete().where(Artista.id == artista_id).execute()
        self.notificar("artista_eliminado", artista_id)
        return result  
    
    def buscar(self, texto):
        return Artista.select().where(Artista.nombre.contains(texto)).order_by(Artista.nombre)  

class DiscoModel(Observable):
    def __init__(self):
        super().__init__()

    def agregar(self, data):
        disco = Discos.create(**data)
        self.notificar("disco_agregado", disco)
        return disco

    def listar(self):
        return Discos.select(Discos, Artista).join(Artista).order_by(Discos.id.desc())

    def obtener(self, disco_id):
        return Discos.get_or_none(Discos.id == disco_id)

    def actualizar(self, disco_id, data):
        result = Discos.update(**data).where(Discos.id == disco_id).execute()
        self.notificar("disco_actualizado", {"id": disco_id, "data": data})
        return result

    def eliminar(self, disco_id):
        result = Discos.delete().where(Discos.id == disco_id).execute()
        self.notificar("disco_eliminado", disco_id)
        return result
    
    def buscar(self, texto):
        return (Discos.select(Discos, Artista).join(Artista)
                .where((Artista.nombre.contains(texto)) | (Discos.titulo.contains(texto)))
                .order_by(Artista.nombre))

class CancionModel(Observable):
    def __init__(self):
        super().__init__()

    def agregar(self, data):
        cancion = Cancion.create(**data)
        self.notificar("cancion_agregada", cancion)
        return cancion

    def listar_por_disco(self, disco_id):
        return Cancion.select().where(Cancion.disco == disco_id).order_by(Cancion.numero_pista)
    
    def listar_todas_con_disco(self):
        return Cancion.select(Cancion, Discos, Artista).join(Discos).join(Artista).order_by(Artista.nombre, Discos.titulo, Cancion.numero_pista)

    def actualizar(self, cancion_id, data):
        result = Cancion.update(**data).where(Cancion.id == cancion_id).execute()
        self.notificar("cancion_actualizada", {"id": cancion_id, "data": data})
        return result

    def eliminar(self, cancion_id):
        result = Cancion.delete().where(Cancion.id == cancion_id).execute()
        self.notificar("cancion_eliminada", cancion_id)
        return result
    
    def buscar(self, texto):
        query = (Cancion
                .select(Cancion, Discos, Artista)
                .join(Discos)
                .join(Artista)
                .where(
                    (Cancion.titulo ** f"%{texto}%") | 
                    (Artista.nombre ** f"%{texto}%") |
                    (Discos.titulo ** f"%{texto}%")
                ))
        return query