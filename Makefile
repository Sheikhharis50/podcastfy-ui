run:
	docker-compose -f deployment/docker-compose.yml up --build

stop:
	docker-compose -f deployment/docker-compose.yml down

logs:
	docker-compose -f deployment/docker-compose.yml logs -f

restart:
	docker-compose -f deployment/docker-compose.yml down && docker-compose -f deployment/docker-compose.yml up --build
