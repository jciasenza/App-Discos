import socket
import threading
import logging
import json
from datetime import datetime

# Configuración de logging del servidor
logging.basicConfig(
    filename='servidor_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ServidorLogs:
    def __init__(self, host='localhost', puerto=5000):
        self.host = host
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.activo = True
        
    def iniciar(self):
        try:
            self.servidor.bind((self.host, self.puerto))
            self.servidor.listen(5)
            print(f"✓ Servidor iniciado en {self.host}:{self.puerto}")
            logger.info(f"Servidor iniciado en {self.host}:{self.puerto}")
            
            while self.activo:
                try:
                    cliente_socket, direccion_cliente = self.servidor.accept()
                    print(f"✓ Cliente conectado desde {direccion_cliente}")
                    logger.info(f"Cliente conectado desde {direccion_cliente}")
                    
                    # Crear un hilo para manejar al cliente
                    hilo_cliente = threading.Thread(
                        target=self.manejar_cliente,
                        args=(cliente_socket, direccion_cliente)
                    )
                    hilo_cliente.daemon = True
                    hilo_cliente.start()
                    
                except Exception as e:
                    print(f"✗ Error al aceptar cliente: {e}")
                    logger.error(f"Error al aceptar cliente: {e}")
                    
        except Exception as e:
            print(f"✗ Error al iniciar servidor: {e}")
            logger.error(f"Error al iniciar servidor: {e}")
        finally:
            self.servidor.close()
            
    def manejar_cliente(self, cliente_socket, direccion_cliente):
        try:
            while self.activo:
                # Recibir datos del cliente
                datos = cliente_socket.recv(1024).decode('utf-8')
                
                if not datos:
                    break
                
                try:
                    # Parsear JSON
                    mensaje = json.loads(datos)
                    evento = mensaje.get('evento', 'desconocido')
                    nivel = mensaje.get('nivel', 'INFO')
                    datos_evento = mensaje.get('datos', {})
                    cliente_info = mensaje.get('cliente', 'desconocido')
                    
                    # Registrar en logs con nivel especificado
                    log_message = f"[{cliente_info}] Evento: {evento} | Datos: {datos_evento}"
                    
                    if nivel.upper() == 'INFO':
                        logger.info(log_message)
                    elif nivel.upper() == 'WARNING':
                        logger.warning(log_message)
                    elif nivel.upper() == 'ERROR':
                        logger.error(log_message)
                    else:
                        logger.info(log_message)
                    
                    print(f"{log_message}")
                    
                    # Enviar confirmación al cliente
                    respuesta = json.dumps({'estado': 'recibido', 'evento': evento})
                    cliente_socket.send(respuesta.encode('utf-8'))
                    
                except json.JSONDecodeError:
                    print(f"✗ Error: JSON inválido recibido")
                    logger.error(f"JSON inválido recibido de {direccion_cliente}")
                    
        except Exception as e:
            print(f"✗ Error manejando cliente: {e}")
            logger.error(f"Error manejando cliente {direccion_cliente}: {e}")
        finally:
            cliente_socket.close()
            print(f"✓ Cliente desconectado: {direccion_cliente}")
            logger.info(f"Cliente desconectado: {direccion_cliente}")
    
    def detener(self):
        self.activo = False
        self.servidor.close()
        print("Servidor detenido")
        logger.info("Servidor detenido")

if __name__ == "__main__":
    servidor = ServidorLogs(host='localhost', puerto=5000)
    try:
        servidor.iniciar()
    except KeyboardInterrupt:
        print("\n⚠ Interrumpido por usuario")
        servidor.detener()
