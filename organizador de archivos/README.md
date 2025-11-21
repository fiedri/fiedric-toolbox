# Organizador de archivos con python
Esta carpeta contiene un conjunto de scripts hechos con Python diseñados para mantener tus carpetas ordenadas,  clasificando y moviendo archivos a subcarpetas según su tipo y extensión.

**Ofrece dos versiones:**
1. **Versión Interactiva (CLI):** Para una organización manual y bajo demanda, con interacción por consola.
2.  **Versión Automatizada (Silent):** Diseñada para funcionar en segundo plano con rutas predefinidas y notificaciones al sistema.

## Características

* **Organización Automática:** Clasifica archivos en categorías predefinidas (`imágenes`, `documentos`, `videos`, `audios`, `ejecutables`, `comprimidos`, `programación`, `fuentes`, `otros`).
* **Gestión de Duplicados:** Mueve archivos repetidos a subcarpetas `DUPLICADOS` dentro de cada categoría.
* **Modo Interactivo (CLI):** Interfaz amigable con [Rich] para seleccionar carpetas manualmente.
* **Modo Silencioso (Automatizado):** Funciona en segundo plano con rutas fijas y notificaciones del sistema al finalizar.


---

##  Instalación
- Descarga el script.
- Instala las dependencias necesarias con:

```bash
pip install -r requirements.txt
```
---
##  Uso

#### Versión 1: Interactiva (CLI) - `src/organizador.py`

1.  **Ejecutar el script.**
2.  **Interacción:**
    * Responde `Y` para organizar la carpeta actual, o `N` para arrastrar y soltar otra carpeta en la terminal.
3.  **Espera a que el proceso termine.**

#### Versión 2: Automatizada (Silent) - `src/organizer_downloads.py`

1.  **Personalizar:**
    Edita el archivo `src/config/rutas.txt` para definir las `rutas` absolutas de las carpetas a organizar. Las notificaciones solo funcionan en Windows 10+; si usas otro sistema operativo, deberás quitar el código de notificaciones.

2.  **Ejecutar (para prueba manual):**
    Puedes ejecutar este script directamente desde la terminal para probarlo. No mostrará nada en consola, pero enviará una notificación al sistema al finalizar (si estás en Windows).

    ```bash
    python src/organizer_downloads.py
    ```


4.  **Programa con el Programador de Tareas** para una ejecución automática regular.

---

## 📁 Estructura de carpetas

Al ejecutar el script, se crearán subcarpetas automáticamente según el tipo de archivo. Estas son las categorías por defecto:

- `imagenes`: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.tiff`, `.jfif`
- `videos`: `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`
- `audios`: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.wma`
- `documentos`: `.pdf`, `.doc`, `.docx`, `.txt`, `.xls`, `.xlsx`, `.xlsb`, `.ods`, `.csv`, `.ppt`, `.pptx`, `.odt`, `.epub`
- `ejecutables y sistema`: `.exe`, `.msi`, `.app`, `.bat`, `.sh`, `.dll`
- `comprimidos`: `.zip`, `.rar`, `.7z`, `.tar.gz`, `.iso`
- `programacion`: `.html`, `.css`, `.js`, `.py`, `.json`, `.xml`, `.sql`
- `fuentes`: `.ttf`, `.otf`, `.woff`, `.woff2`
- `otros`: cualquier archivo que no coincida con las categorías anteriores
- `DUPLICADOS`: subcarpetas dentro de cada categoría donde se colocan archivos repetidos

---
## 🛠️ Posibles Modificaciones y Personalización

Este proyecto es una base sólida. Aquí te sugiero algunas formas en las que podrías modificarlo y mejorarlo aún más:

### 1. Gestión Avanzada de Archivos

* **Archivado por antigüedad:** Mueve automáticamente archivos no accedidos/modificados en un periodo definido (ej. 3, 6, 12 meses) a una carpeta de archivo (`Archivados/`) para mantener la carpeta principal más limpia.

### 2. Retroalimentación y Registro (Logging) Mejorados

* **Registro persistente:** Extiende el sistema de logging para escribir en un archivo de texto (`log.txt`) con el historial detallado de cada ejecución, incluyendo archivos movidos, errores y un resumen final.
* **Notificaciones enriquecidas:** Las notificaciones del sistema podrían incluir un resumen conciso (ej. "Organización completada: 10 imágenes, 5 documentos movidos") o un botón para abrir el log de la última ejecución.
* **Reportes periódicos:** Genera reportes semanales/mensuales que resuman la actividad de organización a lo largo del tiempo.

### 3. Personalización del Usuario

* **Archivo de configuración:** Crea un archivo de configuración externo (ej. `config.ini` o `config.json`) para que el usuario defina rutas, categorías de archivo y sus extensiones, y opciones de notificaciones/logs, facilitando la personalización sin modificar el código.
* **Reglas personalizadas:** Permite al usuario definir reglas más complejas, como mover archivos con palabras clave específicas (ej. "invoice") a carpetas predefinidas ("Facturas") independientemente de su extensión.
