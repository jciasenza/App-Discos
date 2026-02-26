"""
Módulo de Modelos y Base de Datos
=================================

Este módulo define la estructura de la base de datos utilizando Peewee ORM
y proporciona las clases encargadas de la lógica CRUD (Crear, Leer, Actualizar, Borrar).
"""

from peewee import *

# Configuración de la Base de Datos
DB_NAME = "discos.db"
db_discos = SqliteDatabase(DB_NAME)

class BaseModel(Model):
    """Clase base para todos los modelos de la base de datos."""
    class Meta:
        database = db_discos

# --- TABLA: ARTISTA ---
class Artista(BaseModel):
    """
    Representa a un artista en la base de datos.
    
    Attributes:
        nombre (CharField): Nombre único del artista.
        tipo (CharField): Género o tipo de agrupación.
        info (TextField): Información biográfica adicional.
        foto (CharField): Ruta al archivo de imagen.
    """
    nombre = CharField(unique=True)
    tipo = CharField()
    info = TextField(null=True)
    foto = CharField(null=True)

# --- TABLA: DISCOS ---
class Discos(BaseModel):
    """
    Representa un álbum musical vinculado a un artista.
    
    Attributes:
        artista (ForeignKeyField): Referencia al artista creador.
        titulo (CharField): Título del disco.
        anio (IntegerField): Año de lanzamiento.
        formato (CharField): Formato físico o digital (CD, Vinilo, etc).
        portada (CharField): Ruta a la imagen de portada.
    """
    artista = ForeignKeyField(Artista, backref='discos', on_delete='CASCADE')
    titulo = CharField()
    anio = IntegerField(null=True)
    formato = CharField()
    portada = CharField(null=True)

# --- TABLA: CANCION ---
class Cancion(BaseModel):
    """
    Representa una pista individual dentro de un disco.
    
    Attributes:
        numero_pista (IntegerField): Orden de la canción en el disco.
        titulo (CharField): Título de la canción.
        duracion (CharField): Duración en formato MM:SS.
        disco (ForeignKeyField): Referencia al disco al que pertenece.
    """
    numero_pista = IntegerField() 
    titulo = CharField()
    duracion = CharField(null=True)
    disco = ForeignKeyField(Discos, backref="canciones", on_delete="CASCADE")

    class Meta:
        indexes = ((("numero_pista", "disco"), True),)

# --- INICIALIZACIÓN DE LA DB ---
def inicializar_db():
    """
    Conecta a la base de datos, activa claves foráneas y crea las tablas
    si estas no existen.
    """
    if db_discos.is_closed():
        db_discos.connect()
    db_discos.execute_sql("PRAGMA foreign_keys = ON;")
    db_discos.create_tables([Artista, Discos, Cancion])

# --- CLASES CRUD ---

class ArtistaModel:
    """Lógica de negocio para la gestión de Artistas."""

    def agregar(self, data):
        """Crea un nuevo artista.
        
        Args:
            data (dict): Diccionario con los campos del artista.
        """
        return Artista.create(**data)

    def listar(self):
        """Retorna todos los artistas ordenados por nombre."""
        return Artista.select().order_by(Artista.nombre)

    def obtener(self, artista_id):
        """Obtiene un artista por su ID o None si no existe."""
        return Artista.get_or_none(Artista.id == artista_id)

    def actualizar(self, artista_id, data):
        """Actualiza los datos de un artista existente."""
        return Artista.update(**data).where(Artista.id == artista_id).execute()

    def eliminar(self, artista_id):
        """Elimina un artista de la base de datos."""
        return Artista.delete().where(Artista.id == artista_id).execute()
    
    def buscar(self, texto):
        """Busca artistas cuyo nombre contenga el texto proporcionado."""
        return Artista.select().where(Artista.nombre.contains(texto)).order_by(Artista.nombre)

class DiscoModel:
    """Lógica de negocio para la gestión de Discos."""

    def agregar(self, data):
        """Crea un nuevo disco."""
        return Discos.create(**data)

    def listar(self):
        """Lista todos los discos incluyendo la información de su artista."""
        return Discos.select(Discos, Artista).join(Artista).order_by(Discos.id.desc())

    def obtener(self, disco_id):
        """Obtiene un disco por su ID."""
        return Discos.get_or_none(Discos.id == disco_id)

    def actualizar(self, disco_id, data):
        """Actualiza un disco existente."""
        return Discos.update(**data).where(Discos.id == disco_id).execute()

    def eliminar(self, disco_id):
        """Elimina un disco de la base de datos."""
        return Discos.delete().where(Discos.id == disco_id).execute()
    
    def buscar(self, texto):
        """Busca discos por título o nombre del artista."""
        return (Discos.select(Discos, Artista).join(Artista)
                .where((Artista.nombre.contains(texto)) | (Discos.titulo.contains(texto)))
                .order_by(Artista.nombre))

class CancionModel:
    """Lógica de negocio para la gestión de Canciones."""

    def agregar(self, data):
        """Agrega una canción a un disco."""
        return Cancion.create(**data)

    def listar_por_disco(self, disco_id):
        """Retorna las canciones de un disco específico ordenadas por pista."""
        return Cancion.select().where(Cancion.disco == disco_id).order_by(Cancion.numero_pista)
    
    def listar_todas_con_disco(self):
        """Lista todas las canciones con su información de disco y artista."""
        return Cancion.select(Cancion, Discos, Artista).join(Discos).join(Artista).order_by(Artista.nombre, Discos.titulo, Cancion.numero_pista)

    def actualizar(self, cancion_id, data):
        """Actualiza los datos de una canción."""
        return Cancion.update(**data).where(Cancion.id == cancion_id).execute()

    def eliminar(self, cancion_id):
        """Elimina una canción por su ID."""
        return Cancion.delete().where(Cancion.id == cancion_id).execute()
    
    def buscar(self, texto):
        """Búsqueda global de canciones por título, artista o disco."""
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
    
if __name__ == "__main__":
    inicializar_db()