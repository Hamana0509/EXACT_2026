import time

from langchain_core.prompts import ChatPromptTemplate

from app.chains.base import build_structured_chain
from app.log import get_logger, log_answer
from app.prompts.loader import load_prompt
from app.schemas.type2 import Type2Answer, Type2Question

log = get_logger(__name__)


def _build_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", load_prompt("system_base")),
            ("human", load_prompt("type2_physics")),
        ]
    )
    return build_structured_chain(prompt, Type2Answer)


def answer_type2(req: Type2Question) -> Type2Answer:
    log.info("[magenta]type2[/magenta] invoked: question_len=%d", len(req.question))
    start = time.perf_counter()
    chain = _build_chain()
    result = chain.invoke({"question": req.question})
    elapsed = time.perf_counter() - start
    log.info("[green]type2[/green] ok in %.2fs", elapsed)
    log_answer(log, "type2", result)
    return result
