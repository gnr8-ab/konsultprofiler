.PHONY: venv activate sync run

venv:
	uv venv

activate:
	.venv\Scripts\activate

sync:
	uv pip install docxtpl streamlit

run:
	streamlit run src/konsultprofiler/app.py

setup: venv activate sync

all: setup run 