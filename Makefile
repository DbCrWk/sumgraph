setup:
	python -m venv .venv && . .venv/bin/activate
	poetry install

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -f .coverage.*

clean: clean-pyc clean-test

mypy:
	. .venv/bin/activate && mypy sumgraph tests

test: clean
	. .venv/bin/activate && pytest tests --cov=sumgraph --cov-report=term-missing

pylint:
	. .venv/bin/activate && pylint sumgraph tests --reports=y

black:
	. .venv/bin/activate && black sumgraph tests --check

check: mypy test pylint black
