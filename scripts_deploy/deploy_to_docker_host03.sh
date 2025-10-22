#!/bin/bash

# Configuratievariabelen
PRIVATE_KEY="/home/tom/.ssh/id_rsa_docker-host"
SERVER_USER="docker"
SERVER_IP="192.168.70.7"
BRON_MAP="./app"
DOEL_MAP="~/i2-kiss-api"

echo "Server IP: $SERVER_IP"
echo "Doelmap: $DOEL_MAP"
# 1. Verwijder de doelmap op de server als die bestaat
echo "🗑️ Verwijder doelmap op $SERVER_IP..."
ssh -i "$PRIVATE_KEY" "$SERVER_USER@$SERVER_IP" "rm -rf $DOEL_MAP"

# 2. Maak de doelmap opnieuw aan
echo "📂 Maak doelmap opnieuw aan..."
ssh -i "$PRIVATE_KEY" "$SERVER_USER@$SERVER_IP" "mkdir -p $DOEL_MAP"

# Kopieer bestanden met scp en specifieke sleutel
scp -i "$PRIVATE_KEY" -r "../app" "$SERVER_USER@$SERVER_IP:$DOEL_MAP/app"
scp -i "$PRIVATE_KEY" -r "../driver" "$SERVER_USER@$SERVER_IP:$DOEL_MAP/driver"
scp -i "$PRIVATE_KEY" -r "../.env" "$SERVER_USER@$SERVER_IP:$DOEL_MAP/.env"
scp -i "$PRIVATE_KEY" -r "../docker-compose-docker-host03.yml" "$SERVER_USER@$SERVER_IP:$DOEL_MAP/docker-compose.yml"
scp -i "$PRIVATE_KEY" -r "../Dockerfile" "$SERVER_USER@$SERVER_IP:$DOEL_MAP/Dockerfile"
scp -i "$PRIVATE_KEY" -r "../kiss_fc_api" "$SERVER_USER@$SERVER_IP:$DOEL_MAP"
scp -i "$PRIVATE_KEY" -r "../pyproject.toml" "$SERVER_USER@$SERVER_IP:$DOEL_MAP"
scp -i "$PRIVATE_KEY" -r "../uv.lock" "$SERVER_USER@$SERVER_IP:$DOEL_MAP"
scp -i "$PRIVATE_KEY" -r "../scripts_deploy/startup_at_docker_host03.sh" "$SERVER_USER@$SERVER_IP:$DOEL_MAP"

ssh -i "$PRIVATE_KEY" "$SERVER_USER@$SERVER_IP" "rm -f $DOEL_MAP/app/logging_config.yml"
ssh -i "$PRIVATE_KEY" "$SERVER_USER@$SERVER_IP" "mv $DOEL_MAP/app/logging_config_tmp_prd.yml $DOEL_MAP/app/logging_config.yml"

ssh -i "$PRIVATE_KEY" "$SERVER_USER@$SERVER_IP" "chmod +x $DOEL_MAP/startup_at_docker_host03.sh"
# Controleer of het succesvol was
if [ $? -eq 0 ]; then
    echo "✅ Kopiëren succesvol!"
else
    echo "❌ Er ging iets mis bij het kopiëren."
fi


