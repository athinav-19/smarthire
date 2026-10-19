# Answer Quality Evaluation

The instructor requires evaluation of retrieval relevance, mentor answer quality, prompt improvement, and hallucination/refusal behavior.

## Starter test plan

| Test | Expected result |
|---|---|
| Python developer profile | Relevant developer jobs appear near the top |
| Data analyst question | Answer uses retrieved career documents |
| Unsupported question | Mentor says it does not know from the available documents |
| Off-topic question | Guardrail rejects it |
| Unsafe request | Guardrail rejects it |

Record measured results here after testing the final dataset.
