import logfire
import re
from langchain_groq import ChatGroq
from nemoguardrails import RailsConfig, LLMRails

from app.config import settings
from app.guardrails.colang_rules import (
    COLANG_CONTENT,
    OFF_TOPIC_PATTERNS,
    OFF_TOPIC_RESPONSE,
    RAIL_INDICATORS,
    YAML_CONTENT,
)


_rails: LLMRails | None = None
_off_topic_patterns = tuple(re.compile(pattern, re.IGNORECASE) for pattern in OFF_TOPIC_PATTERNS)


def initialize_rails() -> None:
    """
    Build the NeMo LLMRails singleton at app startup.
    Uses the configured guardrail model for intent classification at the gate.
    """
    global _rails

    guard_llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_GUARDRAIL_MODEL,
        temperature=0
    )

    config = RailsConfig.from_content(
        colang_content=COLANG_CONTENT,
        yaml_content=YAML_CONTENT
    )

    _rails = LLMRails(config, llm=guard_llm)
    logfire.info(
        "🛡️ NeMo Guardrails initialised "
        f"({settings.GROQ_GUARDRAIL_MODEL})."
    )
    
    


def guard(message: str) -> tuple[bool, str | None]:
    """
    Run a user message through the NeMo rails gate.

    Returns:
        (True,  rail_response) — a rail fired; return this response immediately,
                                skip the RAG pipeline entirely.
        (False, None)          — message is clean; proceed to LangGraph.
    """
    if any(pattern.search(message) for pattern in _off_topic_patterns):
        logfire.info("🛡️ Deterministic off-topic guard fired.")
        return True, OFF_TOPIC_RESPONSE

    if _rails is None:
        logfire.warning("⚠️ Guardrails not initialised — skipping gate.")
        return False, None

    with logfire.span("🛡️ Guardrails Check"):
        result = _rails.generate(messages=[{"role": "user", "content": message}])

        # NeMo returns {'role': 'assistant', 'content': '...'} — extract text
        content = result.get("content", "") if isinstance(result, dict) else str(result)

        fired = any(indicator in content for indicator in RAIL_INDICATORS)

        if fired:
            logfire.info(f"🛡️ Guardrails fired | query='{message[:80]}'")
            return True, content

        logfire.info("✅ Guardrails passed.")
        return False, None
