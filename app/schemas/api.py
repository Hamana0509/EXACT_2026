from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.type1 import Type1Answer
from app.schemas.type2 import Type2Answer


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    model: str


class ErrorResponse(BaseModel):
    detail: str
    code: str = "internal_error"


class UnifiedRequest(BaseModel):
    """Permissive request mirroring the official unified test set.

    The dispatcher routes by presence of `premises_nl`:
    - non-empty list -> Type 1
    - absent / empty -> Type 2
    """

    premises_nl: list[str] | None = Field(default=None, alias="premises-NL")
    question: str

    model_config = ConfigDict(populate_by_name=True)


class UnifiedResponse(BaseModel):
    dataset_type: Literal["type1", "type2"]
    result: Type1Answer | Type2Answer
