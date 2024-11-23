# test_evaluation.py
import unittest
from evaluation.medical_evaluator import MedicalModelEvaluator

class TestMedicalEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = MedicalModelEvaluator()

    def test_evaluate_response(self):
        query = "What are the symptoms of heart disease?"
        response = "Heart disease symptoms include chest pain and shortness of breath."
        ground_truth = "Symptoms of heart disease can include chest pain and shortness of breath."
        context_docs = ["Heart disease often presents with chest pain and difficulty breathing."]

        evaluation = self.evaluator.evaluate_response(query, response, ground_truth, context_docs)
        self.assertIsInstance(evaluation, dict)
        self.assertIn("factual_accuracy", evaluation)

if __name__ == '__main__':
    unittest.main()
