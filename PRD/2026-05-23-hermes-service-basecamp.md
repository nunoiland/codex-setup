# Hermes Service Basecamp

## Goal

Define `codex-setting` as a Hermes-ready service production basecamp for creating many web-first, app-expandable services quickly, safely, and commercially.

The basecamp should standardize how future services handle product planning, implementation, validation, low-cost VPS deployment, security, payments, subscriptions, credits, admin operations, logging, backup, and revenue-readiness.

## Scope

- In scope:
  - Document the target service basecamp architecture.
  - Define the first product template contract for web-first services.
  - Define Hermes as a service factory worker with strict safety boundaries.
  - Define a single-VPS deployment baseline under a monthly budget of 100,000 KRW.
  - Define billing, subscription, and credit primitives without adding live provider code.
  - Define admin, audit, logs, health, backup, restore, and release requirements.
  - Add readiness output and validation checks proving the contracts exist.
- Out of scope:
  - Creating the actual Next.js product template scaffold.
  - Installing Hermes, Paperclip, Graphiti, Neo4j, Docker, Caddy, PostgreSQL, Stripe, or Toss Payments.
  - Adding runtime dependencies.
  - Adding live payment, auth, deployment, or secret handling.
  - Granting Hermes production deployment or protected-branch merge authority.

## Non-goals

- Do not build a single end-user service in this change.
- Do not create production infrastructure.
- Do not store secrets, provider keys, webhook secrets, payment credentials, or VPS credentials in tracked files.
- Do not make GitHub Actions require AI/provider keys or optional services.
- Do not replace local Codex and GitHub PR review as the default safe path.

## Context

The repository already has PRD-first delivery, API-key-free GitHub Actions, harness evidence collection, `/goal` intake, Product Factory docs, Hermes worker contract, Paperclip operator contract, and Graphiti memory contract.

The missing layer is a concrete service production baseline: which stack future services start from, how they deploy cheaply, how they monetize, and what operational surfaces every product must include before becoming production-ready.

## Constraints

- Web-first, app-expandable architecture.
- Single VPS baseline must fit under 100,000 KRW per month.
- Security, admin, logs, backup, and restore are default requirements.
- Billing must support subscriptions and credits through provider adapters.
- GitHub remains the validation and review source of truth.
- Hermes remains a PR/evidence/memory worker, not an autonomous production operator.

## Acceptance criteria

1. A service basecamp architecture doc defines the target layers and operating flow.
2. A service template contract defines the chosen web-first stack and required service surfaces.
3. A Hermes service factory contract defines worker inputs, outputs, permissions, and prohibited actions.
4. A VPS deployment contract defines Docker Compose, Caddy, PostgreSQL, backup, restore, healthcheck, and rollback expectations.
5. A revenue system contract defines subscription and credit primitives plus provider adapter boundaries.
6. An admin and observability contract defines required admin screens, audit events, and logs.
7. Runtime readiness reports the service basecamp contract without requiring optional services.
8. Validation requires the new docs and confirms GitHub Actions remain API-key-free.

## Edge cases

- A future service needs mobile apps before web is stable.
- A future service needs Korean payments before Stripe.
- VPS resources become too small for Graphiti, Paperclip, or multiple products.
- Billing provider webhooks fail, retry, duplicate, or arrive out of order.
- Admin users need to adjust credits manually.
- Backups exist but restore has never been tested.
- Hermes proposes weakening security or deployment gates.

## Platform target

- docs
- runtime-readiness

## Delivery mode

- existing repository + branch + draft PR
- no direct protected-branch push by default

## Reporting mode

- local_thread
- github

## Secret profile

- Required secret: none for this change.
- Future service secrets:
  - database URL
  - auth secret
  - payment provider keys
  - webhook secrets
  - VPS SSH/deployment credentials
  - backup encryption keys
- Source of injection: external environment or secret manager only.
- Owner or approver: repository operator.

## Human handoff

- QA checks:
  - Confirm docs match the intended basecamp strategy.
  - Confirm validation passes without optional services.
  - Confirm no live secrets or provider values are tracked.
- Manual release or infra tasks:
  - None in this phase.
- Final approver:
  - repository operator.

## Validation commands

```bash
python3 -m codex_runtime --operator-readiness --pretty
./scripts/validate.sh
./scripts/ci-pr-check.sh
git diff --check
```

## Done when

- Service basecamp docs exist and are linked from the docs index.
- Readiness output includes a service basecamp section.
- Validation checks require the new contracts.
- No new dependency, payment, auth, deployment, or secret-bearing integration is added.
