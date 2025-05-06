.PHONY:  field_generator solver post_processor

all: venv bindings field_generator solver postproc

init: venv bindings

venv:
	@echo "=========== Creating a virtual environnement with useful modules ==========="
	@echo "..."
	@rm -rf psa_venv
	@python3 -m venv psa_venv && \
	psa_venv/bin/pip install -r requirements.txt > /dev/null
	@echo "====================== Virtual environnement created ======================="
	@echo ""
	@echo ""

bindings:
	@echo "========================== Creating C++ bindings ==========================="
	@echo "..."
	@make -s -C solver/src > /dev/null
	@echo "============================ Bindings created ============================="
	@echo ""
	@echo ""

exp:
	@echo "=========================== Computing solutions  ==========================="
	@make -s field_generator solver post_processor 
	@echo "========================== Comptation finished ============================"

field_generator:
	@make -s -C field_generator/

solver:
	@make -s -C solver/ run

post_processor:
	@make -s -C post_processor/

