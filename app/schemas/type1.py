from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import CoTStep, FOLFormula, Premise


class Type1Question(BaseModel):
    """Evaluation input for a Type 1 query.

    Mirrors the official competition spec: at evaluation, the system receives
    the question together with the natural-language premises. Nothing else.
    """

    premises_nl: list[str] = Field(alias="premises-NL")
    question: str

    model_config = ConfigDict(populate_by_name=True)


class Type1Record(BaseModel):
    """A full Type 1 dataset record (training / dev shape).

    Released organizer records carry FOL premises, ground-truth answers, and
    human explanations alongside the evaluation inputs. This schema is for
    LOADING those records in scripts; it is NOT exposed on the API surface.
    Use `to_question(index)` to get the inference-input subset.
    """

    premises_nl: list[str] = Field(alias="premises-NL")
    premises_fol: list[str] | None = Field(default=None, alias="premises-FOL")
    questions: list[str]
    answers: list[str] | None = None
    explanation: list[str] | None = None

    model_config = ConfigDict(populate_by_name=True)

    def to_question(self, index: int = 0) -> Type1Question:
        return Type1Question(premises_nl=self.premises_nl, question=self.questions[index])


class Type1Answer(BaseModel):
    """Structured response for a Type 1 question.

    `answer` and `explanation` are required. The remaining fields are scored
    under P3 (reasoning depth) when supplied.
    """

    answer: str = Field(
        description="Selected option letter (A/B/C/D/E), 'Yes'/'No'/'Uncertain', or open-text answer."
    )
    explanation: str = Field(
        description="Natural-language justification citing the premises actually used."
    )
    fol: list[FOLFormula] | None = Field(
        default=None,
        description="Derived FOL formulas, when symbolic reasoning clarifies the answer.",
    )
    cot: list[CoTStep] | None = Field(
        default=None, description="Numbered chain-of-thought steps."
    )
    premises: list[Premise] | None = Field(
        default=None, description="Premises actually used (given / derived / external)."
    )
    confidence: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Self-reported confidence in [0, 1]."
    )
