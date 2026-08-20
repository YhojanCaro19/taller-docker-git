# Escenario 2 — Ejercicio: API REST Node.js + PostgreSQL + pgAdmin

Variante del ejemplo guiado, con CRUD completo, migrations automáticas, validación de datos y administración vía pgAdmin.

## Requisitos cumplidos
1. Estructura completa del ejercicio (`Dockerfile`, `docker-compose.yml`, `Makefile`, `init-scripts/`, `src/`)
2. `DELETE /usuarios/:id`
3. `PUT /usuarios/:id`
4. Migrations con `init-scripts/01-init.sql` (se ejecuta automáticamente al iniciar PostgreSQL)
5. Variables de entorno en `.env` (no hardcodeadas) — ver `.env.example` como plantilla
6. pgAdmin como servicio adicional (puerto 5050)
7. Validación básica de datos (nombre y email) en la API
8. `Makefile` con atajos para los comandos más usados

## Cómo levantarlo

```bash
cp .env.example .env
# edita .env con tus propios valores si quieres
make build
```

## Comandos del Makefile
```bash
make up        # levanta los servicios (sin reconstruir)
make build     # reconstruye la imagen y levanta todo
make logs      # sigue los logs de todos los contenedores
make ps        # estado de los contenedores
make sh        # shell dentro del contenedor de la API
make test      # prueba /health, POST y GET /usuarios
make restart   # reinicia los servicios
make down      # detiene los servicios (conserva los datos)
make clean     # detiene y borra también los volúmenes
```

## Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio |
| GET | `/usuarios` | Lista todos los usuarios |
| POST | `/usuarios` | Crea un usuario (`{ "nombre": "...", "email": "..." }`) |
| PUT | `/usuarios/:id` | Actualiza un usuario existente |
| DELETE | `/usuarios/:id` | Elimina un usuario |

La API valida que `nombre` no esté vacío y que `email` tenga formato válido; si falla, responde `400` con el detalle del error.

## Accesos
- API: http://localhost:3001
- pgAdmin: http://localhost:5050 (login: `PGADMIN_EMAIL` / `PGADMIN_PASSWORD` definidos en `.env`)

## Detener

```bash
make down    # conserva los datos
make clean   # borra también los volúmenes
```

## Persistencia verificada
Se confirmó que los datos sobreviven a `docker compose restart` — la tabla `usuarios` sigue presente en PostgreSQL tras el reinicio.
