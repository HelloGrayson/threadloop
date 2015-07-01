project := threadloop

PHONY:install
install:
	pip install -r requirements-test.txt
	pip install -r requirements.txt

PHONY:test
test:
	PYTHONDONTWRITEBYTECODE=1 py.test -s tests
