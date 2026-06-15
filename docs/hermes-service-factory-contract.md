# Hermes Service Factory Contract

Hermes is the preferred future worker for building and improving services from this basecamp.

Hermes should act as a service factory worker, not as an autonomous production operator.

Hermes is a fit for this role because its documented capabilities include persistent memory, skills, MCP integration, cron scheduling, and subagent delegation. See [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/).

## Worker role

Hermes may help with:

- turning `/goal` into PRD drafts
- turning PRDs into implementation plans
- generating or updating service template code in a branch
- fixing validation failures
- summarizing GitHub Actions evidence
- writing PR handoff notes
- proposing memory updates
- proposing skill or checklist improvements

Hermes must not independently:

- merge protected branches
- deploy production
- change production secrets
- disable tests or guardrails
- make live auth, billing, payment, DNS, or infrastructure changes without explicit approval

## Input contract

A Hermes service factory task must include:

- repository path
- source PRD path or `/goal` text
- target branch or worktree rule
- selected template contract
- validation commands
- approval boundaries
- secret policy
- expected PR handoff format
- optional memory context

## Output contract

Hermes should return:

- changed files summary
- validation commands run
- pass/fail status
- failure evidence and reproduction command when blocked
- PR-ready handoff notes
- deploy and rollback notes when relevant
- revenue checklist updates when relevant
- memory episode proposal
- self-improvement proposal as draft only

## Safe worktree behavior

- Use a dedicated branch or worktree.
- Keep changes focused to the approved PRD and plan.
- Do not edit unrelated local user files.
- Do not force-push.
- Do not delete files without approval.
- Do not write secrets to tracked files, logs, plans, or PR bodies.

## Suggested worker split

For larger services, Hermes may delegate to isolated workers:

- `service-planner`: PRD and plan quality
- `web-builder`: web implementation
- `api-builder`: backend and data flow
- `payment-auth-specialist`: auth, billing, subscriptions, credits
- `qa-reviewer`: validation and regression review
- `security-reviewer`: secrets, auth, permissions, payment safety
- `release-specialist`: deploy and rollback readiness

Delegation must preserve the same approval and secret boundaries.

## Memory write contract

At the end of each run, Hermes should propose memory episodes for:

- product decisions
- validation failures
- deployment issues
- billing and credit lessons
- admin/ops issues
- user-growth or revenue hypotheses
- reusable implementation patterns

Memory updates are draft proposals unless a human or approved runtime explicitly accepts them.
