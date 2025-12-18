#!/bin/bash

case "$1" in
  build)
    docker-compose build
    ;;
  up)
    docker-compose up -d
    ;;
  down)
    docker-compose down
    ;;
  ingest)
    # Run ingestion script inside the backend container (ephemeral)
    echo "Starting ingestion..."
    # We use 'run' to execute the script in a new container instance, mounting necessary volumes
    docker-compose run --rm backend python -m app.rag.ingest
    ;;
  logs)
    docker-compose logs -f
    ;;
  *)
    echo "Usage: ./docker.sh {build|up|down|ingest|logs}"
    exit 1
    ;;
esac
