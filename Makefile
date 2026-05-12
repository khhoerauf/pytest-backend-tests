.PHONY: help install-virtual-environment install-dependencies api-tests lint format performance-tests performance-tests-clean
SHELL := /bin/bash

# Load .env if present
ifneq (,$(wildcard .env))
  include .env
  export
endif

install-virtual-environment:
	@echo "Installing Python virtual environment..."
	python3 -m venv .venv

install-dependencies:
	@echo "Installing python packages..."
	source .venv/bin/activate;
	pip3 install -r requirements.txt

api-tests:
	@echo "Running API tests..."
	source .venv/bin/activate;
	pytest -v;

lint:
	@echo "Running Flake8 to check code style and quality..."
	source .venv/bin/activate;
	flake8;

format:
	@echo "Formatting python code..."
	source .venv/bin/activate;
	black .;

performance-tests:
	@echo "Running JMeter performance tests..."
	mkdir -p jmeter/results
	rm -rf jmeter/results/report
	jmeter -n \
		-t jmeter/performance-tests.jmx \
		-l jmeter/results/results.jtl \
		-e -o jmeter/results/report \
		-Japi_key=$(API_KEY)

performance-tests-report:
	@echo "Opening JMeter HTML report..."
	open jmeter/results/report/index.html

performance-tests-clean:
	@echo "Cleaning JMeter results..."
	rm -rf jmeter/results
