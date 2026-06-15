# Task Brief

Before implementation, write the task down in this shape:

## Minimum brief
- PRD: exact file path
- Goal: what changes for the user or operator
- Non-goals: what should not change
- Affected files: smallest expected surface area
- Validation: exact commands to run
- Approvals: auth, schema, payment, env, deploy, deletion, or irreversible actions

## Execution rules
- If the task is medium or larger, update `PLANS/` first.
- Implement only what the PRD and plan require.
- Reuse existing runtime, docs, and hook patterns.
- Finish with validation plus QA/security review notes.
