.PHONY: help clean lint fmt mt-check test pre-commit bench

help:
	@echo ""
	@echo "Use 'make <command>'"
	@echo ""
	@echo "commands"
	@echo "  dev                start the application in development mode."
	@echo "  prod               start the application in production mode."
	@echo "  setup              setup dependancies for the entire project using docker."
	@echo "  clean				remove cleanable files"
	@echo "  lint				run linters"
	@echo "  fmt				run formaters"
	@echo "  fmt-check			run formatting check"
	@echo "  test				run all tests"
	@echo "  pre-commit			run pre-commit standardization"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

.venv:
	

clean:
	-@rm -rf .venv
	-@rm -fr `find . -name __pycache__`
	-@rm -rf .pytest_cache
	-@rm -rf .mypy_cache

lint: .venv
	

fmt: .venv
	

fmt-check: .venv
	

test: .venv
	

pre-commit: test fmt-check lint
	
