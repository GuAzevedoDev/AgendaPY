FROM python:3.12-slim

WORKDIR /app

# Copia so o requirements primeiro pra aproveitar o cache de camadas do Docker —
# o pip install so roda de novo quando requirements.txt muda, nao a cada
# alteracao de codigo (boa pratica).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Roda como usuario nao-root dentro do container (boa pratica de seguranca)
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
