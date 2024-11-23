# config.py
import os
from cryptography.fernet import Fernet

class Settings:
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

    if ENCRYPTION_KEY is None:
        print("No ENCRYPTION_KEY found. Generating a new one.")
        ENCRYPTION_KEY = Fernet.generate_key().decode()
    else:
        print(f'{ENCRYPTION_KEY=}')
        # Validate the key
        try:
            _ = Fernet(ENCRYPTION_KEY.encode())
        except Exception as e:
            raise ValueError(f"Invalid ENCRYPTION_KEY: {e}")
settings = Settings()