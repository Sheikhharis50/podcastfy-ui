run:
	docker-compose -f docker-compose.yml up --build -d

stop:
	docker-compose -f docker-compose.yml down

logs:
	docker-compose -f docker-compose.yml logs -f

restart:
	docker-compose -f docker-compose.yml down && docker-compose -f docker-compose.yml up --build -d
