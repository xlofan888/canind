install:
	pip install -r requirements.txt

update:
	python -m src.pipeline

run:
	streamlit run app/dashboard.py

test:
	pytest

docker:
	docker compose up --build
