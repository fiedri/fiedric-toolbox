# 🛡️ Guía de Usuario: USB-Purge

USB-Purge es una herramienta de limpieza profunda diseñada para desinfectar memorias USB comprometidas por malware (especialmente aquellos que ocultan archivos, crean accesos directos o usan archivos autorun).

## 🚀 Flujo de Trabajo del Script

El proceso se divide en 5 etapas críticas para garantizar que el malware no se propague a tu computadora:

### 1. Detección y Selección
- El script identifica unidades extraíbles conectadas al sistema.
- **Seguridad**: Requiere privilegios de Administrador para poder formatear y aplicar inmunización a bajo nivel.

### 2. Análisis Heurístico e Aislamiento (Fase Crítica)
Antes de tocar el USB, el script analiza cada archivo y decide si es seguro moverlo a una carpeta temporal en tu PC (`USB_RECOVERY_ROOT`):
- **Lista Blanca**: Archivos comunes como `.jpg`, `.pdf`, `.docx`, `.txt`, etc., se consideran seguros inicialmente.
- **Lista Negra de Riesgo**: Se bloquean automáticamente archivos `.exe`, `.bat`, `.vbs`, `.ps1`, `.lnk`, entre otros.
- **Bloqueo por Nombre**: Archivos como `autorun.inf`, `desktop.ini` o `thumbs.db` son eliminados por ser vectores típicos de infección.
- **Análisis de Entropía**: Si un archivo tiene una extensión desconocida pero su estructura interna parece estar cifrada o empaquetada (alta entropía), se marca como riesgoso por sospecha de ransomware o malware oculto.

### 3. Limpieza Total (Wipe)
Una vez que los archivos "buenos" están a salvo en tu PC:
- El script desmonta la unidad.
- Realiza un **formateo rápido en FAT32** para eliminar cualquier rastro de malware persistente en el sistema de archivos.

### 4. Restauración e Inmunización
- Los archivos seguros se mueven de vuelta al USB limpio.
- **Inmunización de Autorun**: Se crea una carpeta especial llamada `autorun.inf` con nombres de archivos reservados del sistema (`con`, `nul`, `aux`, `prn`). 
  - *¿Por qué?* Windows no permite que el malware cree un archivo `autorun.inf` si ya existe una carpeta con ese nombre que el sistema no puede borrar ni sobrescribir fácilmente.

### 5. Reporte Final
Se genera un archivo `purge_report.txt` en la carpeta del script con:
- Fecha y hora del proceso.
- Unidad procesada.
- Cantidad de archivos rescatados vs. archivos peligrosos eliminados.

---

## ⚠️ Notas Importantes
- **Archivos Eliminados**: Los archivos marcados como "Riesgosos" **NO** se recuperan. Si el script detecta un `.bat` malicioso, lo eliminará para proteger tu sistema.
- **Espacio en Disco**: El script verificará que tengas suficiente espacio en tu computadora para copiar temporalmente los archivos del USB antes de empezar.
- **Pausa de Seguridad**: Al finalizar, la ventana permanecerá abierta para que puedas leer el reporte antes de cerrarla.

## 🛠️ Requisitos
- **Windows**: Ejecutar el terminal (PowerShell o CMD) como Administrador.
- **Linux**: Ejecutar con `sudo`.
