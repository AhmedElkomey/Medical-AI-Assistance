# test_hipaa.py
import unittest
from hipaa_compliance.data_handler import HIPAACompliantStorage
from cryptography.fernet import Fernet

class TestHIPAACompliance(unittest.TestCase):
    def setUp(self):
        self.encryption_key = Fernet.generate_key()
        self.storage = HIPAACompliantStorage(self.encryption_key)
        self.test_data = "Patient John Doe's SSN is 123-45-6789."

    def test_encryption_decryption(self):
        encrypted = self.storage.encrypt_phi(self.test_data)
        decrypted = self.storage.decrypt_phi(encrypted)
        self.assertEqual(self.test_data, decrypted)

    def test_anonymization(self):
        anonymized = self.storage.anonymize_data(self.test_data)
        expected = "Patient [REDACTED NAME]'s SSN is [REDACTED SSN]."
        self.assertEqual(anonymized, expected)

if __name__ == '__main__':
    unittest.main()
