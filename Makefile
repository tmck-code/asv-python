build:
	docker build -t tmckcode/asv-python:latest -f Dockerfile .

shell:
	docker run -it -v $(PWD):/code tmckcode/asv-python:latest bash

test:
	docker run -t -v $(PWD):/code tmckcode/asv-python:latest pytest test/

.PHONY: build shell test