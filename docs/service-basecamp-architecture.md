# Service Basecamp Architecture

This is the standard architecture for using `codex-setting` as a GitHub template for many web-first, app-expandable services with Hermes support.

The goal is not to build one product in this repository. The goal is to make every future product start from the same safe operating baseline.

## Default service factory loop

1. Capture a product request with `/goal`.
2. Convert it into a PRD and implementation plan.
3. Select the service template contract.
4. Let local Codex or Hermes implement in a branch or worktree.
5. Validate locally and through API-key-free GitHub Actions.
6. Open a reviewable PR with evidence.
7. Human approves merge and production-sensitive steps.
8. Record decisions, failures, QA results, and revenue lessons into memory.

## Basecamp layers

| Layer | Purpose | Default |
| --- | --- | --- |
| Product intake | Define what to build and why | `/goal` → PRD → PLAN |
| Worker | Implement and fix safely | Local Codex first, Hermes optional |
| Service template | Start new products consistently | Web-first Next.js starter plus contract |
| Validation | Catch regressions before merge | `validate.sh`, CI PR check, browser QA wrapper |
| Deployment | Run cheaply and reversibly | Single VPS + Docker Compose + Caddy |
| Operations | See and recover system state | Admin, health, logs, backup, restore |
| Revenue | Monetize without lock-in | Billing adapter, subscription and credit ledger |
| Design | Keep products polished and human | Senior design layer and reference library |
| Memory | Improve over time | JSON default, Graphiti optional |

## Reference stack

- Web app: Next.js App Router + TypeScript. Next.js supports self-hosting through Node.js or Docker, which fits the VPS baseline. See [Next.js App Router](https://nextjs.org/docs/app) and [Next.js self-hosting](https://nextjs.org/docs/app/guides/self-hosting).
- Containers: Docker Compose for multi-container local/production stacks. See [Docker Compose](https://docs.docker.com/compose/) and [Compose production guidance](https://docs.docker.com/compose/how-tos/production/).
- Reverse proxy: Caddy for HTTPS and reverse proxying. See [Caddy reverse_proxy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy).
- Database: PostgreSQL with dump-based backup and restore. See [PostgreSQL backup dump docs](https://www.postgresql.org/docs/current/backup-dump.html).
- ORM: Drizzle with migration/export flow. See [Drizzle migrations](https://orm.drizzle.team/docs/migrations).
- Payments: Stripe-first billing adapter with webhook-driven state changes. See [Stripe subscription webhooks](https://docs.stripe.com/billing/subscriptions/webhooks).

## Web-first, app-expandable rule

The first shipped surface should be web unless a PRD explicitly proves that native mobile is required first.

Every service should still keep app expansion possible by:

- keeping business logic outside UI components
- exposing typed API/service boundaries
- preserving mobile-safe auth and session rules
- keeping subscription and credit state server-owned
- designing responsive layouts and mobile-friendly flows from day one
- using the senior design layer before accepting UI-heavy work

## Monthly VPS budget

The default production baseline must fit under 100,000 KRW per month for one small service.

Default target:

- 2 vCPU or better
- 4 GB RAM or better
- 60 GB storage or better
- single region
- Docker Compose stack
- external DNS
- off-box or downloadable encrypted backups when possible

If a product needs more than this, the PRD must call it out as an operational cost decision.

## Safety boundaries

- No tracked secrets.
- No direct protected-branch pushes.
- No autonomous production deployment.
- No billing, auth, or deployment change without explicit approval.
- No merge until required checks pass.
- No self-improvement proposal auto-merge.

## Current template layer

The repository starter should continue following:

- [`service-template-contract.md`](./service-template-contract.md)
- [`vps-deployment-contract.md`](./vps-deployment-contract.md)
- [`revenue-system-contract.md`](./revenue-system-contract.md)
- [`admin-observability-contract.md`](./admin-observability-contract.md)
