.PHONY:  field_generator solver post_processor

all: venv bindings field_generator solver postproc

init: venv bindings

venv:
	rm -rf psa_venv
	python3 -m venv psa_venv && \
	psa_venv/bin/pip install -r requirements.txt

bindings:
	make -C src/solver/src

exp:
	field_generator solver post_processor

field_generator:
	make -C field_generator/

solver:
	make -C solver/ run

post_processor:
	make -C post_processor/

