dev:
	ENVIRONMENT=dev MQTT_HOST=192.168.68.166 python -m fastapi dev src/main.py --host=0.0.0.0

prod:
	ENVIRONMENT=prod DATABASE_URL=sqlite+aiosqlite:////opt/espartan/database.db MQTT_HOST=192.168.68.166 uvicorn src.main:app --host 0.0.0.0

venv:
	python3 -m venv venv

reset: clean upgrade

clean:
	pip uninstall -y -r requirements.txt
	pip uninstall -y -r requirements.dev.txt

upgrade:
	pip install --upgrade pip wheel setuptools
	pip install --no-cache-dir --upgrade --upgrade-strategy eager --prefer-binary -e .[dev]

upgrade-prod:
	pip install --upgrade pip wheel setuptools
	pip install --no-cache-dir --upgrade --upgrade-strategy eager --prefer-binary -r requirements.txt

outdated:
	pip list --outdated

lint: autopep8 pycodestyle pylint

autopep8:
	autopep8 -i -r src --global-config setup.cfg

pycodestyle:
	pycodestyle src

pylint:
	pylint --recursive=y --fail-under=9.5 src

test:
	ENVIRONMENT=dev pytest --cov=src --cov-report=term --cov-report=lcov
