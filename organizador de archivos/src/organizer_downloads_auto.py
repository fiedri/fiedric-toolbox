import os
import shutil
import sys
from win10toast import ToastNotifier

notificar = ToastNotifier()
tipos_de_archivo = {
    "imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
    ".tiff", ".jfif", ".heic", ".heif", ".webp", ".ico"],
    "videos": [".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv",
    ".mpeg", ".mpg", ".3gp", ".m4v", ".vob"],
    "audios": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff", ".amr",".mid",],
    "documentos": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".xlsb", ".ods", ".csv",
    ".ppt", ".pptx", ".odt", ".epub", ".ppt", ".md", ".rtf", ".log"],
    "ejecutables y sistema": [".exe", ".msi", ".app", ".bat", ".sh", ".dll", ".deb", ".rpm", ".sys", ".bin"],
    "comprimidos": [".zip", ".rar", ".7z", ".tar.gz", ".iso", ".gz", ".bz2", ".xz", ".tar", ".cab", ".zst", ".lz"],
    "programacion": [".html", ".css", ".js", ".py", ".json", ".xml", ".sql", ".c", ".cpp", ".java", ".ts",
    ".yml"],
    "fuentes": [".ttf", ".otf", ".woff", ".woff2", ".fon", ".eot"],
    "Otros": []
}

def obtener_rutas(ruta_actual, archivo='rutas.txt'):
    """
    Obtener rutas escritas en el archivo config/rutas.txt
    """
    rutas_validas = []
    archivo_rutas = os.path.join(ruta_actual, 'config', archivo)
    with open(archivo_rutas, 'r', encoding='utf-8') as rutas:
        for linea in rutas:
            ruta = linea.strip()
            if ruta and os.path.exists(ruta):
                rutas_validas.append(os.path.abspath(ruta))
    
    return rutas_validas

def mover_archivo(origen, destino):
    try:
        if not os.path.exists(destino):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.move(origen, destino)
        else:
            carpeta_duplicados = os.path.join(os.path.dirname(destino), "DUPLICADOS")
            os.makedirs(carpeta_duplicados, exist_ok=True)
            base, ext = os.path.splitext(os.path.basename(origen))
            contador = 1
            nuevo_nombre = f"{base} ({contador}){ext}"
            nuevo_destino = os.path.join(carpeta_duplicados, nuevo_nombre)
            while os.path.exists(nuevo_destino):
                contador += 1
                nuevo_nombre = f"{base} ({contador}){ext}"
                nuevo_destino = os.path.join(carpeta_duplicados, nuevo_nombre)
            shutil.move(origen, nuevo_destino)
    except Exception:
        pass  # Silencia errores menores para ejecución automática

def organizar_carpeta(ruta, tipos):
    for archivo in os.listdir(ruta):
        archivo_path = os.path.join(ruta, archivo)
        if os.path.isfile(archivo_path):
            extension = os.path.splitext(archivo_path)[1]
            for categoria, extensiones in tipos.items():
                if extension in extensiones:
                    destino = os.path.join(ruta, categoria, archivo)
                    break
            else:
                destino = os.path.join(ruta, "Otros", archivo)
            mover_archivo(archivo_path, destino)
        elif os.path.isdir(archivo_path) and not archivo in tipos.keys():
            destino = os.path.join(ruta, "Carpetas", archivo)
            mover_archivo(archivo_path, destino)

if __name__== "__main__":
    ruta_script = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(os.path.dirname(__file__))
    ruta_icon = os.path.join(ruta_script, 'icon.ico')
    rutas = obtener_rutas(ruta_script)
    for rt in rutas:
        organizar_carpeta(rt, tipos_de_archivo)
    notificar.show_toast(
    "Organizador de archivos",            
    "✅ ¡Archivos de la carpeta descargas organizados!",  
    icon_path= ruta_icon,                    
    duration=10,                         
)