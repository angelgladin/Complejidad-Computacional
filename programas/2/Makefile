.PHONY: all clean run_bin run_subset

all:
	@echo "make clean"
	@echo "    Limpia el proyecto y elimina los archivos generados en el build."
	@echo "make run"
	@echo "    Ejecuta el programa."

clean:
	@rm -rf src/__pycache__ 2> /dev/null || true

run_bin:
	@python3 src/bin_packing.py

run_subset:
	@python3 src/approx_subset_sum.py
