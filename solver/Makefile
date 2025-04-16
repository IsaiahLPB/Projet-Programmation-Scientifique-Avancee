.PHONY: clean_data

all: bindings run display

bindings:
	make -C src/

run:
	../psa_venv/bin/python3 src/main.py 

display:
	../psa_venv/bin/python3 display.py

clean:
	rm -f data/*