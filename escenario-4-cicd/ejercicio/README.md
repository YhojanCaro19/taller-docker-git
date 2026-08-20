# Escenario 4 — Ejercicio: CI/CD con GitHub Actions (FastAPI)

![Escenario 4 - CI/CD](https://github.com/YhojanCaro19/taller-docker-git/actions/workflows/escenario4-ci-cd.yml/badge.svg)

Variante del ejemplo guiado (que usaba Node.js), migrada a **FastAPI**, con tests obligatorios
antes del build, multi-stage Dockerfile, scan de vulnerabilidades con Trivy, y publicación en
**DockerHub y GitHub Container Registry (GHCR)** con tags semánticos.

## Requisitos cumplidos
1. Estructura completa del ejercicio
2. Aplicación en **FastAPI** en lugar de Node.js
3. El workflow (`.github/workflows/escenario4-ci-cd.yml`, en la raíz del repo — ver nota abajo):
   - Job `test`: corre `pytest` **antes** de cualquier build
   - Job `build-scan-push`: usa `needs: test`, así que **solo construye si los tests pasan**
   - Publica con tags semánticos (`vX.Y.Z`, `vX.Y`, `latest`) usando `docker/metadata-action`
   - Publica tanto en **DockerHub** como en **GHCR**
4. `docker-compose.prod.yml`: levanta la app usando la imagen ya publicada (no la construye)
5. Este README con badge de estado del workflow
6. **Multi-stage build** en el `Dockerfile` (`builder` → `production`)
7. **Scan de vulnerabilidades con Trivy** como paso del pipeline, antes de publicar

## Nota importante sobre la ubicación del workflow
GitHub Actions solo detecta workflows en `.github/workflows/` en la **raíz real del repositorio**,
sin importar la rama. Por eso `escenario4-ci-cd.yml` vive en la raíz del repo (`taller-docker-git/.github/workflows/`)
y no anidado dentro de esta carpeta, aunque el diagrama de la guía lo muestre así — anidado nunca se dispararía.

## Configuración necesaria en GitHub (antes de que funcione la publicación)
1. Settings → Secrets and variables → Actions
2. Agregar `DOCKERHUB_USERNAME`
3. Agregar `DOCKERHUB_TOKEN` (generado en DockerHub → Account Settings → Security → New Access Token)

Si no configuras estos secrets, el pipeline igual corre tests, build, scan y publica en **GHCR**
(usa el `GITHUB_TOKEN` automático) — solo se salta la publicación a DockerHub.

## Cómo levantarlo en local

```bash
cp .env.example .env
docker compose up --build -d
curl http://localhost:3002/
curl http://localhost:3002/health
```

## Cómo correr los tests en local

```bash
cd src
pip install -r requirements-dev.txt
pytest -v
```

## Cómo levantar usando la imagen publicada (modo "producción")

```bash
docker compose -f docker-compose.prod.yml up -d
```
(requiere `DOCKERHUB_USERNAME` en tu `.env`, y que el pipeline ya haya publicado al menos una vez)

## Disparar el pipeline con un tag semántico

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Ver el resultado del scan de Trivy
En GitHub → pestaña **Actions** → el run correspondiente → job `build-scan-push` → paso
"Escanear vulnerabilidades con Trivy". El scan es informativo (no bloquea el pipeline por
defecto); para hacerlo bloqueante, cambiar `exit-code: '0'` a `exit-code: '1'` en el workflow.
