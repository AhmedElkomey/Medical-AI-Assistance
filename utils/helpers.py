# helpers.py
import logging

def setup_logging(level=logging.INFO):
    """Set up logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_medical_terms(filepath: str) -> set:
    """Load medical terms from a file into a set."""
    with open(filepath, 'r') as file:
        terms = set(line.strip() for line in file)
    return terms
