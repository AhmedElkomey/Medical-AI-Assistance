# test_rag.py
import unittest
from rag.enhanced_rag import EnhancedRAG
from sentence_transformers import SentenceTransformer

class TestEnhancedRAG(unittest.TestCase):
    def setUp(self):
        self.embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.rag_system = EnhancedRAG(self.embedder)
        self.documents = [
            "The heart is a muscular organ in most animals.",
            "The brain is the center of the nervous system.",
            "Cancer is a group of diseases involving abnormal cell growth."
        ]
        self.rag_system.add_documents(self.documents)

    def test_retrieve_and_rerank(self):
        query = "What is the function of the heart?"
        results = self.rag_system.retrieve_and_rerank(query)
        self.assertTrue(len(results) > 0)
        top_result = results[0][0]
        self.assertIn("heart", top_result.lower())

if __name__ == '__main__':
    unittest.main()
