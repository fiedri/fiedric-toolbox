import os
from PIL import Image

def compress_image(input_path, output_path, quality=85, max_dimension=None):
    """
    Comprime una imagen y opcionalmente la redimensiona si excede una dimensión máxima.

    Args:
        input_path (str): Ruta completa de la imagen de entrada.
        output_path (str): Ruta completa para guardar la imagen comprimida.
        quality (int): Calidad de compresión (0-100). Más bajo = más compresión.
                      Solo aplica a formatos con pérdida como JPEG.
        max_dimension (int, optional): Si se especifica, redimensiona la imagen
                                       para que su lado más largo no exceda este valor.
                                       Mantiene la relación de aspecto.
    """
    try:
        img = Image.open(input_path)

        # Si se especifica una dimensión máxima, redimensionar
        if max_dimension:
            # Mantener la relación de aspecto
            img.thumbnail((max_dimension, max_dimension))

        # Determinar el formato de salida. Si es PNG, no usar 'quality' directamente
        # a menos que sea para optimización de PNG (que es diferente a la calidad JPEG)
        file_extension = os.path.splitext(output_path)[1].lower()

        if file_extension in ['.jpg', '.jpeg']:
            # Guardar como JPEG con la calidad especificada
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            print(f"Comprimida JPEG: {input_path} -> {output_path} (Calidad: {quality})")
        elif file_extension == '.png':
            # Para PNG, 'optimize=True' intenta reducir el tamaño
            # y 'compress_level' (0-9) puede ser usado para mayor compresión (más lento)
            img.save(output_path, "PNG", optimize=True, compress_level=9)
            print(f"Comprimida PNG: {input_path} -> {output_path} (Optimizado)")
        elif file_extension == '.webp':
            # Guardar como WebP (soporta calidad como JPEG)
            img.save(output_path, "WebP", quality=quality)
            print(f"Convertida a WebP: {input_path} -> {output_path} (Calidad: {quality})")
        else:
            # Para otros formatos, solo guardar sin compresión específica de calidad
            img.save(output_path)
            print(f"Imagen procesada (formato no JPEG/PNG/WebP): {input_path} -> {output_path}")

        original_size = os.path.getsize(input_path) / (1024 * 1024) # MB
        compressed_size = os.path.getsize(output_path) / (1024 * 1024) # MB
        print(f"Tamaño original: {original_size:.2f} MB, Tamaño comprimido: {compressed_size:.2ff} MB")
        print(f"Reducción: {((original_size - compressed_size) / original_size * 100):.2f}%")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{input_path}'")
    except Exception as e:
        print(f"Error al procesar '{input_path}': {e}")

def process_directory(input_dir, output_dir, quality=85, max_dimension=None, convert_to_webp=False):
    """
    Process all supported images in the input directory and compress them
    into the output directory. Optionally, convert all images to WebP.
    """
    input_dir = input_dir.strip().strip('"').strip("'")
    output_dir = output_dir.strip().strip('"').strip("'")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(
            f"Directorio de salida '{output_dir}' creado."
        )

    supported_extensions = (
        '.jpg', '.jpeg', '.png', '.webp'
    )

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            print(
                f"\nProcesando: {filename}"
            )
            compress_image(
                input_path,
                output_path,
                quality,
                max_dimension
            )
            # Si se solicita conversión a WebP y el archivo no es ya WebP
            if convert_to_webp and not filename.lower().endswith('.webp'):
                webp_filename = os.path.splitext(filename)[0] + '.webp'
                webp_output_path = os.path.join(output_dir, webp_filename)
                compress_image(
                    input_path,
                    webp_output_path,
                    quality,
                    max_dimension
                )
        else:
            print(
                f"Saltando archivo no soportado: {filename}"
            )
if __name__ == "__main__":
    # --- CONFIGURACIÓN ---
    input_directory = input("introduce directorio") # Crea esta carpeta y pon tus imágenes aquí
    output_directory = "images_comprimidas" # Aquí se guardarán las imágenes procesadas
    compression_quality = 80 # Para JPEG/WebP: 0 (peor) a 100 (mejor). Un buen punto de partida es 75-85.
    
    # Opcional: Redimensionar el lado más largo de la imagen a este valor (ej. 1920 para full HD)
    # Si no quieres redimensionar, déjalo como None
    max_image_dimension = 1920 # Por ejemplo, para imágenes de hero, o 800 para miniaturas
    convert_webp_prompt = (
        "¿Convertir todas las imágenes a WebP además de comprimirlas? (s/n, default: n): "
    )
    convert_to_webp = (
        input(convert_webp_prompt).strip().lower() == "s"
    )
    # --- EJECUCIÓN ---
    process_directory(input_directory, output_directory, compression_quality, max_image_dimension, convert_to_webp)
    print("\nProceso de compresión de imágenes finalizado.")