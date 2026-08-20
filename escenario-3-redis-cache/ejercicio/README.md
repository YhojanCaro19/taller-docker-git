# Escenario 3 — Ejercicio: App con caché Redis (FastAPI + PostgreSQL)

Variante del ejemplo guiado (que usaba Flask), migrada a FastAPI, con PostgreSQL como fuente de
verdad, Redis solo como capa de caché, contador de visitas, rate limiting, y configuración
separada para desarrollo vs producción.

## Requisitos cumplidos
1. Estructura completa del ejercicio (`docker-compose.yml`, `docker-compose.override.yml`, `app/`, `db/`)
2. Framework cambiado de Flask a **FastAPI**
3. `GET /contador`: contador de visitas usando `INCR` de Redis
4. **Rate limiting** con Redis: máximo 10 requests por minuto por IP (middleware global, responde `429` si se excede)
5. **PostgreSQL como fuente de verdad**, Redis solo como caché
6. `GET /usuarios`: patrón cache-aside — primero busca en Redis; si no está, busca en PostgreSQL y guarda el resultado en Redis (TTL 30s)
7. `docker-compose.override.yml` para desarrollo (hot-reload, bind mount) vs producción (imagen fija, sin volumen)
8. Healthchecks en los 3 servicios (`redis`, `db`, `app`)

## Cómo levantarlo

```bash
cp .env.example .env
# edita .env con tus propios valores si quieres
make build
```

Esto levanta en **modo desarrollo** (con hot-reload, porque `docker-compose.override.yml` se
aplica automáticamente). Para simular **producción** (sin bind mount, sin `--reload`):

```bash
make up-prod
```

## Comandos del Makefile
```bash
make up        # levanta los servicios (sin reconstruir)
make build     # reconstruye la imagen y levanta todo (modo desarrollo)
make up-prod   # levanta ignorando el override (modo producción)
make logs      # sigue los logs de todos los contenedores
make ps        # estado de los contenedores
make sh        # shell dentro del contenedor de la API
make test      # prueba /health, /contador (x2) y /usuarios
make restart   # reinicia los servicios
make down      # detiene los servicios (conserva los datos)
make clean     # detiene y borra también los volúmenes
```

## Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio (usado por el healthcheck) |
| GET | `/contador` | Incrementa y devuelve el contador de visitas (Redis `INCR`) |
| GET | `/usuarios` | Lista usuarios — cache-aside entre Redis y PostgreSQL |
| POST | `/usuarios` | Crea un usuario en PostgreSQL e invalida la caché |

Todas las rutas están protegidas por rate limiting: más de 10 requests en 60 segundos desde la
misma IP responden `429` con el tiempo restante hasta que se libera.

## Accesos
- API: http://localhost:8001
- Redis: `localhost:6380` (puerto host distinto al Escenario 3 del ejemplo, para poder correr ambos a la vez)
- PostgreSQL: `localhost:5433`

## Detener

```bash
make down    # conserva los datos
make clean   # borra también los volúmenes
```

## Persistencia verificada
Se confirmó que los usuarios en PostgreSQL sobreviven a `docker compose restart`.
