from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import redis
import psycopg2
import psycopg2.extras
import os
import json

app = FastAPI(title="App con caché Redis (ejercicio) - FastAPI")

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", 5432)
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_NAME = os.environ.get("DB_NAME", "cachedb")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

RATE_LIMIT_MAX = 10
RATE_LIMIT_WINDOW = 60  # segundos

USUARIOS_CACHE_KEY = "usuarios_cache"
USUARIOS_CACHE_TTL = 30  # segundos


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
    )


@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    """Rate limiting: máximo RATE_LIMIT_MAX requests por RATE_LIMIT_WINDOW segundos, por IP."""
    ip = request.client.host if request.client else "desconocido"
    key = f"ratelimit:{ip}"
    actuales = redis_client.incr(key)
    if actuales == 1:
        redis_client.expire(key, RATE_LIMIT_WINDOW)
    if actuales > RATE_LIMIT_MAX:
        ttl = redis_client.ttl(key)
        return JSONResponse(
            status_code=429,
            content={
                "error": "Demasiadas solicitudes, intenta de nuevo más tarde",
                "retry_after_segundos": ttl,
            },
        )
    return await call_next(request)


@app.get("/")
def index():
    return {"servicio": "App con caché Redis (ejercicio - FastAPI)", "status": "activo"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/contador")
def contador():
    """Contador de visitas usando INCR de Redis."""
    visitas = redis_client.incr("contador_visitas")
    return {"visitas": visitas}


@app.get("/usuarios")
def listar_usuarios():
    """Patrón cache-aside: primero busca en Redis; si no está, busca en
    PostgreSQL (fuente de verdad) y guarda el resultado en Redis."""
    datos_cache = redis_client.get(USUARIOS_CACHE_KEY)
    if datos_cache:
        return {"origen": "cache", "usuarios": json.loads(datos_cache)}

    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, nombre, email, creado_en FROM usuarios ORDER BY id")
        usuarios = cur.fetchall()
        cur.close()
    finally:
        conn.close()

    usuarios_json = json.loads(json.dumps(usuarios, default=str))
    redis_client.setex(USUARIOS_CACHE_KEY, USUARIOS_CACHE_TTL, json.dumps(usuarios_json))
    return {"origen": "postgres", "usuarios": usuarios_json}


@app.post("/usuarios")
def crear_usuario(payload: dict):
    """Inserta en PostgreSQL (fuente de verdad) e invalida la caché de Redis."""
    nombre = payload.get("nombre")
    email = payload.get("email")
    if not nombre or not email:
        raise HTTPException(status_code=400, detail="nombre y email son obligatorios")

    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id, nombre, email, creado_en",
            (nombre, email),
        )
        nuevo = cur.fetchone()
        conn.commit()
        cur.close()
    finally:
        conn.close()

    redis_client.delete(USUARIOS_CACHE_KEY)
    return json.loads(json.dumps(nuevo, default=str))
