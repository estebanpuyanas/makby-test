.PHONY: help dependencies exercise1 exercise2 webviewer

help:
	@echo "Available commands:"
	@echo "make dependencies - configure environment + installs required dependencies to run the code."
	@echo "make exercise1 - runs the solution file for exercise 1"
	@echo "make exercise2 - runs the solution file for exercise 2"
	@echo "make webviewer - starts the localhost web viewer (http://localhost:5000)"

dependencies:
	@echo "Configuring environment and installing dependencies..."
	pyenv local 3.12.12 && \
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

exercise1:
	@echo "Running exercise 1 solution..."
	source .venv/bin/activate && \
	python3 -m src.exercise1.solution

exercise2:
	@echo "Running exercise 2 solution..."
	source .venv/bin/activate && \
	python3 -m src.exercise2.solution

webviewer:
	@echo "Starting web viewer at http://localhost:5000 ..."
	source .venv/bin/activate && \
	python3 webviewer/app.py