from pydantic import BaseModel, Field

from app.schemas.common import CoTStep, FOLFormula, Premise


class Type2Question(BaseModel):
    """Evaluation input for a Type 2 query.

    Mirrors the official spec: the system receives only the question.
    Record metadata (e.g. `id`) is tracked outside the API surface by
    submission scripts.
    """

    question: str


class Type2Record(BaseModel):
    """A full Type 2 dataset record (training / dev shape).

    Released organizer records carry the question alongside `id`, a
    chain-of-thought reference, and ground-truth `answer` + `unit`. This
    schema is for LOADING those records in scripts; it is NOT exposed on
    the API surface. Use `to_question()` to get the inference-input subset.
    """

    id: str
    question: str
    cot: str | None = None
    answer: str | None = None
    unit: str | None = None

    def to_question(self) -> Type2Question:
        return Type2Question(question=self.question)


class Type2Answer(BaseModel):
    """Structured response for a Type 2 question.

    `answer` is the numeric value as a string (preserves precision such as
    '3.0e-5'); `unit` is a separate field. `cot` and `premises` carry the
    physical reasoning and laws applied.
    """

    answer: str = Field(
        description="Numeric value as a string (e.g. '2.4', '3.0e-5'). Do NOT include the unit here."
    )
    unit: str = Field(description="SI unit, e.g. 'ohm', 'J', 'V', 'A'.")
    explanation: str = Field(
        description="Natural-language justification citing the governing physical laws and key steps."
    )
    cot: list[CoTStep] | None = Field(
        default=None,
        description="Numbered numeric chain-of-thought, units carried through every step.",
    )
    fol: list[FOLFormula] | None = Field(
        default=None, description="Optional formal representation of the reasoning."
    )
    premises: list[Premise] | None = Field(
        default=None,
        description="Physical laws / formulas used (e.g. Ohm's law, Kirchhoff's voltage law).",
    )
    confidence: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Self-reported confidence in [0, 1]."
    )
