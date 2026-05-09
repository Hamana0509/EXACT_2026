from fastapi import APIRouter

from app.chains.type1 import answer_type1
from app.chains.type2 import answer_type2
from app.schemas.api import UnifiedRequest, UnifiedResponse
from app.schemas.type1 import Type1Question
from app.schemas.type2 import Type2Question

router = APIRouter(prefix="/api/v1", tags=["unified"])


@router.post("/answer", response_model=UnifiedResponse)
def post_unified_answer(req: UnifiedRequest) -> UnifiedResponse:
    """Dispatcher matching the official unified test set.

    Routes by presence of `premises-NL`: non-empty list -> Type 1; otherwise -> Type 2.
    """
    if req.premises_nl:
        t1 = Type1Question(premises_nl=req.premises_nl, question=req.question)
        return UnifiedResponse(dataset_type="type1", result=answer_type1(t1))

    t2 = Type2Question(question=req.question)
    return UnifiedResponse(dataset_type="type2", result=answer_type2(t2))
