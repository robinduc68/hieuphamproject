FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# print() / stdout hiện ngay trong `docker compose logs` (không bị buffer)
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["sh", "-c", \
  "python -u -m app.migrations.runner upgrade && \
   python -u -m app.seed && \
   python -u -m uvicorn app.main:app --host 0.0.0.0 --port 8000 \
     --proxy-headers --forwarded-allow-ips='*'"]
