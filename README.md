# AutoRiskAI

AutoRiskAI is a simulation project that automates and supports risk, audit, and compliance workflows in a banking-like environment. It leverages Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), classical Machine Learning (ML) models, FastAPI-based services, and containerized local deployment to simulate a real-world AI engineering workflow. Emphasis is placed on privacy, explainability, reproducibility, and complete on-premise development.

## System Architecture Overview

The AutoRiskAI system consists of the following key modules:

- **RAG Q&A System**  
  Context-aware document retrieval and answer generation using LangChain, `MiniLM`, and a local LLM (e.g., Mistral via Ollama).  
  [Code: `pipeline/pdf_to_pgvector.py`](./pipeline/pdf_to_pgvector.py)

- **Vector Store**  
  Uses `pgvector` (Postgres extension) to store and search document embeddings.  
  [Docker: `docker-compose.yml`](./docker-compose.yml)  
  [Code: `api/semantic_search_api.py`](./api/semantic_search_api.py)

- **ML Risk Engine**  
  Simulated audit log anomaly detection using XGBoost. Model development, evaluation, and interpretability are handled in Jupyter notebooks.  
  [Notebook: `notebooks/audit_log_modeling.ipynb`](./notebooks/anamoly_xgboost.ipynb)  
  [Data: `data/logs/simulated_audit_logs.csv`](./data/logs/)

- **Interpretability Layer**  
  SHAP-based explanations to visualize and interpret model outputs for compliance and audit traceability.  
  [Notebook: `notebooks/shap_explanations.ipynb`](./notebooks/anamoly_xgboost.ipynb) 

- **API Gateway**  
  FastAPI application exposes key endpoints:
  - `/search`: For semantic document Q&A
  - `/score-log`: For risk scoring on audit events
  - `/explain-risk`: For SHAP-based explanations of predictions  
  [Code: `api/risk_scoring_api.py`](./api/risk_scoring_api.py)

- **Observability Stack**  
  Prometheus and Grafana for logging and monitoring (optional extension).

- **Secure Deployment**  
  Docker Compose environment with `.env` configuration to simulate enterprise-grade infrastructure.  
  [Dockerfile: `Dockerfile`](./Dockerfile)

## Key Features

- Document ingestion and semantic retrieval using MiniLM and pgvector
- Grounded Q&A over internal risk/audit policy PDFs
- Simulated audit log generator with anomaly scenarios
- Anomaly detection using XGBoost with support for SHAP explainability
- Local-only FastAPI services for scoring and explanation
- MLflow used for experiment tracking, model logging, and evaluation
- Containerized infrastructure using Docker and Docker Compose
- Tested endpoints with integration test suite (`pytest` and `FastAPI TestClient`)

## Project Layout

```
AutoRiskAI/
├── api/
│   └── risk_scoring_api.py
├── pipeline/
│   └── pdf_to_pgvector.py
├── data/
│   └── logs/
│       └── simulated_audit_logs_with_features.csv
├── embeddings/
    └── scripts
      └──generate_noisy_audit_logs.py
      └──create-sample-pdf.py
├── models/
    └── xgb_model.model
├── query/
    └── test_api.py
├── tests/
    └── semantic_search.py    
├── notebooks/
│   ├── anamoly_xgboost.ipynb.ipynb
│   └── feature_engineering.ipynb
├── docker-compose.yml
└── requirements.txt
```

## Getting Started

1. Clone this repository.
2. Create a `.env` file with the following:
   ```
   POSTGRES_DB=autoriskdb
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=yourpassword
   ```
3. Start the system:
   ```bash
   docker-compose up --build
   ```
4. In a separate terminal, run the PDF ingestion:
   ```bash
   python rag/pdf_to_pgvector.py
   ```

## Endpoints

- `POST /search`: Perform a semantic search on policy documents.
- `POST /score-log`: Submit an audit log and receive a risk score.
- `POST /explain-risk`: Get SHAP-based explanation for an audit event.

Example API call:
```bash
curl -X POST http://localhost:8000/score-log   -H "Content-Type: application/json"   -d '{"timestamp": "2025-07-14T10:22:00", "user": "user_10", "ip_address": "192.168.1.1", "event_type": "login_failure", "resource": "/secure/data"}'
```

## Testing

Run tests using `pytest`:

```bash
pytest tests/test_api.py
```

## MLOps Features

- MLflow used for:
  - Logging parameters, metrics, and models
  - SHAP value tracking
  - Reproducibility of experiments
- Docker used for:
  - Reproducible API deployment
  - Portable, secure development
- APIs modular and ready for CI/CD integration
- FastAPI test suite ensures endpoint coverage and input validation