.PHONY: vtr video

all: vtr

vtr:
	@../psa_venv/bin/python3 main.py ../consts.JSON

video:
	./png_files/encode.sh

clean:
	rm -f vtr_files/*