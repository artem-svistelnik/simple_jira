ifeq (cmd, $(firstword $(MAKECMDGOALS)))
  runargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(runargs):;@true)
  ifeq ($(runargs),)
	runargs := backend bash
  endif
endif

build:
	docker build . -t simple-jira -f Dockerfile

run:
	docker compose up

restart:
	docker compose stop && docker compose up -d

stop:
	docker compose stop

cmd:
	docker compose run $(runargs)

dump:
	docker compose exec database pg_dump -U postgres -d postgres -f /dump.sql
	docker compose cp database:/dump.sql ./dump.sql

load:
	cat dump.sql | docker compose exec -T -u postgres database psql --port=5432