# Product Template Repo Transition PRD

## Goal

Turn `codex_set` into a runnable personal product template repository that can be used as a GitHub template for new web-first SaaS products while preserving the full Codex operating stack.

## Summary

- Keep `.codex`, `.agents`, workflows, scripts, runtime, and Product Factory docs in every generated product repository.
- Add a minimal but runnable Next.js App Router starter at the repository root.
- Add a safe bootstrap script that personalizes product-facing metadata without touching secrets, remotes, or deployment state.
- Keep risky integrations such as auth, billing, provider setup, and production deployment as placeholders or contracts only.

## Scope

- In scope:
  - root web starter
  - package manager and validation integration
  - bootstrap script
  - template-repo documentation refresh
  - Docker baseline
- Out of scope:
  - live auth wiring
  - live billing/provider wiring
  - real database migrations
  - production deployment mutation
  - remote repository rename or push automation

## Acceptance Criteria

1. The repository has a runnable web-first starter with landing, `/app`, `/admin`, and `/health`.
2. `./scripts/validate.sh` covers runtime/docs guards plus lint, typecheck, and build for the starter.
3. `./scripts/ci-pr-check.sh` includes a web health smoke check.
4. `python3 scripts/bootstrap-template.py --slug sample-product --name "Sample Product" --dry-run` reports bootstrap changes without mutating tracked files.
5. GitHub Actions remain API-key-free and install starter dependencies explicitly before validation.

## Secret Profile

No new tracked secrets are allowed. Product-specific auth, billing, provider, and deployment values must remain externally injected.

## Validation Commands

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
python3 scripts/bootstrap-template.py --slug sample-product --name "Sample Product" --dry-run
```
