"""
Script de prueba para demostrar la comunicación cliente-servidor
Ejecutar este script DESPUÉS de iniciar servidor_logs.py
"""

import time
from cliente_logs import ClienteLogs

def main():
    print("=" * 60)
    print("PRUEBA DE CLIENTE DE LOGS")
    print("=" * 60)
    
    # Crear cliente
    cliente = ClienteLogs(nombre_cliente='Test-App', host='localhost', puerto=5000)
    
    # Intentar conectar
    print("\n[1] Intentando conectar al servidor...")
    if not cliente.conectar():
        print("✗ No se pudo conectar al servidor.")
        print("   Asegúrate de ejecutar: python servidor_logs.py")
        return
    
    print("\n[2] Enviando eventos de prueba...")
    time.sleep(0.5)
    
    # Ejemplo 1: Agregar artista
    cliente.enviar_log(
        evento='artista_agregado',
        datos={'id': 1, 'nombre': 'The Beatles', 'tipo': 'Banda'},
        nivel='INFO'
    )
    time.sleep(0.3)
    
    # Ejemplo 2: Agregar disco
    cliente.enviar_log(
        evento='disco_agregado',
        datos={'id': 1, 'titulo': 'Abbey Road', 'artista_id': 1, 'anio': 1969},
        nivel='INFO'
    )
    time.sleep(0.3)
    
    # Ejemplo 3: Agregar canción
    cliente.enviar_log(
        evento='cancion_agregada',
        datos={'id': 1, 'titulo': 'Come Together', 'numero_pista': 1, 'disco_id': 1},
        nivel='INFO'
    )
    time.sleep(0.3)
    
    # Ejemplo 4: Actualizar disco
    cliente.enviar_log(
        evento='disco_actualizado',
        datos={'id': 1, 'campos': {'anio': 1969}},
        nivel='WARNING'
    )
    time.sleep(0.3)
    
    # Ejemplo 5: Eliminar canción
    cliente.enviar_log(
        evento='cancion_eliminada',
        datos={'id': 1, 'titulo': 'Come Together'},
        nivel='ERROR'
    )
    time.sleep(0.3)
    
    # Ejemplo 6: Eliminar disco
    cliente.enviar_log(
        evento='disco_eliminado',
        datos={'id': 1},
        nivel='ERROR'
    )
    time.sleep(0.3)
    
    # Ejemplo 7: Eliminar artista
    cliente.enviar_log(
        evento='artista_eliminado',
        datos={'id': 1, 'nombre': 'The Beatles'},
        nivel='ERROR'
    )
    
    print("\n[3] Todos los eventos fueron enviados")
    print("\n[4] Desconectando...")
    cliente.desconectar()
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)
    print("\nArchivos de log generados:")
    print("  • cliente_logs.log (en este directorio)")
    print("  • servidor_logs.log (en la máquina del servidor)")
    print("\nPara ver los logs:")
    print("  • Windows: type cliente_logs.log")
    print("  • Linux/Mac: cat cliente_logs.log")

if __name__ == "__main__":
    main()
