.PHONY: venv solver

all: venv fieldgen solver postproc

venv:
	rm -rf psa_venv
	python3 -m venv psa_venv && \
	psa_venv/bin/pip install -r requirements.txt

fieldgen:

solver:
	make -C solver/src
	psa_venv/bin/python3 solver/src/main.py 
	psa_venv/bin/python3 solver/src/display.py

postproc:

