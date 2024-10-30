#!/bin/bash
# Устанавливаем строгий режим
set -e

python -m src.client.main & uvicorn src.api.main:app --host 0.0.0.0 --port 8000

exec "$@"
