You will solve a physics problem and return a numerical answer with its unit.

## Question
{question}

## Instructions
1. Identify the given quantities (with units) and the asked quantity. Record them in `cot[0]`.
2. Identify the governing physical law(s). Add each to `premises` with `source="external"` and a clear statement (e.g. "Ohm's law: V = I * R").
3. Show the numeric derivation step by step in `cot`. Carry units through every step. Make unit conversions explicit; do not silently change unit prefixes.
4. Emit the final number in `answer` (e.g. "2.4", "3.0e-5"). DO NOT include the unit in `answer` — the unit goes in the `unit` field (e.g. "ohm", "J", "V", "A").
5. Write `explanation` summarizing which laws applied, how quantities combined, and what the final result represents physically.
6. Set `confidence` honestly. If the problem requires numeric approximation or rounding, mention it in the explanation.
