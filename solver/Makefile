.PHONY: clean_data

all: bindings run display

bindings:
	make -C src/

run:
	../psa_venv/bin/python3 src/main.py ../consts.JSON

display:
	../psa_venv/bin/python3 display.py

tests:
	make -C tests/

clean:
	rm -f data/* 