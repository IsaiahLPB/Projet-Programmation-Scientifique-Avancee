.PHONY: venv field_generator bindings solver post_processor

all: venv field_generator solver postproc

exp:
	make field_generator solver post_processor

venv:
	rm -rf psa_venv
	python3 -m venv psa_venv && \
	psa_venv/bin/pip install -r requirements.txt

field_generator:
	make -C field_generator/

bindings:
	make -C solver/src

solver:
	psa_venv/bin/python3 solver/src/main.py consts.JSON

post_processor:
	make -C post_processor/

