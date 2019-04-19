PROJECT_DIR_NAME:=management_django_service
ENTER_DJANGO:=docker-compose run djangoweb
DJANGO_USER_UID:=$(shell id -u)
build: ## build necessary stuff for our project to run (docker images)
	docker-compose build

run: ## start containers with docker-compose and attach to logs
	docker-compose up --no-build

rund: ## start containers with docker-compose (detached mode)
	docker-compose up --no-build -d

stop: ## stop all running containers for this project
	docker-compose stop

enter: ## enter the Django container (want to play freely with manage.py commands? just `make enter` and have fun)
	$(ENTER_DJANGO) sh

test:
	$(ENTER_DJANGO) pytest -v -m "not webtest"

flake:
	$(ENTER_DJANGO) flake8


test_all:	
	$(ENTER_DJANGO) pytest -v

test_func:	

	$(ENTER_DJANGO) pytest -v -m webtest

clean-py: ## clean python artifacts (cache, tests, build stuff...)
	find ./$(PROJECT_DIR_NAME) -name '*.pyc' -exec rm -f {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '*.pyo' -exec rm -f {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '*~' -exec rm -f {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '__pycache__' -exec rm -fr {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '*.egg-info' -exec rm -fr {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '*.egg' -exec rm -f {} +



