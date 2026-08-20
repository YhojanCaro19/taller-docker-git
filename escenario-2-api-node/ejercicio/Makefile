.PHONY: up build down logs ps restart clean sh test

up:
	docker-compose up -d

build:
	docker-compose up --build -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

ps:
	docker-compose ps

sh:
	docker exec -it api_node_ej sh

clean:
	docker-compose down -v

test:
	curl http://localhost:3001/health
	curl -X POST http://localhost:3001/usuarios \
		-H "Content-Type: application/json" \
		-d '{"nombre":"Juan","email":"juan@test.com"}'
	curl http://localhost:3001/usuarios
