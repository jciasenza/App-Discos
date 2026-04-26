"""
DIAGRAMA DE ARQUITECTURA - Sistema de Logs Cliente-Servidor
"""

ARQUITECTURA = """

╔════════════════════════════════════════════════════════════════════════════╗
║                    SISTEMA DE LOGS CENTRALIZADO                            ║
╚════════════════════════════════════════════════════════════════════════════╝


                              ┌─────────────────────┐
                              │   APP DISCOS (GUI)  │
                              │   (main.py)         │
                              └──────────┬──────────┘
                                         │
                      ┌──────────────────┼──────────────────┐
                      │                  │                  │
                      ▼                  ▼                  ▼
            ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐
            │  ArtistaModel │  │  DiscoModel  │  │  CancionModel   │
            │ (Observable)  │  │(Observable)  │  │  (Observable)   │
            └───────────────┘  └──────────────┘  └─────────────────┘
                      │                  │                  │
                      │ notificar()       │ notificar()     │ notificar()
                      │                  │                  │
        ┌─────────────┴──────────────────┴──────────────────┴────────────┐
        │                                                                  │
        ▼                                                                  ▼
    ┌──────────────┐                              ┌─────────────────────┐
    │ ObservadorLog│                              │ObservadorClienteLogs│
    │  (Local)     │                              │  (Remoto)           │
    └──────┬───────┘                              └──────────┬──────────┘
           │                                                  │
           │ logger.info()                                    │ enviar_log()
           │                                                  │
           ▼                                                  ▼
    ┌──────────────┐                              ┌─────────────────────┐
    │app_discos.log│                              │   ClienteLogs       │
    │   (archivo)  │                              │  (TCPClient)        │
    └──────────────┘                              └──────────┬──────────┘
                                                             │
                                                   JSON (UTF-8)
                                                             │
                                        ┌────────────────────┼────────────────────┐
                                        │                    │                    │
                                        ▼                    ▼                    ▼
                                    TCP/IP             TCP/IP                TCP/IP
                                    localhost          localhost            localhost
                                    :5000              :5000                :5000


                          ╔═══════════════════════════════════╗
                          │      ServidorLogs                 │
                          │      (servidor_logs.py)           │
                          │      socket.listen(5)             │
                          ╚═════════════┬═════════════════════╝
                                        │
                    ┌───────────────────┼───────────────────┐
                    │ Cliente 1         │ Cliente 2         │ Cliente N
                    │ (hilo)            │ (hilo)            │ (hilo)
                    │ recv/send          │ recv/send         │ recv/send
                    │                   │                   │
                    ▼                   ▼                   ▼
             JSON parsing        JSON parsing        JSON parsing
                    │                   │                   │
                    └───────────────────┼───────────────────┘
                                        │
                                logger.info/warn/error()
                                        │
                                        ▼
                            ┌──────────────────────┐
                            │ servidor_logs.log    │
                            │   Centralizado       │
                            └──────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

FLUJO DE DATOS
─────────────

1. USUARIO ACCION
   └─► main.py (GUI) ─── Click en botón (ej: crear artista)

2. CONTROLADOR CRUD
   └─► ArtistaModel.agregar() ─── Crea registro en BD

3. OBSERVADORES EN ACCIÓN
   ├─► ObservadorLog.actualizar()
   │   └─► Escribe en app_discos.log (local)
   │
   └─► ObservadorClienteLogs.actualizar()
       └─► ClienteLogs.enviar_log()
           └─► Socket.send(JSON) ─── TCP a servidor

4. SERVIDOR RECIBE
   └─► ServidorLogs.manejar_cliente()
       ├─► JSON.parse()
       ├─► logger.info/warn/error()
       ├─► Escribe en servidor_logs.log
       └─► Envia confirmación al cliente


═══════════════════════════════════════════════════════════════════════════════

SECUENCIA TEMPORAL
──────────────────

    Tiempo
      ↓
      │
      ├─ T=0.0s  │ Usuario hace clic en "Agregar Artista"
      │
      ├─ T=0.1s  │ ArtistaModel.agregar(data) ejecutado
      │          ├─► Artista creado en BD
      │          └─► notificar("artista_agregado", datos)
      │
      ├─ T=0.15s │ ObservadorLog.actualizar() en paralelo
      │          └─► app_discos.log escrito
      │
      ├─ T=0.15s │ ObservadorClienteLogs.actualizar() en paralelo
      │          └─► ClienteLogs.enviar_log()
      │
      ├─ T=0.2s  │ JSON empaquetado y enviado al servidor
      │
      ├─ T=0.25s │ ServidorLogs recibe datos (en hilo separado)
      │          ├─► JSON parseado
      │          ├─► servidor_logs.log escrito
      │          └─► Confirmación enviada al cliente
      │
      └─ T=0.3s  │ ClienteLogs recibe confirmación
                 └─► "Log enviado" mostrado en terminal


═══════════════════════════════════════════════════════════════════════════════

ESTRUCTURA DE ARCHIVOS
──────────────────────

App Discos/
├── main.py                      ← Punto de entrada
├── model.py                     ← Clases CRUD + Observadores
├── controller.py                ← Controlador
├── views.py                     ← Interfaz gráfica
│
├── NUEVO: servidor_logs.py      ← Servidor TCP de logs
├── NUEVO: cliente_logs.py       ← Cliente TCP de logs
├── NUEVO: config_logs.py        ← Configuración centralizada
├── NUEVO: prueba_cliente_servidor.py ← Script de test
│
├── DOCUMENTACIÓN:
├── README_LOGS.md               ← Documentación completa
├── GUIA_RAPIDA_LOGS.md         ← Guía rápida
│
└── LOGS GENERADOS (en tiempo de ejecución):
    ├── app_discos.log           ← Logs locales de aplicación
    ├── cliente_logs.log         ← Logs del cliente
    ├── servidor_logs.log        ← Logs del servidor (centralizado)
    └── discos.db                ← Base de datos SQLite


═══════════════════════════════════════════════════════════════════════════════

COMUNICACIÓN JSON
─────────────────

CLIENTE ENVÍA (JSON):
{
    "evento": "artista_agregado",
    "datos": {
        "id": 1,
        "nombre": "The Beatles",
        "tipo": "Banda"
    },
    "nivel": "INFO",
    "cliente": "App-Discos"
}

SERVIDOR RESPONDE (JSON):
{
    "estado": "recibido",
    "evento": "artista_agregado"
}


═══════════════════════════════════════════════════════════════════════════════

MODOS DE OPERACIÓN
──────────────────

MODO 1: Solo Logs Locales
┌──────────────┐
│  App Discos  │
└──────┬───────┘
       │
       ├─► ObservadorLog → app_discos.log
       │
       └─► ObservadorClienteLogs → NO SE CONECTA (servidor no activo)
                                  → cliente_logs.log (logs locales solo)
           
Resultado: 1 archivo de log (app_discos.log)
Nota: Es la opción más segura para desarrollo


MODO 2: Logs Locales + Remoto
┌──────────────┐       ┌──────────────┐
│  App Discos  │ ───► │ServidorLogs  │
└──────────────┘       └──────────────┘
     │             │
     ├─► app_discos.log       │
     │             │
     ├─► cliente_logs.log     │
     │             │
     └─────────────► servidor_logs.log

Resultado: 3 archivos de log (todos sincronizados)
Nota: La opción recomendada para producción


═══════════════════════════════════════════════════════════════════════════════

NIVELES DE LOG POR OPERACIÓN CRUD
────────────────────────────────

CREATE:
  artista_agregado    → INFO   (verde)
  disco_agregado      → INFO   (verde)
  cancion_agregada    → INFO   (verde)

UPDATE:
  artista_actualizado     → WARNING (amarillo)
  disco_actualizado       → WARNING (amarillo)
  cancion_actualizada     → WARNING (amarillo)

DELETE:
  artista_eliminado   → ERROR  (rojo)
  disco_eliminado     → ERROR  (rojo)
  cancion_eliminada   → ERROR  (rojo)


═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(ARQUITECTURA)
