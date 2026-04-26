import socket
import json
import logging
from datetime import datetime

class JSONEncoderPersonalizado(json.JSONEncoder):
    """Codificador JSON personalizado que maneja tipos especiales"""
    def default(self, o):
        # Manejar objetos Peewee
        if hasattr(o, '__dict__') and hasattr(o, '_meta'):
            return {
                'id': getattr(o, 'id', None),
                'tipo': o.__class__.__name__,
                **{k: str(v) if isinstance(v, set) else v 
                   for k, v in o.__dict__.items() 
                   if not k.startswith('_')}
            }
        # Manejar sets
        elif isinstance(o, set):
            return list(o)
        # Manejar datetime
        elif isinstance(o, datetime):
            return o.isoformat()
        # Manejar otros objetos
        elif hasattr(o, '__dict__'):
            return {k: str(v) if isinstance(v, set) else v 
                   for k, v in o.__dict__.items() 
                   if not k.startswith('_')}
        else:
            return str(o)

class ClienteLogs:
    def __init__(self, host='localhost', puerto=5000, nombre_cliente='Cliente'):
        self.host = host
        self.puerto = puerto
        self.nombre_cliente = nombre_cliente
        self.socket = None
        self.conectado = False
        
        # Configurar logging local también
        logging.basicConfig(
            filename='cliente_logs.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
    def conectar(self):
        """Conecta al servidor de logs"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.puerto))
            self.conectado = True
            print(f"✓ Conectado al servidor en {self.host}:{self.puerto}")
            self.logger.info(f"Conectado al servidor en {self.host}:{self.puerto}")
            return True
        except Exception as e:
            print(f"✗ Error conectando al servidor: {e}")
            self.logger.error(f"Error conectando al servidor: {e}")
            self.conectado = False
            return False
    
    def enviar_log(self, evento, datos, nivel='INFO'):
        """Envía un evento de log al servidor
        
        Args:
            evento (str): Nombre del evento (ej: 'artista_agregado')
            datos (dict): Datos del evento
            nivel (str): Nivel de log ('INFO', 'WARNING', 'ERROR')
        """
        if not self.conectado:
            if not self.conectar():
                self.logger.error(f"No se puede enviar log {evento} - no conectado")
                return False
        
        try:
            # Crear mensaje JSON
            mensaje = {
                'evento': evento,
                'datos': datos,
                'nivel': nivel,
                'cliente': self.nombre_cliente
            }
            
            # Enviar al servidor con codificador personalizado
            self.socket.send(json.dumps(mensaje, cls=JSONEncoderPersonalizado).encode('utf-8'))
            
            # Recibir confirmación
            respuesta = self.socket.recv(1024).decode('utf-8')
            respuesta_json = json.loads(respuesta)
            
            if respuesta_json.get('estado') == 'recibido':
                print(f"Log enviado: {evento}")
                self.logger.info(f"Log enviado: {evento}")
                return True
            
        except (ConnectionResetError, BrokenPipeError):
            print(f"✗ Conexión perdida con el servidor")
            self.logger.error("Conexión perdida con el servidor")
            self.conectado = False
            return False
        except Exception as e:
            print(f"✗ Error enviando log: {e}")
            self.logger.error(f"Error enviando log: {e}")
            return False
    
    def desconectar(self):
        """Desconecta del servidor"""
        try:
            if self.socket:
                self.socket.close()
            self.conectado = False
            print(f"✓ Desconectado del servidor")
            self.logger.info("Desconectado del servidor")
        except Exception as e:
            print(f"✗ Error desconectando: {e}")
            self.logger.error(f"Error desconectando: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear cliente
    cliente = ClienteLogs(nombre_cliente='App-Discos-Test')
    
    # Conectar
    if cliente.conectar():
        # Enviar algunos logs de prueba
        cliente.enviar_log('artista_agregado', {'id': 1, 'nombre': 'The Beatles'}, 'INFO')
        cliente.enviar_log('disco_agregado', {'id': 1, 'titulo': 'Abbey Road', 'artista_id': 1}, 'INFO')
        cliente.enviar_log('disco_actualizado', {'id': 1, 'anio': 1969}, 'WARNING')
        cliente.enviar_log('cancion_eliminada', {'id': 5}, 'ERROR')
        
        # Desconectar
        cliente.desconectar()
