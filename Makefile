.PHONY: install test run clean

install:
	pip install -r requirements.txt

test:
	pytest tests/

run:
	streamlit run app.py

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
