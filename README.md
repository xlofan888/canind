# 🇨🇦 CANIND — Canada Economic Command Center

CANIND is a free/open-source prototype dashboard for monitoring Canada's economic health, recession risk, trade exposure and economic transition.

## v0.1 goals

- 10 core indicators
- Recession Risk Score
- Economic Momentum Score
- Economic Breadth Score
- Transition Score
- Statistics Canada WDS connector
- Bank of Canada Valet connector
- SQLite storage
- Streamlit dashboard
- GitHub Actions daily refresh
- Safe fallback/demo data when APIs are unavailable

## Important

This is an analytical monitoring tool, not an official recession classifier or investment advice.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.pipeline
streamlit run app/dashboard.py
```

Open http://localhost:8501.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a new Streamlit Community Cloud app.
3. Select the repository.
4. Set the main file to `app/dashboard.py`.
5. Deploy.

The app uses SQLite by default, so no database server is required for v0.1.

## Data sources

Primary sources:
- Statistics Canada Web Data Service (WDS)
- Bank of Canada Valet API

v0.1 deliberately keeps CMHC/CREA/PMI adapters as placeholders so the core application remains runnable without commercial credentials.

## Licence

MIT
