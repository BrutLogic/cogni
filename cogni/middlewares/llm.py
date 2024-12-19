from typing import Any, Dict
from ..wrappers import MW
from ..tools import llm

@MW.register
def mock_llm(ctx: Dict[str, Any], conv: Any) -> Any:
    """Middleware that processes input through mock LLM."""
    return llm(conv, model="mock_llm")

@MW.register 
def llm_chain(ctx: Dict[str, Any], conv: Any) -> Any:
    """Generic LLM middleware that can be configured with different models."""
    model = ctx.get("model", "mock_llm")
    return llm(conv, model=model)
