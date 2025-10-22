#!/bin/bash

# Configuratievariabelen
SERVER_IP="10.116.0.50"
DOEL_MAP="/home/tom/deployed/i2-kiss-api"

echo "Server IP: $SERVER_IP"
echo "Doelmap: $DOEL_MAP"
# 1. Verwijder de doelmap op de server als die bestaat
echo "🗑️ Verwijder doelmap op $SERVER_IP..."
rm -rf $DOEL_MAP

# 2. Maak de doelmap opnieuw aan
echo "📂 Maak doelmap opnieuw aan..."
mkdir -p $DOEL_MAP

# Kopieer bestanden met scp en specifieke sleutel
cp -r ../app "$DOEL_MAP/app"
cp -r ../driver "$DOEL_MAP/driver"
cp -r ../.env "$DOEL_MAP/.env"
cp -r ../docker-compose-dev-vm-tom.yml "$DOEL_MAP/docker-compose.yml"
cp -r ../Dockerfile "$DOEL_MAP/Dockerfile"
cp -r ../kiss_fc_api "$DOEL_MAP"
cp -r ../pyproject.toml "$DOEL_MAP"
cp -r ../uv.lock "$DOEL_MAP"
cp -r ../scripts_deploy/startup_at_dev_vm_tom.sh "$DOEL_MAP"

rm -f $DOEL_MAP/app/logging_config.yml
mv $DOEL_MAP/app/logging_config_tmp_prd.yml $DOEL_MAP/app/logging_config.yml

chmod +x $DOEL_MAP/startup_at_dev_vm_tom.sh


