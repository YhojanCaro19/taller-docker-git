# Etapa 1: build - instala dependencias (incluye herramientas de compilación si algún paquete las necesita)
FROM python:3.11-slim AS builder

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY src/main.py src/healthcheck.py ./

# Etapa 2: production - imagen final, solo con lo necesario para correr
FROM python:3.11-slim AS production

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app .

ENV PATH=/root/.local/bin:$PATH \
    PORT=3000

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python healthcheck.py || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
