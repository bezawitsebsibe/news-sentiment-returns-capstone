# News Sentiment ↔ Stock Returns (Capstone)

Finance-ready refactor of Week 1 project. Focus: reliability, tests, CI/CD, and an executive-friendly dashboard.

## Quickstart
```bash
# 1) Create and activate a virtual environment (Windows PowerShell example)
python -m venv .venv
. .venv/Scripts/Activate.ps1

# 2) Install requirements
pip install -r requirements.txt

# 3) Run tests
pytest -q

# 4) Try the end-to-end demo pipeline (uses synthetic data)
python -m src.pipeline.run_all --demo

# 5) Launch the dashboard (demo mode)
streamlit run app/streamlit_app.py -- --demo
```

### Notes on TA-Lib (optional)
If TA-Lib is difficult to install on your machine, this project uses `pandas-ta` by default.
Switch to TA-Lib by setting `TECH_LIB=talib` in `.env` and installing TA-Lib locally.
