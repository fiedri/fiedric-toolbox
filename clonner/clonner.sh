#!/bin/bash

USER=$1

if [[ -z $USER ]]
then
    echo Ningun parametro encontrado
    exit 1
fi

echo "--- Iniciando extracción de: $USER ---"

mkdir -p "$USER"

cd "$USER" || exit

gh repo list "$USER" --limit 1000 --json name --jq '.[].name' | xargs -I {} gh repo clone "$USER/{}"

echo "--- El código de $USER ahora es parte de tu imperio. ---"