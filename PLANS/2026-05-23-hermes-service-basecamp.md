# Hermes Service Basecamp Plan

## Source PRD

- `PRD/2026-05-23-hermes-service-basecamp.md`

## Status

- approved for implementation from the user-provided proposed plan

## Platform target

- docs
- runtime-readiness

## Affected areas

- Product Factory docs
- runtime readiness output
- validation script
- docs index and README links

## Tasks

1. Add service basecamp contracts:
   - architecture
   - product template
   - Hermes service factory
   - VPS deployment
   - revenue system
   - admin and observability
2. Update existing Product Factory docs to point future service creation to the basecamp contracts.
3. Add a static `service_basecamp` section to operator readiness with no external service requirements.
4. Tighten validation so the new contracts are required and workflow files do not require optional service dependencies.
5. Run validation and report exact results.

## Risks and edge cases

- Do not add package dependencies.
- Do not implement live auth, payment, deployment, or secret handling.
- Do not require Docker, Caddy, PostgreSQL, Stripe, Toss, Hermes, Paperclip, Graphiti, or Neo4j for normal validation.
- Keep future service templates as contracts only in this phase.

## Validation commands

```bash
python3 -m codex_runtime --operator-readiness --pretty
./scripts/validate.sh
./scripts/ci-pr-check.sh
git diff --check
```

## Review gates

- QA: docs are complete enough for the next engineer to scaffold the first service template.
- Security: no tracked secrets or live provider credentials.
- Delivery: GitHub Actions remain API-key-free and optional-service-free.

## Release / rollback notes

- This phase is docs/readiness only.
- Rollback is a normal revert of the added docs and readiness checks.
