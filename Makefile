export PYTHONPATH := src

run:
	@poetry run uvicorn main:app --reload

test:
	@poetry run pytest -v

activate:
	@poetry shell

deactivate:
	@echo "No Poetry, o ambiente e uma sub-shell. Para desativar, basta digitar 'exit' e pressionar Enter."
