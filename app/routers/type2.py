from fastapi import APIRouter

from app.chains.type2 import answer_type2
from app.schemas.type2 import Type2Answer, Type2Question

router = APIRouter(prefix="/api/v1/type2", tags=["type2"])


@router.post("/answer", response_model=Type2Answer)
def post_type2_answer(req: Type2Question) -> Type2Answer:
    return answer_type2(req)
