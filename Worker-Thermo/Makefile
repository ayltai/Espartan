BOARD    = ESP32-C3
BAUD     = 460800
# FIRMWARE = ~/Downloads/ESP32_GENERIC_C3-20250911-v1.26.1.bin
FIRMWARE = ~/Downloads/ESP32_GENERIC_C3-20251208-v1.27.0-preview.503.g2bd337ef18.bin

run:
	PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python main.py

venv:
	python3 -m venv venv

reset: clean upgrade

clean:
	pip uninstall -y -r requirements.txt

upgrade:
	mkdir -p esparknode
	rm -rf ./esparknode/*
	cp -r ../../espark/espark-node/esparknode ./
	cp -f ../../espark/espark-node/Makefile.template ./Makefile
	pip install --upgrade --upgrade-strategy eager --no-cache-dir --prefer-binary -r requirements.txt

outdated:
	pip list --outdated

lint: autopep8 pycodestyle pylint

autopep8:
	PYTHONPATH=. autopep8 -i -r src --global-config setup.cfg

pycodestyle:
	PYTHONPATH=. pycodestyle src

pylint:
	PYTHONPATH=. pylint --recursive=y --fail-under=9.5 src

test:
	PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 pytest --cov=src --cov-report=term --cov-report=lcov

flash:
	esptool erase-flash
	esptool --chip ${BOARD} -b ${BAUD} --before default-reset --after hard-reset write-flash 0 ${FIRMWARE}

deploy:
	mpremote connect /dev/ttyACM0 cp -rf ./esparknode :/
	mpremote connect /dev/ttyACM0 cp -rf ./src :/
	mpremote connect /dev/ttyACM0 cp -f ./main.py :/main.py

rm:
	mpremote connect /dev/ttyACM0 fs rm :/main.py
	mpremote connect /dev/ttyACM0 fs rm -r :/src
	mpremote connect /dev/ttyACM0 fs rm -r :/esparknode

ls:
	mpremote connect /dev/ttyACM0 fs ls :/
