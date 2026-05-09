You will answer a logic question about university regulations.

## Premises (natural language)
{premises_nl}

## Question
{question}

## Instructions
1. Restate the question in your own words inside `cot[0]`.
2. For each NL premise, decide whether it is relevant. List the relevant ones in `premises` with `source="given"`, using the premise number as the `id`.
3. Reason step by step in `cot`. When you derive an intermediate conclusion, add it to `premises` with `source="derived"`.
4. If a first-order-logic translation clarifies the argument, you may emit FOL formulas in `fol`. (FOL premises are NOT given in the input; you would derive them yourself if helpful.)
5. Determine the question shape from the question text and answer accordingly:
   - If options like "A. ... B. ... C. ..." are listed, emit a single letter in `answer`.
   - If the question is a yes/no/uncertain decision, emit exactly "Yes", "No", or "Uncertain".
   - Otherwise emit a concise natural-language answer.
6. Write a clear `explanation` that cites premise numbers (e.g. "By premise 1 and the conclusion in step 2, ...").
7. Set `confidence` honestly. Use a value < 0.5 if the premises are not enough to entail a single answer.
