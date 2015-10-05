project := threadloop

flake8 := flake8
pytest := py.test -s --tb short --cov $(project) tests

test_args := --cov-report term-missing --cov-report xml

.DEFAULT_GOAL := test

.PHONY:install
install:
	pip install -r requirements-test.txt
	python setup.py develop

.PHONY: clean
clean:
	@find $(project) tests -name "*.pyc" -delete

.PHONY:test
test: clean lint
	PYTHONDONTWRITEBYTECODE=1 $(pytest) $(test_args)

.PHONY: lint
lint:
	$(flake8) $(project) tests
