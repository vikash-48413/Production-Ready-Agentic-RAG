# import os
# from dotenv import load_dotenv


# load_dotenv()


# class Settings:
#     # Load environment variables from .env file
#     GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#     GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")
#     GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")

#     # Qdrant
#     QDRANT_URL = os.getenv("QDRANT_URL") or os.getenv("QDRANT_CLUSTER_URL") or os.getenv("QDRANT_HOST")
#     QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or os.getenv("QDRANT_CLUSTER_API_KEY")
#     QDRANT_COLLECTION = "advance_rag"

#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# settings = Settings()




import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # --- GEMINI EMBEDDINGS ---
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # --- VECTOR DB (QDRANT) ---
    QDRANT_URL = (
        os.getenv("QDRANT_CLUSTER_ENDPOINT")
        or os.getenv("QDRANT_URL")
        or os.getenv("QDRANT_CLUSTER_URL")
    )
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "advance_rag")

    # --- REASONING ENGINE (GROQ) ---
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")
    GROQ_GUARDRAIL_MODEL = os.getenv("GROQ_GUARDRAIL_MODEL", "openai/gpt-oss-20b")
    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")

    # --- LLM GATEWAY (PORTKEY) ---
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
    GROQ_SLUG = os.getenv("GROQ_SLUG", "vllm")
    GROQ_SLUG_2 = os.getenv("GROQ_SLUG_2", "vllm2")
    PORTKEY_CONFIG_SLUG = os.getenv("PORTKEY_CONFIG_SLUG")


    # --- OBSERVABILITY ---
    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "rag_scale_test")
    LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

# Apply LangChain environment variables for automatic tracing
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "rag_scale_test")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

settings = Settings()
