#!/bin/sh
set -e

# Espera o Postgres aceitar conexoes antes de seguir — evita o Gunicorn
# subir e a primeira request cair com erro de conexao recusada, comum
# quando o container do banco ainda esta inicializando.
if [ -n "$DATABASE_URL" ]; then
    python - <<'EOF'
import os
import sys
import time
from urllib.parse import urlparse

url = urlparse(os.environ["DATABASE_URL"])
host = url.hostname or "localhost"
port = url.port or 5432

import socket

for tentativa in range(30):
    try:
        with socket.create_connection((host, port), timeout=2):
            sys.exit(0)
    except OSError:
        time.sleep(1)

print(f"Nao foi possivel conectar em {host}:{port} apos 30 tentativas", file=sys.stderr)
sys.exit(1)
EOF
fi

# Aplica migrations pendentes antes de servir trafego.
flask db upgrade

# exec substitui o processo do shell pelo Gunicorn, garantindo que ele
# receba SIGTERM/SIGINT diretamente (senao o shell fica no meio e o
# container demora/ignora o shutdown gracioso).
exec gunicorn -c gunicorn.conf.py app:app
