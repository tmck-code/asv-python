build:
	docker build -t tmckcode/asv-python:latest -f Dockerfile .

shell:
	docker run -it tmckcode/asv-python:latest bash

test:
	docker run -t tmckcode/asv-python:latest pytest test/

.PHONY: build shell test