# Service Template Contract

This contract defines the first standard product template that generated services should use.

This repository now includes a runnable starter that follows this contract at a minimal safe depth.

## Template target

Name: `web-saas`

Use for:

- SaaS products
- AI utilities
- content tools
- admin-backed marketplaces
- internal tools that may become products

Do not use for:

- native-app-first products
- high-throughput infrastructure services
- products that require managed Kubernetes or multi-region from day one

## Default stack

| Area | Default |
| --- | --- |
| Runtime | Node.js LTS |
| Package manager | `pnpm` |
| Web framework | Next.js App Router |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Component base | shadcn/ui-compatible component structure |
| Database | PostgreSQL |
| ORM | Drizzle |
| Auth boundary | Auth.js-compatible server-owned session model |
| Billing boundary | Provider adapter, Stripe first |
| Deployment | Docker Compose on a single VPS |

## Required service surfaces

Every generated service must include:

- public landing page
- authenticated app shell
- account/settings area
- admin area under `/admin`
- health endpoint under `/health`
- audit log
- error log
- job log
- payment or billing event log when monetization is enabled
- backup and restore runbook
- local validation script
- Docker Compose production baseline

## Architecture rules

- Keep business logic out of React components.
- Keep provider-specific billing logic behind adapter boundaries.
- Keep auth/session checks server-owned.
- Keep credit changes ledger-based.
- Keep admin actions audited.
- Keep schema changes migration-backed.
- Keep UI responsive enough for mobile web before native apps exist.

## Folder expectations for the starter

The starter should use a predictable layout:

```text
src/
  app/
  components/
  config/
  db/
  domain/
  jobs/
  lib/
  server/
  services/
  validation/
ops/
  deploy/
  backup/
  restore/
tests/
```

Exact file names may vary by product, but boundaries should not.

## Required validation

The generated service must provide commands for:

- typecheck
- lint
- unit tests
- migration dry-run
- Playwright or browser smoke test
- Docker build
- healthcheck smoke test
- senior designer review using `docs/senior-designer-review-checklist.md`
- screenshot or visual QA evidence once the service has a runnable UI

The template repository should validate the starter surfaces it actually ships, and leave deeper product-specific checks for later expansion.

## Design system requirements

The future template must follow:

- [`DESIGN.md`](./DESIGN.md)
- [`design-reference-library.md`](./design-reference-library.md)
- [`design-system-contract.md`](./design-system-contract.md)
- [`senior-designer-review-checklist.md`](./senior-designer-review-checklist.md)
- [`visual-qa-contract.md`](./visual-qa-contract.md)

The default visual direction is premium, restrained, human, and product-specific. Do not ship generic AI-style UI.

## App expansion path

When native apps are added later:

- reuse server-owned auth/session rules
- reuse billing and credit APIs
- keep app-specific UI separate from web UI
- keep entitlement decisions on the backend
- preserve one product-state model across web, iOS, and Android
