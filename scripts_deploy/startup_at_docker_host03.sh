#!/bin/bash
#!/bin/bash
# Absoluut pad naar de directory waar dit script staat
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

rm $PROJECT_ROOT/docker-compose.yml
mv $PROJECT_ROOT/docker-compose-docker-host03.yml $PROJECT_ROOT/docker-compose.yml
rm -f $PROJECT_ROOT/app/logging_config.yml
mv $PROJECT_ROOT/app/logging_config_tmp_prd.yml $PROJECT_ROOT/app/logging_config.yml

docker build -t i2-kiss-api . 
docker compose up -d
