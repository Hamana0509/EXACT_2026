from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.type1 import Type1Answer, Type1Question, Type1Record
from app.schemas.type2 import Type2Answer, Type2Question, Type2Record

client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert isinstance(body["model"], str) and body["model"]


def test_type1_question_round_trip() -> None:
    q = Type1Question.model_validate(
        {"premises-NL": ["foo", "bar"], "question": "Q?"}
    )
    assert q.premises_nl == ["foo", "bar"]
    a = Type1Answer(answer="A", explanation="By premise 1.")
    assert a.answer == "A"
    assert a.fol is None


def test_type1_record_extracts_inference_input() -> None:
    """Type1Record loads a full dataset record; .to_question() drops FOL/answers/explanation."""
    record = Type1Record.model_validate(
        {
            "premises-NL": ["P1", "P2"],
            "premises-FOL": ["ForAll(x, ...)"],
            "questions": ["Does it follow?"],
            "answers": ["A"],
            "explanation": ["Because P1 and P2."],
        }
    )
    q = record.to_question()
    assert isinstance(q, Type1Question)
    assert q.premises_nl == ["P1", "P2"]
    assert q.question == "Does it follow?"
    assert not hasattr(q, "premises_fol")


def test_type2_question_round_trip() -> None:
    q = Type2Question(question="What is 2 + 2?")
    assert q.question == "What is 2 + 2?"
    a = Type2Answer(answer="2.4", unit="ohm", explanation="Parallel resistance.")
    assert a.unit == "ohm"


def test_type2_record_extracts_inference_input() -> None:
    record = Type2Record.model_validate(
        {"id": "TD001", "question": "Q?", "answer": "2.4", "unit": "ohm", "cot": "..."}
    )
    q = record.to_question()
    assert isinstance(q, Type2Question)
    assert q.question == "Q?"


def test_type1_endpoint_with_mocked_chain() -> None:
    fixture = Type1Answer(answer="A", explanation="mocked")
    with patch("app.routers.type1.answer_type1", return_value=fixture):
        r = client.post(
            "/api/v1/type1/answer",
            json={"premises-NL": ["a premise"], "question": "Does it follow?"},
        )
    assert r.status_code == 200
    assert r.json()["answer"] == "A"


def test_type2_endpoint_with_mocked_chain() -> None:
    fixture = Type2Answer(answer="2.4", unit="ohm", explanation="mocked")
    with patch("app.routers.type2.answer_type2", return_value=fixture):
        r = client.post("/api/v1/type2/answer", json={"question": "R parallel?"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"] == "2.4"
    assert body["unit"] == "ohm"


def test_unified_routes_to_type1_when_premises_present() -> None:
    fixture = Type1Answer(answer="B", explanation="mocked")
    with patch("app.routers.unified.answer_type1", return_value=fixture):
        r = client.post(
            "/api/v1/answer",
            json={"premises-NL": ["foo"], "question": "Q?"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["dataset_type"] == "type1"
    assert body["result"]["answer"] == "B"


def test_unified_routes_to_type2_when_no_premises() -> None:
    fixture = Type2Answer(answer="45", unit="J", explanation="mocked")
    with patch("app.routers.unified.answer_type2", return_value=fixture):
        r = client.post("/api/v1/answer", json={"question": "Capacitor energy?"})
    assert r.status_code == 200
    body = r.json()
    assert body["dataset_type"] == "type2"
    assert body["result"]["unit"] == "J"
