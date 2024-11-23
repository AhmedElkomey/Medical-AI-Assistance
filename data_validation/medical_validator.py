# medical_validator.py
from typing import Dict, List
import re
from datetime import datetime
from pydantic import BaseModel, validator
import logging

class MedicalDocument(BaseModel):
    """Pydantic model for medical document validation"""
    doc_id: str
    content: str
    source: str
    publication_date: datetime
    medical_categories: List[str]
    confidence_score: float
    verified_by_medical_professional: bool = False
    citations: List[Dict[str, str]] = []

    @validator('content')
    def validate_medical_content(cls, v):
        # Check for required medical context patterns
        required_patterns = [
            r'\b(?:study|trial|analysis)\b',
            r'\b(?:patient|treatment|diagnosis)\b',
            r'\b(?:conclusion|results|findings)\b'
        ]
        for pattern in required_patterns:
            if not re.search(pattern, v, re.IGNORECASE):
                raise ValueError(f"Content missing required medical context: {pattern}")
        return v

    @validator('confidence_score')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Confidence score must be between 0 and 1")
        return v

class MedicalDataValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.blacklist_terms = self._load_blacklist()

    def _load_blacklist(self) -> List[str]:
        # Load terms that should trigger additional review
        return [
            "cure all",
            "miracle treatment",
            "guaranteed results",
            "100% effective"
        ]

    def validate_document(self, doc_data: dict) -> MedicalDocument:
        """Comprehensive validation of medical documents"""
        # Validate using Pydantic model
        doc = MedicalDocument(**doc_data)
        validation_results = {
            "passed": True,
            "warnings": [],
            "metadata_complete": True,
            "requires_review": False
        }

        # Check for blacklisted terms
        for term in self.blacklist_terms:
            if term.lower() in doc.content.lower():
                validation_results["warnings"].append(f"Contains potentially problematic term: {term}")
                validation_results["requires_review"] = True

        # Validate citations
        if not doc.citations:
            validation_results["warnings"].append("No citations provided")
            validation_results["metadata_complete"] = False

        # Check content length and structure
        if len(doc.content.split()) < 100:
            validation_results["warnings"].append("Content may be too brief for comprehensive medical information")

        if validation_results["warnings"]:
            validation_results["passed"] = False
            self.logger.warning(f"Validation issues: {validation_results['warnings']}")
            raise ValueError(f"Validation failed: {validation_results['warnings']}")

        return doc
