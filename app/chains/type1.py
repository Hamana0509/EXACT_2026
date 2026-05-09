import time

from langchain_core.prompts import ChatPromptTemplate

from app.chains.base import build_structured_chain
from app.log import get_logger, log_answer
from app.prompts.loader import load_prompt
from app.schemas.type1 import Type1Answer, Type1Question

log = get_logger(__name__)


def _build_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", load_prompt("system_base")),
            ("human", load_prompt("type1_logic")),
        ]
    )
    return build_structured_chain(prompt, Type1Answer)


def answer_type1(req: Type1Question) -> Type1Answer:
    log.info(
        "[cyan]type1[/cyan] invoked: %d premise(s), question_len=%d",
        len(req.premises_nl),
        len(req.question),
    )
    start = time.perf_counter()
    chain = _build_chain()
    payload = {
        "premises_nl": "\n".join(f"{i + 1}. {p}" for i, p in enumerate(req.premises_nl)),
        "question": req.question,
    }
    result = chain.invoke(payload)
    elapsed = time.perf_counter() - start
    log.info("[green]type1[/green] ok in %.2fs", elapsed)
    log_answer(log, "type1", result)
    return result
