from typing import TypeVar

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from app.config import get_settings
from app.llm import build_chat_model
from app.log import get_logger

T = TypeVar("T", bound=BaseModel)

log = get_logger(__name__)


def build_structured_chain(prompt: ChatPromptTemplate, schema: type[T]) -> Runnable:
    """Compose a prompt template with a `with_structured_output`-bound ChatOpenAI.

    The structured-output method comes from `STRUCTURED_OUTPUT_METHOD` in `.env`
    (default `json_schema`). For models that do not support JSON-schema mode
    on OpenRouter, fall back to `function_calling` or `json_mode`.
    """
    settings = get_settings()
    log.debug(
        "building structured chain: schema=%s method=%s model=%s",
        schema.__name__,
        settings.structured_output_method,
        settings.model_name,
    )
    llm = build_chat_model()
    structured = llm.with_structured_output(schema, method=settings.structured_output_method)
    return prompt | structured
