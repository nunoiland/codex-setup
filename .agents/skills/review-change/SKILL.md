---
name: review-change
description: Review the current diff against the PRD, approved plan, and repository conventions. Use for QA, security, and maintainability review before finalizing a PRD-driven change.
---

# Review Change

Use this skill after implementation and validation.

## Goal

Assess whether the current change is correct, safe, and still aligned with the PRD.

## Review lenses

- QA: behavior changes, regression risk, edge cases, missing tests
- Security: auth, secrets, validation, storage, network use, privilege boundaries, injection, dependency risk
- Maintainability: scope control, architectural fit, consistency with existing patterns
- Delivery fit: GitHub handoff assumptions, protected-branch safety, reporting-channel boundaries, and human handoff clarity

## Workflow

1. Read the PRD and approved plan.
2. Inspect the current diff and nearby code.
3. Verify that delivery mode, reporting mode, and secret boundaries remain aligned with the PRD.
4. Review with `qa_reviewer`.
5. Review with `security_reviewer`.
6. Summarize findings first, ordered by severity.
7. If no findings exist, state that explicitly and note residual risks or coverage gaps.

## Rules

- Reviewers are read-only.
- Tie feedback to behavior, files, or concrete risks.
- Do not let maintainability comments displace higher-severity correctness or security issues.
- Call out any mismatch between GitHub delivery guidance, local handoff guidance, and actual guardrails.
