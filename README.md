# Medical AI Application

A comprehensive end-to-end application for processing, validating, and querying medical documents while ensuring HIPAA compliance. This system integrates data validation, HIPAA-compliant data handling, a Retrieval-Augmented Generation (RAG) system, and a comprehensive evaluation framework tailored for medical AI models.

## Features

- **Document Validation**: Uses Pydantic models to validate medical documents against predefined rules and patterns
- **HIPAA-Compliant Data Handling**: Encrypts Protected Health Information (PHI) using Fernet symmetric encryption and anonymizes data
- **Retrieval-Augmented Generation (RAG)**: Implements an enhanced RAG system with semantic search and cross-encoder reranking using FAISS and Sentence Transformers
- **Model Evaluation**: Provides a comprehensive evaluation framework with medical-specific metrics
- **MLflow Tracking**: Tracks experiments, logs metrics, and handles model versioning
- **Streamlit UI**: Offers a user-friendly interface for system interaction

## Prerequisites

- Python 3.9+
- Git
- Virtual Environment Tool (e.g., venv, conda)
- Docker and Docker Compose (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AhmedElkomey/medical_ai.git
cd medical_ai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Generate an encryption key:
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
```

Set required environment variables:
```bash
export ENCRYPTION_KEY='your-generated-key'
export DATABASE_URL='sqlite:///./mlflow.db'
```

Alternatively, create a `.env` file:
```bash
ENCRYPTION_KEY=your-generated-key
DATABASE_URL=sqlite:///./mlflow.db
```

## Usage

### Starting the API Server

```bash
uvicorn app.main:app --reload
```
- API Access: http://localhost:8000
- Documentation: http://localhost:8000/docs

### Starting the Streamlit UI

```bash
streamlit run app/ui/streamlit_app.py
```
- UI Access: http://localhost:8501

## Example Usage

### Processing a Medical Document

```json
{
  "doc_id": "doc_001",
  "content": "This study analyzes the treatment of patients with a new cardiac drug...",
  "source": "Cardiology Journal",
  "publication_date": "2023-10-01T00:00:00",
  "medical_categories": ["Cardiology", "Pharmacology"],
  "confidence_score": 0.95,
  "verified_by_medical_professional": true,
  "citations": [
    {"title": "Previous Cardiac Study", "link": "http://example.com/study1"},
    {"title": "Drug Efficacy Research", "link": "http://example.com/study2"}
  ]
}
```

### Querying the System

```json
{
  "query": "What are the recent advancements in heart failure treatment?"
}
```

## Project Structure

```
medical_ai/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── ui/
│       └── streamlit_app.py
├── data_validation/
│   ├── __init__.py
│   ├── medical_validator.py
│   └── validation_rules/
├── hipaa_compliance/
│   ├── __init__.py
│   ├── data_handler.py
│   └── encryption/
├── rag/
│   ├── __init__.py
│   ├── enhanced_rag.py
│   └── embeddings/
├── evaluation/
│   ├── __init__.py
│   ├── medical_evaluator.py
│   └── metrics/
├── models/
│   ├── __init__.py
│   └── model_artifacts/
├── tests/
│   ├── test_validation.py
│   ├── test_hipaa.py
│   ├── test_rag.py
│   └── test_evaluation.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── api.md
│   ├── deployment.md
│   └── security.md
├── mlflow_tracking/
│   ├── __init__.py
│   ├── experiment_tracker.py
│   ├── model_registry.py
│   └── configs/
├── mlruns/
├── mlflow.db
├── requirements.txt
├── setup.py
└── README.md
```

## Testing

Run the test suite:
```bash
python -m unittest discover tests
```

## Docker Deployment

1. Build and run containers:
```bash
docker-compose up --build
```

2. Access services:
- API: http://localhost:8000
- UI: http://localhost:8501

## Security Considerations

- Ensure proper encryption key management
- Implement access control mechanisms
- Use HTTPS for all endpoints
- Follow HIPAA compliance guidelines
- Avoid logging sensitive information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

Please ensure your code passes all tests and follows project coding standards.

## License

This project is licensed under the MIT License.

## Contact

- Name: Ahmed Elkomey
- Email: ahmedelkomey961@gmail.com
- GitHub: https://github.com/AhmedElkomey/

## Troubleshooting

Common issues and solutions:

- **Invalid Encryption Key**: Regenerate key using provided script
- **Module Import Errors**: Verify presence of `__init__.py` files
- **Index Errors**: Process documents before querying
- **Streamlit Errors**: Ensure API server is running

For additional support, please check the documentation in the `docs/` directory or raise an issue on GitHub.