# Always start by activating the virtual environment: source .venv/bin/activate
.PHONY: venv activate sync run stop

venv:
	uv venv


sync:
	uv pip install docxtpl streamlit

run:
	streamlit run src/konsultprofiler/app.py

setup: venv activate sync

all: setup run

stop:
	-@rmdir /s /q .venv 2>nul || rm -rf .venv 