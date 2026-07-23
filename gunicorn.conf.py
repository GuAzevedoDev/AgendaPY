import multiprocessing
import os

# Bind interno — o Nginx é quem fica exposto na porta 80/443, o Gunicorn só
# precisa ser alcançável pelo proxy (mesma rede docker ou localhost).
bind = os.environ.get("GUNICORN_BIND", "127.0.0.1:8000")

# App com no máx. ~10 usuários simultâneos: não há motivo pra formula
# (2 * cpu_count) + 1, que foi pensada pra servir tráfego público. 2 workers
# já cobre folga pra deploy/restart sem downtime; threads absorvem as
# requisições que ficam bloqueadas esperando o Postgres.
workers = int(os.environ.get("GUNICORN_WORKERS", 2))
threads = int(os.environ.get("GUNICORN_THREADS", 4))
worker_class = "gthread"

# Evita workers pendurados por conexão trava no DB ou request lento.
timeout = 30
graceful_timeout = 30
keepalive = 5

# Recicla workers periodicamente pra mitigar memory leaks de longa duração
# (com 10 usuários o processo pode ficar de pé por semanas sem restart).
max_requests = 500
max_requests_jitter = 50

# Importa a app uma vez no master e faz fork — inicia mais rápido e usa
# menos memória. Cada worker mantém seus próprios contadores do Flask-Limiter
# (storage em memória), o que é aceitável nessa escala.
preload_app = True

# Log direto pro stdout/stderr — o Docker/systemd journal já persiste.
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

# Nginx envia esses headers; sem isso request.is_secure e url_for(_external=True)
# não refletem o HTTPS terminado no proxy.
forwarded_allow_ips = "*"
