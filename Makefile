setup:
	python -m venv .venv && . .venv/bin/activate
	poetry install
	. .venv/bin/activate && pre-commit install --hook-type pre-commit --hook-type pre-push

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

test-prepush: clean
	. .venv/bin/activate && pytest tests

pylint:
	. .venv/bin/activate && pylint sumgraph tests --reports=y

black:
	. .venv/bin/activate && black sumgraph tests --check

check: mypy test pylint black
