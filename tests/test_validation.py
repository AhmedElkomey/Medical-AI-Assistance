# test_validation.py
import unittest
from data_validation.medical_validator import MedicalDataValidator, MedicalDocument
from datetime import datetime

class TestMedicalValidator(unittest.TestCase):
    def setUp(self):
        self.validator = MedicalDataValidator()

    def test_valid_document(self):
        doc_data = {
            "doc_id": "123",
            "content": "This study analyzes the treatment of patients with a new drug. The results and conclusions are promising.",
            "source": "Medical Journal",
            "publication_date": datetime.now(),
            "medical_categories": ["Cardiology"],
            "confidence_score": 0.9,
            "verified_by_medical_professional": True,
            "citations": [{"title": "Previous Study", "link": "http://example.com"}]
        }
        doc = self.validator.validate_document(doc_data)
        self.assertIsInstance(doc, MedicalDocument)

    def test_missing_required_content(self):
        doc_data = {
            "doc_id": "123",
            "content": "This is an article about health.",
            "source": "Medical Journal",
            "publication_date": datetime.now(),
            "medical_categories": ["General Health"],
            "confidence_score": 0.9,
            "verified_by_medical_professional": False,
            "citations": []
        }
        with self.assertRaises(ValueError):
            self.validator.validate_document(doc_data)

    def test_blacklisted_term(self):
        doc_data = {
            "doc_id": "123",
            "content": "This miracle treatment is 100% effective for all patients.",
            "source": "Unknown",
            "publication_date": datetime.now(),
            "medical_categories": ["Alternative Medicine"],
            "confidence_score": 0.9,
            "verified_by_medical_professional": False,
            "citations": []
        }
        with self.assertRaises(ValueError):
            self.validator.validate_document(doc_data)

if __name__ == '__main__':
    unittest.main()
