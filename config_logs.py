"""
Configuración centralizada para el sistema de logs
"""

# Configuración del Servidor
SERVIDOR_CONFIG = {
    'host': 'localhost',      # Host del servidor
    'puerto': 5000,           # Puerto del servidor
    'max_conexiones': 5,      # Máximo número de conexiones simultáneas
}

# Configuración del Cliente
CLIENTE_CONFIG = {
    'host': 'localhost',           # Host del servidor (debe coincidir con SERVIDOR_CONFIG)
    'puerto': 5000,                # Puerto del servidor (debe coincidir con SERVIDOR_CONFIG)
    'nombre_cliente': 'App-Discos', # Nombre identificativo del cliente
    'timeout': 5,                  # Timeout en segundos para conexión
}

# Configuración de Logging
LOGGING_CONFIG = {
    'archivo_servidor': 'servidor_logs.log',
    'archivo_cliente': 'cliente_logs.log',
    'archivo_local': 'app_discos.log',
    'level': 'INFO',
    'formato': '%(asctime)s - %(levelname)s - %(message)s',
    'fecha_formato': '%Y-%m-%d %H:%M:%S',
}

# Mensajes de Estado
MENSAJES = {
    'servidor_iniciado': '✓ Servidor iniciado en {host}:{puerto}',
    'cliente_conectado': '✓ Cliente conectado desde {direccion}',
    'error_servidor': '✗ Error al iniciar servidor: {error}',
    'error_cliente': '✗ Error conectando al servidor: {error}',
    'conexion_perdida': '✗ Conexión perdida con el servidor',
}
