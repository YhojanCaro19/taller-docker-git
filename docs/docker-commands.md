# Comandos Docker Útiles (Cheatsheet)

## Levantar servicios
docker-compose up -d
docker-compose up --build -d        # Reconstruir imágenes
docker-compose up -d --scale api=3  # Escalar servicio

## Ver estado
docker-compose ps
docker-compose logs -f [servicio]
docker-compose top

## Gestión
docker-compose stop
docker-compose start
docker-compose restart [servicio]
docker-compose down
docker-compose down -v              # Eliminar también volúmenes

## Inspección
docker-compose exec [servicio] sh
docker-compose exec db psql -U postgres
docker-compose exec redis redis-cli

## Limpieza
docker system prune -f              # Eliminar dangling
docker volume prune -f              # Eliminar volúmenes no usados
docker-compose down --rmi all -v    # Todo limpio
