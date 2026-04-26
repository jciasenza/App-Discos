# 🚀 GUÍA RÁPIDA: Sistema de Logs Cliente-Servidor

## Inicio Rápido

### Opción 1: Solo Logs Locales (Recomendado para inicio)
```bash
cd c:\Users\curej\Desktop\UTN\App Discos
python main.py
```
✓ Genera: `app_discos.log`

---

### Opción 2: Logs Locales + Servidor Centralizado

#### Terminal 1 - Inicia el Servidor
```bash
cd c:\Users\curej\Desktop\UTN\App Discos
python servidor_logs.py
```

Esperado:
```
✓ Servidor iniciado en localhost:5000
```

#### Terminal 2 - Ejecuta la Aplicación
```bash
cd c:\Users\curej\Desktop\UTN\App Discos
python main.py
```

Esperado:
```
✓ Conectado al servidor de logs remoto
```

✓ Genera:
- `app_discos.log` (local)
- `servidor_logs.log` (servidor)
- `cliente_logs.log` (cliente)

---

### Opción 3: Prueba Rápida del Cliente-Servidor

#### Terminal 1 - Servidor
```bash
python servidor_logs.py
```

#### Terminal 2 - Cliente de Prueba
```bash
python prueba_cliente_servidor.py
```

---

## 📋 Archivos Creados/Modificados

| Archivo | Función |
|---------|---------|
| `servidor_logs.py` | 🟢 **NUEVO** - Servidor que recibe y registra logs |
| `cliente_logs.py` | 🟢 **NUEVO** - Cliente que envía eventos al servidor |
| `config_logs.py` | 🟢 **NUEVO** - Configuración centralizada |
| `prueba_cliente_servidor.py` | 🟢 **NUEVO** - Script de prueba |
| `model.py` | 🔵 MODIFICADO - Agregado ObservadorClienteLogs |
| `main.py` | 🔵 MODIFICADO - Integración de cliente-servidor |
| `README_LOGS.md` | 🟢 **NUEVO** - Documentación completa |

---

## 🔍 Ver Logs Generados

### Windows PowerShell
```powershell
# Ver contenido
Get-Content app_discos.log
Get-Content servidor_logs.log
Get-Content cliente_logs.log

# Ver últimas líneas
Get-Content app_discos.log -Tail 10

# Monitorear en tiempo real
Get-Content app_discos.log -Tail 10 -Wait
```

### Windows CMD
```cmd
type app_discos.log
tail -f app_discos.log  (si tienes Git Bash)
```

---

## 🎯 Niveles de Log por Evento

```
📘 INFO      → Cuando se AGREGA algo (CREATE)
    ├─ artista_agregado
    ├─ disco_agregado
    └─ cancion_agregada

📙 WARNING   → Cuando se ACTUALIZA algo (UPDATE)
    ├─ artista_actualizado
    ├─ disco_actualizado
    └─ cancion_actualizada

📕 ERROR     → Cuando se ELIMINA algo (DELETE)
    ├─ artista_eliminado
    ├─ disco_eliminado
    └─ cancion_eliminada
```

---

## ⚙️ Cambiar Configuración

### Cambiar puerto (ejemplo: 8080)

**En `servidor_logs.py`:**
```python
servidor = ServidorLogs(host='localhost', puerto=8080)  # línea 83
```

**En `cliente_logs.py`:**
```python
cliente = ClienteLogs(host='localhost', puerto=8080)  # línea 9
```

**En `config_logs.py`:**
```python
SERVIDOR_CONFIG = {
    'puerto': 8080,  # Cambiar aquí
    ...
}
```

---

## 🐛 Solución de Problemas

### El servidor no inicia
```
✗ Error al iniciar servidor
```
**Solución:** El puerto 5000 está en uso
- Cambiar puerto en `servidor_logs.py` línea 83
- O matar el proceso: `netstat -ano | findstr :5000`

### El cliente no se conecta
```
⚠ No se pudo conectar al servidor - funcionando solo con logs locales
```
**Solución:** El servidor no está activo
- Iniciar servidor en otra terminal: `python servidor_logs.py`
- Verificar que puerto coincida en ambos lados (5000 por defecto)

### Los logs no aparecen
```
# Verificar ruta actual
cd c:\Users\curej\Desktop\UTN\App Discos
# Listar archivos
dir *.log
```

---

## 📊 Ejemplo de Salida

### Terminal del Servidor
```
✓ Servidor iniciado en localhost:5000
✓ Cliente conectado desde ('127.0.0.1', 54321)
📨 [App-Discos] Evento: artista_agregado | Datos: {'id': 1, 'nombre': 'The Beatles'}
📨 [App-Discos] Evento: disco_agregado | Datos: {'id': 1, 'titulo': 'Abbey Road'}
⚠ Evento: disco_actualizado | Datos: {'id': 1, 'data': {'anio': 1969}}
```

### Archivo `app_discos.log`
```
2026-04-26 10:30:45 - INFO - Evento: artista_agregado | Datos: <Artista object>
2026-04-26 10:30:50 - INFO - Evento: disco_agregado | Datos: <Discos object>
2026-04-26 10:31:00 - WARNING - Evento: disco_actualizado | Datos: {'id': 1, 'data': {'anio': 1969}}
```

### Archivo `servidor_logs.log`
```
2026-04-26 10:30:45 - INFO - Servidor iniciado en localhost:5000
2026-04-26 10:30:47 - INFO - Cliente conectado desde ('127.0.0.1', 54321)
2026-04-26 10:30:50 - INFO - [App-Discos] Evento: artista_agregado | Datos: {'id': 1, 'nombre': 'The Beatles'}
```

---

## 💡 Próximos Pasos

- [ ] Probar con solo logs locales: `python main.py`
- [ ] Iniciar servidor: `python servidor_logs.py`
- [ ] Ejecutar aplicación con servidor: `python main.py`
- [ ] Revisar archivos de log: `dir *.log`
- [ ] Probar prueba rápida: `python prueba_cliente_servidor.py`

---

## ❓ Preguntas Frecuentes

**P: ¿Necesito el servidor para que funcione la aplicación?**  
R: No, los logs locales funcionan sin servidor. El servidor es opcional para centralizar logs.

**P: ¿Qué pasa si el servidor falla?**  
R: La aplicación continúa funcionando con solo logs locales. Solo se pierden los logs remotos.

**P: ¿Puedo tener múltiples clientes conectados?**  
R: Sí, el servidor maneja múltiples clientes simultáneamente (máximo 5 por defecto).

**P: ¿Dónde se crean los archivos de log?**  
R: En el directorio actual de ejecución (normalmente `c:\Users\curej\Desktop\UTN\App Discos\`).

**P: ¿Puedo cambiar el formato de los logs?**  
R: Sí, en `config_logs.py` o directamente en el código de `logging.basicConfig()`.

