import os
from PIL import Image

supported_extensions = (".jpg", ".jpeg", ".webp", ".png")

def comprimirImg(ruta):
    file_name, file_extension = os.path.splitext(ruta)
    print(file_extension)
    match file_extension.lower():
        case ".jpg" | ".jpeg":
            print('hola')
        case ".webp":
            print('hola')
        case ".png":
            print('hola')


def recorrerRuta(ruta, salida, quality=80, max_dimension = None, webp=False):
    if not os.path.exists(salida):
        os.makedirs(salida)
        print(f"Carpeta de salida {salida} creada")
    for file in os.listdir(ruta):
        if file.lower().endswith(supported_extensions):
            input_path = os.path.join(ruta,file)
            if webp and not file.lower().endswith('.webp'):
                web_file = os.path.splitext(file)[0] + '.webp'
                web_path = os.path.join(ruta, web_file)
                comprimirImg(input_path)
            comprimirImg(input_path)
        else:
            print(f'Saltando archivo no soportado {file}')    

if __name__ == "__main__":
    input_path = input("Ingresa la ruta de la/as imagenes").strip().strip('"').strip("'")
    output_path = input("Ingresa la ruta de salida").strip().strip('"').strip("'")
    convert_to_webp = input('¿Convertir a formato webp? (s/n) [n]: ').strip().lower()
    if convert_to_webp not in ('s', 'n'):
        convert_to_webp = 'n'
    quality = 85
    dimension = 1920
    recorrerRuta(input_path, output_path, quality,convert_to_webp) 

"""
1. aceptar la ruta donde estan las imagnes o la ruta de una imagen
2. seleccionar ruta de salida o tomar una por defecto
"""