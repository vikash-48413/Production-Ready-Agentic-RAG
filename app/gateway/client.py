import logfire
from portkey_ai import Portkey, createHeaders, PORTKEY_GATEWAY_URL
from langchain_openai import ChatOpenAI

from app.config import settings


# Inline Portkey configs are rejected when the workspace has block_inline_config
# enabled. Use a saved config slug when one is supplied; otherwise route through
# the configured Portkey provider virtual key.
GATEWAY_CONFIG = {
    "strategy": {"mode": "fallback"},
    "cache": {"mode": "simple"},
    "retry": {
        "attempts": 2,
        "on_status_codes": [429, 503]
    },
    "targets": [
        {"override_params": {"model": f"@{settings.GROQ_SLUG}/llama-3.3-70b-versatile"}},
        {"override_params": {"model": f"@{settings.GROQ_SLUG_2}/llama-3.1-8b-instant"}},
    ]
}

PRIMARY_MODEL = f"@{settings.GROQ_SLUG}/{settings.GROQ_MODEL}"

portkey_client = Portkey(
    api_key=settings.PORTKEY_API_KEY,
    config=settings.PORTKEY_CONFIG_SLUG or None,
)


def get_langchain_llm(feature: str = "rag") -> ChatOpenAI:
    """
    Returns a Portkey-backed ChatOpenAI — a drop-in for ChatGroq in LangChain nodes.

    Why ChatOpenAI and not ChatGroq:
      Portkey is a proxy. It exposes an OpenAI-compatible endpoint at PORTKEY_GATEWAY_URL.
      ChatGroq is hardwired to Groq's API and does not support routing through a proxy.
      ChatOpenAI supports base_url (points at Portkey) and default_headers (passes Portkey
      auth + config). The @rag/model-name format is Portkey-specific — Groq's own client
      does not understand it. You are still using Groq models; Portkey is just in the middle.
    """
    headers = createHeaders(
        api_key=settings.PORTKEY_API_KEY,
        config=settings.PORTKEY_CONFIG_SLUG,
        metadata={
            "feature": feature,
            "_user": "rag-system",
            "environment": "production"
        }
    ) if settings.PORTKEY_CONFIG_SLUG else None

    return ChatOpenAI(
        api_key=settings.PORTKEY_API_KEY,
        base_url=PORTKEY_GATEWAY_URL,
        model=PRIMARY_MODEL,
        temperature=0,
        default_headers=headers,
    )


def extract_cache_status(response) -> str:
    """
    Pull x-portkey-cache-status from the Portkey native client response headers.
    Tries multiple attribute paths defensively — returns 'MISS' if not found.
    """
    for attr in ("_raw_response", "_response", "_http_response"):
        raw = getattr(response, attr, None)
        if raw is not None:
            status = getattr(raw, "headers", {}).get("x-portkey-cache-status", "")
            if status:
                return status.upper()
    return "MISS"
