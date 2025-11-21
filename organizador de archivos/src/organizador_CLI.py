import os
import shutil
import sys
import time
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()
mensaje = r"""
   ____                                   _                     
  / __ \                                 (_)                    
 | |  | |  _ __    __ _    __ _   _ __    _   ____   ___   _ __ 
 | |  | | | '__|  / _` |  / _` | | '_ \  | | |_  /  / _ \ | '__|
 | |__| | | |    | (_| | | (_| | | | | | | |  / /  |  __/ | |   
  \____/  |_|     \__, |  \__,_| |_| |_| |_| /___|  \___| |_|   
                   __/ |                                        
                  |___/                                         

******************************************************************"""

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
}

def limpiar_consola():
    """Limpiar pantalla dependiendo del sistema operativo"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def pedir_ruta():
    """
    Retorna:
        str: Ruta absoluta de la carpeta a organizar.
    """
    usar_ruta_actual=Confirm.ask("[cyan]\n¿Organizar carpeta actual?[/cyan]")
    if usar_ruta_actual:
        return os.getcwd()#elige la carpeta donde ejecuto el script
    while not usar_ruta_actual:
        ruta=Prompt.ask("[cyan]\nArrastra y suelta la carpeta a organizar[/cyan]").strip("&").strip().strip("'").strip('"')
        if ruta:
            ruta = os.path.abspath(ruta)
            if os.path.isdir(ruta):
                return ruta
        console.print("[bold red]Ruta no valida[/bold red]")

def mover_archivo(origen, destino):
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

def organizar_carpeta(ruta, tipos, nombre):
    for archivo in os.listdir(ruta):
        if archivo == nombre:
            continue
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

if __name__== "__main__":
    limpiar_consola()
    console.print(mensaje, style="bold yellow")
    script_name = os.path.basename(sys.executable if getattr(sys, "frozen", False) else __file__)
    try:
        RUTA_FUENTE = pedir_ruta()
        with console.status("[bold green]Organizando carpeta...[/bold green]", spinner="dots"):
            # Simula una tarea larga
            organizar_carpeta(RUTA_FUENTE, tipos_de_archivo, script_name)
            time.sleep(2)
        console.print("[bold green]✅ Todo ha sido organizado[/bold green]")
        time.sleep(1)
        with console.status("[yellow]Cerrando...[yellow]", spinner="dots"):
            time.sleep(3)
    except Exception as e:
        print(f"Ocurrio un error: {e}")