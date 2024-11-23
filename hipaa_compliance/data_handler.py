# data_handler.py
import re
from cryptography.fernet import Fernet
import logging

class HIPAACompliantStorage:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
        self.logger = logging.getLogger(__name__)

    def encrypt_phi(self, data: str) -> str:
        """Encrypt Protected Health Information"""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_phi(self, encrypted_data: str) -> str:
        """Decrypt Protected Health Information"""
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    def anonymize_data(self, text: str) -> str:
        """Remove personally identifiable information"""
        patterns = {
            'name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'email': r'\b[\w\.-]+@[\w\.-]+\.\w+\b',
            'phone': r'\b\d{3}[-.)]\d{3}[-.)]\d{4}\b'
        }

        anonymized = text
        for pattern_name, pattern in patterns.items():
            anonymized = re.sub(pattern, f'[REDACTED {pattern_name.upper()}]', anonymized)
        return anonymized
