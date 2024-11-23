# main.py
import logging
from fastapi import FastAPI, HTTPException
from app.config import settings
from data_validation.medical_validator import MedicalDataValidator
from hipaa_compliance.data_handler import HIPAACompliantStorage
from rag.enhanced_rag import EnhancedRAG
from evaluation.medical_evaluator import MedicalModelEvaluator
from sentence_transformers import SentenceTransformer
import uvicorn

app = FastAPI()
logger = logging.getLogger(__name__)

# Initialize components
validator = MedicalDataValidator()
encryption_key = settings.ENCRYPTION_KEY.encode()
hipaa_storage = HIPAACompliantStorage(encryption_key)
base_embedder = SentenceTransformer('all-MiniLM-L6-v2')
rag_system = EnhancedRAG(base_embedder)
evaluator = MedicalModelEvaluator()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical AI API"}

@app.post("/process_document/")
def process_document(doc: dict):
    # Validate document
    try:
        medical_doc = validator.validate_document(doc)
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    # Encrypt PHI
    encrypted_content = hipaa_storage.encrypt_phi(medical_doc.content)
    medical_doc.content = encrypted_content

    # Add to RAG system
    rag_system.add_documents([encrypted_content])

    return {"message": "Document processed successfully"}

@app.post("/query/")
def query_system(query_data: dict):
    query = query_data.get('query')
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    # Retrieve documents
    results = rag_system.retrieve_and_rerank(query)

    # Decrypt content
    decrypted_results = []
    for doc, score in results:
        decrypted_content = hipaa_storage.decrypt_phi(doc)
        decrypted_results.append({"content": decrypted_content, "score": score})

    return {"results": decrypted_results}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
