from typing import Literal

from pydantic import BaseModel, Field

AnswerLetter = Literal["A", "B", "C", "D", "E"]
YesNoUncertain = Literal["Yes", "No", "Uncertain"]


class CoTStep(BaseModel):
    step: int = Field(ge=1, description="1-indexed step number.")
    reasoning: str = Field(description="What this step concludes and from which premises.")


class FOLFormula(BaseModel):
    formula: str = Field(description="First-order-logic formula as a string (no canonical solver dialect required).")
    description: str | None = Field(
        default=None,
        description="Optional natural-language gloss of what the formula encodes.",
    )


class Premise(BaseModel):
    id: str | int = Field(description="Identifier of the premise (e.g. 1, 2, 'P3', 'OhmLaw').")
    statement: str = Field(description="The premise content.")
    source: Literal["given", "derived", "external"] = Field(
        default="given",
        description="'given' = from the input; 'derived' = produced by reasoning; 'external' = world knowledge.",
    )
