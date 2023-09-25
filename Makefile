up_services:
	docker-compose --env-file .env -f docker-compose.yaml up -d
down_services:
	docker-compose --env-file .env -f docker-compose.yaml down
