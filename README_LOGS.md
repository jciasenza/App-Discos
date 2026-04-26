# Sistema de Logs Centralizado - App Discos

Este sistema implementa un patrón observador mejorado que permite registrar eventos tanto localmente como en un servidor centralizado de logs.

## Componentes

### 1. **servidor_logs.py** - Servidor Centralizado de Logs
Servidor TCP que escucha conexiones de clientes y registra todos los eventos en un archivo de log.

**Características:**
- Escucha en `localhost:5000` por defecto
- Maneja múltiples clientes simultáneamente con threads
- Recibe eventos en formato JSON
- Registra con diferentes niveles (INFO, WARNING, ERROR)
- Genera archivo `servidor_logs.log`

**Uso:**
```bash
python servidor_logs.py
```

**Salida esperada:**
```
✓ Servidor iniciado en localhost:5000
✓ Cliente conectado desde ('127.0.0.1', 54321)
📨 [App-Discos] Evento: artista_agregado | Datos: ...
```

---

### 2. **cliente_logs.py** - Cliente de Logs
Cliente que se conecta al servidor y envía eventos de la aplicación.

**Características:**
- Conexión TCP al servidor de logs
- Envío de eventos en JSON
- Manejo automático de desconexiones
- Registro local en `cliente_logs.log`
- Confirmación de recepción desde el servidor

**Uso programático:**
```python
from cliente_logs import ClienteLogs

# Crear cliente
cliente = ClienteLogs(nombre_cliente='Mi-App')

# Conectar
if cliente.conectar():
    # Enviar evento
    cliente.enviar_log('evento_importante', {'dato': 'valor'}, 'INFO')
    
    # Desconectar
    cliente.desconectar()
```

**Uso de prueba:**
```bash
python cliente_logs.py
```

---

### 3. **Patrones Observadores en model.py**

#### ObservadorLog (Local)
Registra eventos en un archivo local usando `logging`.

```python
observador_log = ObservadorLog()
model_artista.agregar_observador(observador_log)
```

#### ObservadorClienteLogs (Remoto)
Envía eventos a un servidor centralizado.

```python
cliente_logs = ClienteLogs(nombre_cliente='App-Discos')
cliente_logs.conectar()
observador_cliente = ObservadorClienteLogs(cliente_logs)
model_disco.agregar_observador(observador_cliente)
```

---

## Flujo de Funcionamiento

```
┌─────────────────┐
│  App Discos     │
│  (main.py)      │
└────────┬────────┘
         │
         ├─► ObservadorLog ──► app_discos.log (local)
         │
         └─► ObservadorClienteLogs ──► ClienteLogs
                                           │
                                           └─► ServidorLogs
                                                    │
                                                    └─► servidor_logs.log
```

---

## Formato de Mensajes JSON

### Enviado por Cliente:
```json
{
    "evento": "artista_agregado",
    "datos": {
        "id": 1,
        "nombre": "The Beatles"
    },
    "nivel": "INFO",
    "cliente": "App-Discos"
}
```

### Respuesta del Servidor:
```json
{
    "estado": "recibido",
    "evento": "artista_agregado"
}
```

---

## Niveles de Log por Evento

| Tipo de Evento | Nivel | Color |
|---|---|---|
| `*_agregado/*_agregada` | INFO | Verde |
| `*_actualizado/*_actualizada` | WARNING | Amarillo |
| `*_eliminado/*_eliminada` | ERROR | Rojo |

---

## Archivos de Log Generados

### 1. `app_discos.log` (Local)
```
2026-04-26 10:30:45 - INFO - Evento: artista_agregado | Datos: <Artista object>
2026-04-26 10:31:12 - WARNING - Evento: disco_actualizado | Datos: {'id': 1, 'data': {'anio': 1969}}
2026-04-26 10:32:00 - ERROR - Evento: disco_eliminado | Datos: 1
```

### 2. `servidor_logs.log` (Servidor)
```
2026-04-26 10:30:45 - INFO - Servidor iniciado en localhost:5000
2026-04-26 10:30:47 - INFO - Cliente conectado desde ('127.0.0.1', 54321)
2026-04-26 10:30:50 - INFO - [App-Discos] Evento: artista_agregado | Datos: {...}
```

### 3. `cliente_logs.log` (Cliente)
```
2026-04-26 10:30:47 - INFO - Conectado al servidor en localhost:5000
2026-04-26 10:30:50 - INFO - Log enviado: artista_agregado
```

---

## Instrucciones de Uso

### Paso 1: Iniciar Servidor (en una terminal)
```bash
cd c:\Users\curej\Desktop\UTN\App Discos
python servidor_logs.py
```

### Paso 2: Ejecutar la Aplicación (en otra terminal)
```bash
python main.py
```

La aplicación intentará conectarse al servidor automáticamente:
- Si el servidor está activo: ambos logs local y remoto funcionan
- Si el servidor no está disponible: solo funciona logging local

### Prueba Rápida del Cliente
```bash
python cliente_logs.py
```

---

## Configuración

### Cambiar Puerto del Servidor
En `servidor_logs.py`:
```python
servidor = ServidorLogs(host='localhost', puerto=5001)  # Cambiar 5000 a 5001
```

En `cliente_logs.py`:
```python
cliente = ClienteLogs(host='localhost', puerto=5001)  # Cambiar 5000 a 5001
```

### Cambiar Nombre del Cliente
```python
cliente = ClienteLogs(nombre_cliente='Mi-Nombre-Personalizado')
```

---

## Manejo de Errores

- **Servidor no disponible**: El cliente se desconecta automáticamente y muestra una advertencia
- **JSON inválido**: El servidor registra el error y continúa funcionando
- **Cliente averiado**: El servidor registra el error y espera al siguiente cliente
- **Desconexión inesperada**: Ambos lados detectan la desconexión y registran el evento

---

## Ventajas de esta Implementación

✓ **Escalabilidad**: Múltiples clientes pueden conectarse a un servidor  
✓ **Flexibilidad**: Nuevos observadores sin modificar el código existente  
✓ **Resiliencia**: Si el servidor falla, la app continúa con logs locales  
✓ **Separación de responsabilidades**: Los niveles de abstracción están claramente definidos  
✓ **Monitoreo centralizado**: Todos los eventos en un único lugar  
✓ **Trazabilidad**: Logs con timestamps y información del cliente origen  

