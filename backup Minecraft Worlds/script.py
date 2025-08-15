import os, zipfile,datetime, time
from win10toast import ToastNotifier

fecha_actual = datetime.datetime.today().strftime('%d-%m-%Y')
notify = ToastNotifier()

def create_backup(mc_world_dir, backup_dir, log_file):
    os.makedirs(MC_BACKUP_DIR, exist_ok=True)
    for world in os.listdir(mc_world_dir):
        world_path = os.path.join(mc_world_dir, world)
        if os.path.isdir(world_path):
            backup_zip_path = os.path.join(backup_dir, world + '.mcworld')
            try:
                with zipfile.ZipFile(backup_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(world_path):
                        #os.walk, recorre recursivamente un directorio
                        for file in files:
                            abs_file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_file_path, world_path)
                            zipf.write(abs_file_path, rel_path)
                        for dir in dirs:
                            abs_dir_path = os.path.join(root, dir)
                            rel_path = os.path.relpath(abs_dir_path, world_path)
                            zipf.write(abs_dir_path, rel_path)
                log_file.write(f"Resguardo del mundo {world} creado exitosamente\n")
            except Exception as e:
                log_file.write(f"Error al crear el backup del mundo {world}: {e}")

if __name__ == "__main__":
    MC_WORLD_DIR = "C:/Users/USUARIO/AppData/Local/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/LocalState/games/com.mojang/minecraftWorlds"
    MC_BACKUP_DIR = "E:/documentos/mundominecraft"
    backup_log_file = os.path.join(MC_BACKUP_DIR, "backup_log.txt")
    
    with open(backup_log_file, "w", encoding="utf-8") as log_file:
        log_file.write("----- Registro de Resguardo -----\n")
    with open(backup_log_file, "a", encoding="utf-8") as log_file:
        log_file.write(f"Resguardo del dia: {fecha_actual}\n")
        if os.path.exists(MC_WORLD_DIR):
            create_backup(MC_WORLD_DIR, MC_BACKUP_DIR, log_file)
        else:
            log_file.write("El directorio de mundos de minecraft no existe")
    notify.show_toast("Resguardo de mundos de Minecraft", f"Resguardo a la fecha: {fecha_actual}", icon_path= './icon.ico', duration=5)
    time.sleep(5)