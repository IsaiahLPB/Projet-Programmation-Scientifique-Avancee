.PHONY: 	

venv:
	python3 -m venv psa_venv
	source psa_venv/bin/activate
	pip install numpy
	pip install matplotlib
	pip install swig
	pip install setuptools

