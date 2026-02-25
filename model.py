from peewee import *

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

# --- CLASES CRUD ---
class ArtistaModel:
    def agregar(self, data):
        return Artista.create(**data)

    def listar(self):
        return Artista.select().order_by(Artista.nombre)

    def obtener(self, artista_id):
        return Artista.get_or_none(Artista.id == artista_id)

    def actualizar(self, artista_id, data):
        return Artista.update(**data).where(Artista.id == artista_id).execute()

    def eliminar(self, artista_id):
        return Artista.delete().where(Artista.id == artista_id).execute()
    
    def buscar(self, texto):
        return Artista.select().where(Artista.nombre.contains(texto)).order_by(Artista.nombre)

class DiscoModel:
    def agregar(self, data):
        return Discos.create(**data)

    def listar(self):
        return Discos.select(Discos, Artista).join(Artista).order_by(Discos.id.desc())

    def obtener(self, disco_id):
        return Discos.get_or_none(Discos.id == disco_id)

    def actualizar(self, disco_id, data):
        return Discos.update(**data).where(Discos.id == disco_id).execute()

    def eliminar(self, disco_id):
        return Discos.delete().where(Discos.id == disco_id).execute()
    
    def buscar(self, texto):
        return (Discos.select(Discos, Artista).join(Artista)
                .where((Artista.nombre.contains(texto)) | (Discos.titulo.contains(texto)))
                .order_by(Artista.nombre))

class CancionModel:
    def agregar(self, data):
        return Cancion.create(**data)

    def listar_por_disco(self, disco_id):
        return Cancion.select().where(Cancion.disco == disco_id).order_by(Cancion.numero_pista)
    
    def listar_todas_con_disco(self):
        return Cancion.select(Cancion, Discos, Artista).join(Discos).join(Artista).order_by(Artista.nombre, Discos.titulo, Cancion.numero_pista)

    def actualizar(self, cancion_id, data):
        return Cancion.update(**data).where(Cancion.id == cancion_id).execute()

    def eliminar(self, cancion_id):
        return Cancion.delete().where(Cancion.id == cancion_id).execute()
    
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