import os


API_URL = os.getenv("API_URL", "http://127.0.0.1:5000").rstrip("/")
REQUEST_TIMEOUT = float(os.getenv("API_TIMEOUT", "15"))
