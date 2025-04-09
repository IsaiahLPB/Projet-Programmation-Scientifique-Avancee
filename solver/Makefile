.PHONY: clean_data

ALG_ID = 0

all: bindings run display

bindings:
	make -C src/

run:
	../psa_venv/bin/python3 src/main.py $(ALG_ID)

display:
	../psa_venv/bin/python3 display.py $(ALG_ID)

clean:
	rm -f data/*