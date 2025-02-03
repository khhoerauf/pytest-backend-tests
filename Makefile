.PHONY: help install-virtual-environment install-dependencies api-tests lint format
SHELL := /bin/bash

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