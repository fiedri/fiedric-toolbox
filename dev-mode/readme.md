# dev-mode.sh
Este script proporciona una simple interfaz de comandos para activar o desactivar servicios de desarrollo en un sistema linux.

## Funciones

- **Activar Servicios**: Inicia servicios seleccionados como PostgreSQL, Docker, and MongoDB.
- **Deactivar Servicios**: Detiene servicios predefinidos (PostgreSQL, Docker, MongoDB, docker.socket).

## Uso

1.  **Run the script**:
    ```bash
    ./dev-mode.sh
    ```
2.  **Selecciona una opcion**:
    -   `1`: Activar - Presenta una lista de servicios para seleccionar
    -   `2`: Deactivar - Detiene los servicios predefinidos.

## Manejo de servicios

El script actualmente maneja los siguientes servicios:

-   `postgresql` (PostgreSQL Database)
-   `docker` (Docker Engine)
-   `mongod` (MongoDB Database)
-   `docker.socket` (stopped during deactivation)

## Requerimentos

-   `whiptail`: For interactive menus.
