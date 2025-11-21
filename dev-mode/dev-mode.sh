#!/bin/bash
sudo -v
echo "Development Mode Script"
opcion=$(whiptail --title "Modo de Desarrollo" --menu "Selecciona una opcion:" 10 60 3\
    "1" "[ACTIVAR]" \
    "2" "[DESACTIVAR]" 3>&1 1>&2 2>&3)

if [ $? -ne 0 ]; then
    echo "Ejecución cancelada."
    exit 1
fi
function activar_servicios(){
# --- Configuración de Servicios ---
# Define los servicios que puedes activar. 
# Formato: "Nombre_Systemd" "Etiqueta_Mostrar" "ON/OFF"
SERVICES=(
    "postgresql" "PostgreSQL Database" "OFF"
    "docker"     "Docker Engine"       "OFF"
    "mongod"    "MongoDB Database"    "OFF"
)

# --- Crear la lista para Whiptail ---
# Inicializa la lista de servicios a seleccionar
whiptail_list=()
for ((i=0; i<${#SERVICES[@]}; i+=3)); do
    whiptail_list+=("${SERVICES[i]}" "${SERVICES[i+1]}" "${SERVICES[i+2]}")
done

SELECTED_SERVICES=$(whiptail --title "Inicializador de Servicios" --checklist "Seleccione los servicios a iniciar:" 16 40 10 \
    "${whiptail_list[@]}" 3>&1 1>&2 2>&3)

# Si el estado no es 0 (0 = OK, 1 = Cancelar, 255 = ESC)
if [ $? -ne 0 ]; then
    echo "Activación de servicios cancelada."
    exit 1
fi

# --- Iniciar Servicios Seleccionados ---

#sino se selecciono ningun servicio
if [ -z "$SELECTED_SERVICES" ]; then
    echo "No se seleccionaron servicios para iniciar."
    exit 0
fi

for SERVICE in $SELECTED_SERVICES; do
    # Elimina las comillas dobles
    SERVICE=$(echo $SERVICE | tr -d '"')
    
    echo "Iniciando servicio: $SERVICE"
    sudo systemctl start $SERVICE
    
    # si el servicio se inicio correctamente
    if [ $? -eq 0 ]; then
        echo "Servicio $SERVICE iniciado correctamente."
    else
        echo "Error al iniciar el servicio $SERVICE."
    fi
done

}
function desactivar_servicios(){
    SERVICES_TO_STOP=(
    "postgresql" 
    "docker"     
    "mongod"
    "docker.socket"
)
echo "Deteniendo servicios seleccionados..."
for SERVICE in "${SERVICES_TO_STOP[@]}"; do
    if systemctl is-active --quiet "$SERVICE"; then
        echo "Deteniendo servicio: $SERVICE"
        sudo systemctl stop "$SERVICE"
        
        if [ $? -eq 0 ]; then
            echo "Servicio $SERVICE detenido correctamente."
        else
            echo "Error al detener el servicio $SERVICE."
        fi
    else
        echo "El servicio $SERVICE no está activo."
    fi
done

}
if [ "$opcion" = 1 ]; then
    activar_servicios
elif [ "$opcion" = 2 ]; then
    desactivar_servicios
fi