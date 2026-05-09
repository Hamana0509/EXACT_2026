from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    openai_url: str = Field(alias="OPENAI_URL")
    model_name: str = Field(alias="MODEL_NAME")
    structured_output_method: Literal["json_schema", "function_calling", "json_mode"] = Field(
        default="json_schema", alias="STRUCTURED_OUTPUT_METHOD"
    )
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # Qwen3 thinking toggle. Forwarded via `extra_body.chat_template_kwargs.enable_thinking`
    # to vLLM/SGLang-served Qwen3 backends. Default off: thinking mode emits <think>...</think>
    # tags that can break structured output unless the provider strips them.
    enable_thinking: bool = Field(default=False, alias="ENABLE_THINKING")
    max_tokens: int = Field(default=32768, alias="MAX_TOKENS")

    # Sampling overrides. When unset, the LLM builder picks Qwen3's recommended values for
    # the active thinking mode (see app/llm.py: QWEN3_THINKING / QWEN3_NON_THINKING).
    temperature: float | None = Field(default=None, alias="TEMPERATURE")
    top_p: float | None = Field(default=None, alias="TOP_P")
    top_k: int | None = Field(default=None, alias="TOP_K")
    min_p: float | None = Field(default=None, alias="MIN_P")
    presence_penalty: float | None = Field(default=None, alias="PRESENCE_PENALTY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
