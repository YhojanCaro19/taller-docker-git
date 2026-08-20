.PHONY: up build up-prod down logs ps restart clean sh test

up:
	docker compose up -d

build:
	docker compose up --build -d

up-prod:
	docker compose -f docker-compose.yml up --build -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

sh:
	docker exec -it redis_app_ej sh

clean:
	docker compose down -v

test:
	curl http://localhost:8001/health
	curl http://localhost:8001/contador
	curl http://localhost:8001/contador
	curl http://localhost:8001/usuarios
