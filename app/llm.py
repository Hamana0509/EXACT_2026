from langchain_openai import ChatOpenAI

from app.config import get_settings

# Qwen3 model-card recommendations. https://huggingface.co/Qwen/Qwen3-8B
# Greedy decoding is explicitly discouraged for thinking mode (causes endless repetitions).
QWEN3_THINKING = {"temperature": 0.6, "top_p": 0.95, "top_k": 20, "min_p": 0.0}
QWEN3_NON_THINKING = {"temperature": 0.7, "top_p": 0.8, "top_k": 20, "min_p": 0.0}


def build_chat_model(temperature: float | None = None) -> ChatOpenAI:
    s = get_settings()
    defaults = QWEN3_THINKING if s.enable_thinking else QWEN3_NON_THINKING

    temp = temperature if temperature is not None else (
        s.temperature if s.temperature is not None else defaults["temperature"]
    )
    top_p = s.top_p if s.top_p is not None else defaults["top_p"]
    top_k = s.top_k if s.top_k is not None else defaults["top_k"]
    min_p = s.min_p if s.min_p is not None else defaults["min_p"]

    # `top_k` and `min_p` are not standard OpenAI fields; vLLM/SGLang accept them via
    # `extra_body`. `chat_template_kwargs.enable_thinking` is the documented way to
    # toggle Qwen3's thinking mode through an OpenAI-compatible endpoint.
    extra_body: dict = {
        "top_k": top_k,
        "min_p": min_p,
        "chat_template_kwargs": {"enable_thinking": s.enable_thinking},
    }

    kwargs: dict = {
        "model": s.model_name,
        "api_key": s.openai_api_key,
        "base_url": s.openai_url,
        "temperature": temp,
        "top_p": top_p,
        "max_tokens": s.max_tokens,
        "timeout": 60,
        "extra_body": extra_body,
    }
    if s.presence_penalty is not None:
        kwargs["presence_penalty"] = s.presence_penalty

    return ChatOpenAI(**kwargs)
