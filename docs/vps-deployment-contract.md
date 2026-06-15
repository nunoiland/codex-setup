# VPS Deployment Contract

This contract defines the default low-cost production baseline for future services.

The goal is a simple, reversible deployment that can run under 100,000 KRW per month for one small service.

## Default topology

Use one VPS with Docker Compose:

```text
internet
  -> Caddy
    -> web
    -> worker
    -> postgres
    -> backup
```

Required services for future product scaffolds:

- `web`: Next.js app
- `worker`: background jobs
- `postgres`: primary database
- `caddy`: reverse proxy and HTTPS
- `backup`: scheduled dump and retention helper

## Production Compose rules

- Do not bind-mount source code in production.
- Use built images or checked-out release code.
- Store secrets only in the server environment or secret manager.
- Keep persistent database data in named volumes or explicit server paths.
- Keep logs accessible without exposing secrets.
- Do not expose PostgreSQL directly to the public internet.

## Caddy baseline

Caddy should:

- terminate HTTPS
- redirect HTTP to HTTPS
- reverse proxy to the app container
- preserve host and client IP headers where safe
- keep Caddyfile tracked with placeholders only

## Healthcheck

Every service must expose:

```text
GET /health
```

The healthcheck should report:

- app version or commit
- process uptime
- database connectivity
- background job readiness when relevant
- degraded status without leaking secrets

## Backup

Use PostgreSQL dump-based backups as the baseline.

Required behavior:

- daily database dump
- retention policy
- manual backup command before risky deploys
- restore command documented
- restore test checklist
- encryption or restricted storage for off-box backups

PostgreSQL `pg_dump` output can be restored on newer PostgreSQL versions and is a practical baseline for small-service portability.

## Deploy flow

Default human-run deploy flow:

1. Pull or fetch the approved release branch.
2. Create a fresh backup.
3. Build containers.
4. Run migration dry-run or migration plan check.
5. Apply migration only after approval.
6. Start containers.
7. Check `/health`.
8. Check admin logs.
9. Record deploy result.

## Rollback flow

Every release must document:

- previous image or commit
- whether migrations are reversible
- database restore point
- exact rollback command
- expected downtime or degraded behavior

If migration rollback is unsafe, the PR must say so before release.

## Not included in v1

- Kubernetes
- multi-region
- managed database requirement
- blue/green automation
- unattended production deploys
- production deployment from GitHub-hosted Actions
