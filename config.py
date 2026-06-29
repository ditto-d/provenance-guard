import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_WEIGHT=0.50
STYLOMETRIC_WEIGHT=0.30
REPETITION_WEIGHT=0.20

RATE_LIMIT="10 per minute; 100 per day"

AUDIT_LOG_PATH = "logs/audit_log.json"
