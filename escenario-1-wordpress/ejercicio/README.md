# Escenario 1 — Ejercicio: WordPress + MariaDB + phpMyAdmin

Variante del ejemplo guiado, usando MariaDB en vez de MySQL y agregando phpMyAdmin para administrar la base.

## Requisitos cumplidos
1. MariaDB 10.11 en lugar de MySQL
2. phpMyAdmin como servicio adicional (puerto 8081)
3. Variables de entorno en `.env` (no hardcodeadas) — ver `.env.example` como plantilla
4. Volumen nombrado personalizado: `mi_wordpress_data`
5. Red personalizada: `mi_red_wordpress`

## Cómo levantarlo

```bash
cp .env.example .env
# edita .env con tus propios valores si quieres
docker compose up -d
```

## Accesos
- WordPress: http://localhost:8082
- phpMyAdmin: http://localhost:8081 (usuario/password: los definidos en `.env`, variables MYSQL_USER / MYSQL_PASSWORD)

## Detener

```bash
docker compose down       # conserva los datos
docker compose down -v    # borra también los volúmenes
```

## Persistencia verificada
Se confirmó que los datos sobreviven a `docker compose restart` — las tablas de WordPress siguen presentes en MariaDB tras el reinicio.
