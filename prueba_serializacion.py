import json
from cliente_logs import JSONEncoderPersonalizado
from model import Artista, Discos, Cancion

# Prueba 1: Objeto con set (problema original)
print("=" * 60)
print("PRUEBA 1: Objeto con set")
print("=" * 60)

datos_con_set = {
    'id': 1,
    'nombre': 'The Beatles',
    'tags': {'rock', 'britpop', 'classico'}  # Esto es un set
}

try:
    json_str = json.dumps(datos_con_set, cls=JSONEncoderPersonalizado)
    print(f"✓ Set convertido correctamente: {json_str}")
except Exception as e:
    print(f"✗ Error: {e}")

# Prueba 2: Objeto Peewee (simulado)
print("\n" + "=" * 60)
print("PRUEBA 2: Diccionario con valores complejos")
print("=" * 60)

datos_complejos = {
    'id': 1,
    'titulo': 'Abbey Road',
    'anio': 1969,
    'valores_especiales': {'a', 'b', 'c'},  # set
}

try:
    json_str = json.dumps(datos_complejos, cls=JSONEncoderPersonalizado)
    print(f"✓ Diccionario complejo serializado: {json_str}")
except Exception as e:
    print(f"✗ Error: {e}")

# Prueba 3: Números, strings, None
print("\n" + "=" * 60)
print("PRUEBA 3: Tipos primitivos")
print("=" * 60)

tipos_primitivos = {
    'string': 'texto',
    'numero': 42,
    'decimal': 3.14,
    'booleano': True,
    'nulo': None
}

try:
    json_str = json.dumps(tipos_primitivos, cls=JSONEncoderPersonalizado)
    print(f"✓ Tipos primitivos serializados: {json_str}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("TODAS LAS PRUEBAS COMPLETADAS")
print("=" * 60)
