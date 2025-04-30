.PHONY: venv

venv:
	rm -rf psa_venv
	python3 -m venv psa_venv && \
	psa_venv/bin/pip install -r requirements.txt
