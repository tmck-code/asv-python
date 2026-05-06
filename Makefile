# if NO_CACHE is set to 1, then we pass the --no-cache flag to docker build
NO_CACHE ?= ""
CACHE_ARG = $(if $(filter 1,$(NO_CACHE)),--no-cache,)

build:
	docker build \
		$(CACHE_ARG) \
		--build-arg UID=$(shell id -u) \
		--build-arg GID=$(shell id -g) \
		-t tmckcode/asv-python:latest \
		.

shell:
	docker run -it \
		-v $(PWD):/code \
		tmckcode/asv-python:latest \
		python3

test:
	docker run -t \
		-v $(PWD)/asv:/app/asv \
		-v $(PWD)/test:/app/test \
		tmckcode/asv-python:latest \
		sh -c 'pytest -vv test/'

.PHONY: build shell test
