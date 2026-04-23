#!/bin/bash

if [ -z "$ROBOT_IMAGE" ]; then
  echo "ROBOT_IMAGE não está configurado!"
  exit 1
fi

echo "Iniciando o robô com a imagem: $ROBOT_IMAGE"

docker run --rm "$ROBOT_IMAGE"