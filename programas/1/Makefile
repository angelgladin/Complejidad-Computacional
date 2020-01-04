.PHONY: all compile clean run

all:
	@echo "make clean"
	@echo "    Limpia el proyecto y elimina los archivos generados en el build."
	@echo "make run"
	@echo "    Ejecuta el programa."

clean:
	@rm -rf src/__pycache__ 2> /dev/null || true

run:
	@python3 src/clique.py