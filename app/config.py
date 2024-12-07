import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

class Config:
    # Azure OpenAI configuration
    # GPT-40-mini deployed on Azure
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    AZURE_API_KEY = os.getenv("AZURE_API_KEY")
    AZURE_API_VERSION = "2024-08-01-preview"

    # Redis configuration
    REDIS_URL = os.getenv("REDIS_URL")

    # Celery configuration
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
