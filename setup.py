# setup.py
from setuptools import setup, find_packages

setup(
    name='medical_ai',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'cryptography',
        'sentence-transformers',
        'faiss-cpu',
        'numpy',
        'pandas',
        'scikit-learn',
        'mlflow',
        'torch',
        'streamlit',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'medical_ai=app.main:app',
        ],
    },
)
