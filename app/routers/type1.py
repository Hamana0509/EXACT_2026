from fastapi import APIRouter

from app.chains.type1 import answer_type1
from app.schemas.type1 import Type1Answer, Type1Question

router = APIRouter(prefix="/api/v1/type1", tags=["type1"])


@router.post("/answer", response_model=Type1Answer)
def post_type1_answer(req: Type1Question) -> Type1Answer:
    return answer_type1(req)
