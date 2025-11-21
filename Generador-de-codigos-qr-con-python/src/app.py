import qrcode
import qrcode.image.svg
import time
import os
import subprocess

CARPETA = 'Qr generados'
ruta_actual = os.path.dirname(os.path.abspath(__file__))#devuelve un string con la ruta
ruta_padre = os.path.dirname(ruta_actual)#obtine la ruta padre
destine = os.path.join(ruta_padre, CARPETA)#une la ruta con la carpeta o con la otra ruta creada
os.makedirs(destine, exist_ok=True)#crea la carpeta si no existe, si existe no hace nada

print('Generador de codigos qr')
print('*' * 40)


while True:
    texto = input("Ingrese el texto o la url: ").strip()#strip elimina espacios que estén al principio o final del texto
    # evalua la longitud del texto
    if texto:#texto devuelve True si no esta vacio, lo que hace que la condicion se cumpla
        break
    print("El texto o la url no pueden estar vacios")

nombre_qr = input('ingrese el nombre que desea darle al archivo: ')

if not nombre_qr:#verifica si nombre_qr esta vacio, si lo esta se ejecuta esta condicion
    nombre_qr = "codigo_qr"


while True:
    formato = input('Escribe "png" o "svg", para elegir el formato: ').lower()
    #lower() tranforma la letra en minuscula
    if formato in("png", "svg"):#evaluo si formato tiene como valor "png" o "svg"
        break
    print("Seleccion no válida")

 # Creacion del codigo qr. Utilizamos la funcion .make()
 # lo generamos a partir del valor de la variable texto
if formato == "png":
    img = qrcode.make(texto)
else:
    fondo = input("¿Desea el QR con fondo? (s/n): ").strip().lower()
    while fondo not in ('s', 'n'):
        print('Escriba s o n')
        fondo = input("¿Desea el QR con fondo? (s/n): ").strip().lower()
    factory = qrcode.image.svg.SvgFillImage if fondo == "s" else qrcode.image.svg.SvgImage
    img = qrcode.make(texto, image_factory=factory)



print('Generado qr...')
time.sleep(2)
# la extension del archivo ira de acuerdo al valor de formato
print('Generado qr...')
ruta_qr = os.path.join(destine, f"{nombre_qr}.{formato}")
img.save(ruta_qr)
print('Codigo qr generado con exito')

print(f'archivo guardado en la ruta actual {destine}')

abrir = input('¿Desea abrir el archivo?(s/n): ')
if abrir.lower() == 's':
    if os.name == 'nt':
        os.startfile(ruta_qr)
    else:
        try:
            subprocess.run(['xdg-open', ruta_qr], check=True)
        except FileNotFoundError:
            print(f"[!] Error: No se encontró la herramienta 'xdg-open'. Asegúrate de que esté instalada.")
        except subprocess.CalledProcessError as e:
            print(f"[!] Error al abrir el archivo: {e}")
