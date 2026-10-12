import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    # Load environment variables from .env file
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")
    GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")

    # Qdrant
    QDRANT_URL = os.getenv("QDRANT_URL") or os.getenv("QDRANT_CLUSTER_URL") or os.getenv("QDRANT_HOST")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or os.getenv("QDRANT_CLUSTER_API_KEY")
    QDRANT_COLLECTION = "advance_rag"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()
