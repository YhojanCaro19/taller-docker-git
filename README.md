# Taller Docker + Git

4 escenarios progresivos de Docker Compose, cada uno con un ejemplo guiado y un ejercicio propio.

## Escenarios

| # | Escenario | Rama | Estado |
|---|---|---|---|
| 1 | [WordPress + MySQL/MariaDB](./escenario-1-wordpress) | `main` (mergeada) | ✅ Completo |
| 2 | [API REST Node.js + PostgreSQL](https://github.com/YhojanCaro19/taller-docker-git/tree/escenario-2-api-node/escenario-2-api-node) | [`escenario-2-api-node`](https://github.com/YhojanCaro19/taller-docker-git/tree/escenario-2-api-node) | ✅ Completo |
| 3 | [App con caché Redis](https://github.com/YhojanCaro19/taller-docker-git/tree/escenario-3-redis/escenario-3-redis-cache) | [`escenario-3-redis`](https://github.com/YhojanCaro19/taller-docker-git/tree/escenario-3-redis) | ✅ Completo |
| 4 | [CI/CD con GitHub Actions](https://github.com/YhojanCaro19/taller-docker-git/tree/escenario-4-cicd/escenario-4-cicd) | [`escenario-4-cicd`](https://github.com/YhojanCaro19/taller-docker-git/tree/escenario-4-cicd) | ✅ Completo, pipeline verificado en verde |

Los escenarios 2, 3 y 4 viven en sus propias ramas (no están mezclados a `main`) — es el flujo de
trabajo que pide la guía, donde el merge a `main` es un paso opcional al finalizar. Para verlos,
usa los links de la tabla o cambia de rama en GitHub con el selector de ramas.

Cada carpeta de escenario tiene `ejemplo/` (la muestra guiada) y `ejercicio/` (la variante pedida,
con su propio `README.md` documentando requisitos cumplidos y cómo levantarlo).

## Estructura del repositorio
```
taller-docker-git/
├── docs/                          Cheatsheets de git y docker
├── escenario-1-wordpress/
│   ├── ejemplo/                   WordPress + MySQL
│   └── ejercicio/                 MariaDB + phpMyAdmin + .env
├── escenario-2-api-node/          (rama escenario-2-api-node)
│   ├── ejemplo/                   API Node.js + PostgreSQL
│   └── ejercicio/                 CRUD completo + pgAdmin + Makefile
├── escenario-3-redis-cache/       (rama escenario-3-redis)
│   └── ejercicio/                 FastAPI + Redis + Postgres, cache-aside, rate limiting
└── escenario-4-cicd/              (rama escenario-4-cicd)
    └── ejercicio/                 FastAPI + multi-stage + tests + Trivy + CI/CD
.github/workflows/escenario4-ci-cd.yml   Pipeline del Escenario 4 (vive en la raíz porque
                                          GitHub Actions solo lee workflows ahí)
```

## Flujo de trabajo
Ver [docs/git-workflow.md](./docs/git-workflow.md) y [docs/docker-commands.md](./docs/docker-commands.md).
