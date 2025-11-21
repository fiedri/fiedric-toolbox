# Como funciona scalffoldProjectjs
este se divide en una funcion principal que a su vez esta dividida en otras funciones

## funcion principal scaffoldProject()
- path.resolve() es una función del módulo nativo path de Node.js que construye una ruta absoluta a partir de fragmentos de rutas. Toma una secuencia de rutas o fragmentos y las combina, resolviendo .. y . para obtener la ruta final absoluta.
esta funcion se encarga de verificar que template se va usar, recibiendo las respuestas del usuario, y obteniendo las rutas necesarias, asi como crear la carpeta del proyecto, procesar los recursos del usuario

### processDirectory(sourceDir, destinationDir)
esta funcion le el directorio fuente obtiene un item comprueba si es una carpeta o un archivo, si es una carpeta la crea en el proyecto, y se llama a si misma con la direccion de esta carpeta como parametro sourceDir, si es un archivo be si incluye la palabra recourses que significa que debe crear un archivo por cada elemento en resouceLIst, y reemplaza el nombre para que no sea resource y llama a renderAndWriteFile, sino incluye la palabra significa que solo se debe reemplazar '.ejs'
De esta manera se recorre y se crean cada una de las carpetas dentro de la plantilla, al hacer que si una ruta lleva a una carpeta, se vuelve a llamar para crearla en proyecto, y luego pasa a lo que esta tiene adentro, al ya leer todos los archivos de esta, pasa a la otra

### renderAndWriteFile(sourceFile, destinationFile, data)
toma el archivo fuente y los datos, que seran reemplazados dentro de las plantillas, lee el contenido del archivo fuente, lo renderiza con ejs y luego escribe uno nuevo en la ruta, si termina con ejs, sino solamente lo copia