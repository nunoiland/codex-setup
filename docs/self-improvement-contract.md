# Self-Improvement Contract

The runtime may propose improvements to its own workflow, but those proposals remain draft-only until a human reviews them.

## Allowed proposal types

- new skill drafts
- checklist improvements
- prompt refinements
- memory-deduplication ideas
- guardrail additions that strengthen safety

## Disallowed behavior

- direct mutation of protected branches without review
- removal or weakening of approval gates
- automatic deployment decisions
- silent adoption of business strategy as fact
- storing secrets or production credentials in tracked files

## Review rule

Every proposal must be treated as:

- status: `draft`
- review required: `true`
- human approver required before adoption

## Promotion path

1. proposal is generated from a run
2. operator reviews it in GitHub or local runtime storage
3. approved ideas are turned into a plan-backed code or doc change
4. normal validation, QA, and security review still apply
