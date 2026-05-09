from functools import lru_cache
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


@lru_cache
def load_prompt(name: str) -> str:
    """Load a prompt template (.md) from `app/prompts/`.

    The returned string is meant to be passed to `ChatPromptTemplate` as a
    message body. Curly braces in the file are interpreted as template
    placeholders; literal `{` or `}` characters must be escaped as `{{` / `}}`.
    """
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")
