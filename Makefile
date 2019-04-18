PROJECT_DIR_NAME:=management_django_service
ENTER_DJANGO:=docker-compose exec djangoweb
DJANGO_USER_UID:=$(shell id -u)
build: ## build necessary stuff for our project to run (docker images)
	@$(MAKE) clean-py || printf "\n\033[33mWasn't able to execute clean-py, maybe some file permissions issue! But build anyway.\033[0m\n\n"
	docker-compose build --build-arg DJANGO_USER_UID=$(DJANGO_USER_UID)

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



