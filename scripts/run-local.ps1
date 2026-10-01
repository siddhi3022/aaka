python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
uvicorn app.main:app --reload
