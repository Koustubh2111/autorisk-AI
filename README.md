# AutoRiskAI

AutoRiskAI is a simulation project designed to replicate the responsibilities of an AI Engineer and Data Scientist working within a regulated banking environment. The system automates and supports risk, audit, and compliance workflows leveraging Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), classical Machine Learning (ML) models, secure APIs, and MLOps best practices. Emphasis is placed on privacy, explainability, reproducibility, and on-premise development.



## System Architecture Overview

The AutoRiskAI system consists of the following key modules:

- **RAG Q&A System:**  
  Context-aware document retrieval and answer generation using LangChain, MiniLM, and a local LLM (e.g., Mistral, LLaMA.cpp).

- **Vector Store:**  
  Uses `pgvector` (Postgres extension) or FAISS for efficient document embedding search.

- **ML Risk Engine:**  
  Classical models such as Isolation Forest and XGBoost for anomaly detection in audit logs.

- **Interpretability Layer:**  
  SHAP-based explanations and visualizations to make ML model outputs interpretable.

- **API Gateway:**  
  FastAPI-based service exposing endpoints for LLM queries and ML model results.

- **Observability Stack:**  
  Prometheus and Grafana for logging, metrics, and monitoring.

- **Secure Deployment:**  
  Docker Compose setup with local JWT-based authentication simulating enterprise-grade access control.

---

## Key Features

- Grounded question-answering on internal risk and audit policy documents.
- Anomaly detection on simulated audit log data.
- Interpretable risk scoring with natural language explanations powered by LLMs.
- Secure API endpoints featuring role-based access control (RBAC) and audit logging.
- Entirely local development without reliance on paid cloud APIs.
- Comprehensive technical documentation emphasizing reproducibility for hiring evaluation.

---