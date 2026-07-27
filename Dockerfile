FROM python:3.12-slim

# Timezone do Brasil, senao o container roda em UTC e o datetime.now()
# do Python fica 3h a frente do horario real (causa bug de "horario ja passou")
ENV TZ=America/Sao_Paulo
RUN apt-get update && apt-get install -y --no-install-recommends tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

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
