# Generador de Códigos QR

Esta es una aplicación en Python que permite generar códigos QR en formato PNG o SVG a partir de texto o URLs. Los códigos QR generados se guardan automáticamente en una carpeta específica y se ofrece la opción de abrirlos directamente desde la aplicación. Ideal para proyectos personales o educativos.

## Características

- Genera códigos QR en dos formatos:
  - **PNG**: Imagen con fondo.
  - **SVG**: Imagen vectorial.
    - Puede elegir con fondo o sin fondo.
- Guarda los códigos QR generados en una carpeta llamada `Qr generados`.
- Permite personalizar el nombre del archivo generado.
- Ofrece la opción de abrir el archivo generado automáticamente.

## Requisitos

- Python 3.9 o superior.
- Librerías necesarias (instalarlas con `pip`):
  - [qrcode](https://pypi.org/project/qrcode/)

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias necesarias instalando el requirements o ejecutando:

   ```bash
   pip install qrcode[pil]

3. Ejecuta el archivo app.py para iniciar la aplicación.

## Uso

Al ejecutar la aplicación, selecciona el formato del código QR que deseas generar:

1.  **png** para PNG.
2.  **svg** para SVG.

Ingresa el texto o URL que deseas convertir en un código QR.

Escribe el nombre que deseas darle al archivo generado (o presiona Enter para usar el nombre predeterminado `codigo_qr`).

El código QR se generará y se guardará en la carpeta `Qr generados`.

Decide si deseas abrir el archivo generado directamente desde la aplicación.

