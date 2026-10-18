# AI Ticket Triage 🎫

**GitHub-ready AI / NLP portfolio project** — customer support ticket category and priority prediction with team routing suggestions.

> **Data caveat:** Training examples are **fully synthetic**. The model is a functional demonstration only; synthetic test accuracy does not establish performance on real support tickets. Review outputs before taking action. Do not upload sensitive customer data.

## Features
- Classify ticket into one of five categories: Access & Login, Billing & Payments, Technical Bug, Feature Request, Account & Subscription.
- Predict Low / Medium / High priority, separately from category.
- Recommend a destination support team.
- Confidence values and a low-confidence human-review flag.
- Streamlit browser app for individual tickets and CSV batch predictions.
- FastAPI REST service with Swagger documentation.
- Reproducible synthetic training data, saved models, evaluation metrics, pytest tests, GitHub Actions.

## Run locally (Windows PowerShell)
```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```
If PowerShell restricts activation, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe -m streamlit run app/streamlit_app.py`.

## Run locally (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```
Open the local Streamlit URL displayed in your terminal (typically http://localhost:8501).

## REST API
In a second terminal, with the environment activated:
```bash
uvicorn api.main:app --reload
```
Documentation: http://127.0.0.1:8000/docs

Example request:
```bash
curl -X POST http://127.0.0.1:8000/predict -H 'Content-Type: application/json' -d '{"text":"My invoice is incorrect, please fix soon."}'
```
Example output keys: `category`, `category_confidence`, `priority`, `priority_confidence`, `route_to`, `needs_human_review`.

## Retrain and test
```bash
python -m src.dataset
python -m src.model
pytest -q
```
Data is generated deterministically (seed 42), models trained using stratified train/test split (75%/25%). The two independent TF-IDF + Logistic Regression classifiers are saved to `models/`, and held-out accuracy and class reports are saved in `models/metrics.json`.

## Project layout
```text
ai_ticket_triage/
├── app/streamlit_app.py       # interactive web UI
├── api/main.py               # REST API
├── src/dataset.py            # synthetic examples
├── src/model.py              # training and inference
├── data/sample_tickets.csv   # generated samples
├── models/                   # trained classifiers + metrics
├── tests/                    # model and API tests
├── .github/workflows/tests.yml
├── requirements.txt
├── .gitignore
└── LICENSE
```

## About the AI
Text is turned into TF-IDF unigram/bigram features, then logistic regression models learn relationships to labels. The category determines the routing team using an explicit mapping. Confidence is the top predicted probability, **not** a guarantee of accuracy. Thresholds are for demonstration only; they are not calibrated to operational risk.

## Limitations & improvements
- Synthetic phrases can leak stylistic clues and do not represent actual ticket distributions.
- Separately generated urgency phrases make priority detection artificial.
- Next: collect labeled, anonymized real tickets with permission; deduplicate near-matches before splitting; compare against a baseline; calibrate probabilities; evaluate out-of-distribution performance and bias; add feedback and retraining approval before any production use.

## Deploy
Streamlit Community Cloud: push repo to GitHub, choose `app/streamlit_app.py` as the entry point, ensure `models/` is included. The REST API can run on a Python host using `uvicorn api.main:app --host 0.0.0.0 --port 8000`. For real usage, add authentication, rate limiting, audit logs, and privacy protections.

## GitHub upload
Create a repository, open a terminal in this folder, then:
```bash
git init
git add .
git commit -m "Add AI ticket triage classifier"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-ticket-triage.git
git push -u origin main
```
