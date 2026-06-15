# Plan: Product Template Repo Transition

## Source

- `PRD/2026-06-02-template-repo-transition.md`
- user-approved implementation plan for turning `codex_set` into a runnable GitHub template repo

## Implementation

1. Add root web starter files for Next.js App Router, TypeScript, Tailwind, lint, and build.
2. Add product-facing starter routes:
   - landing page
   - `/app` placeholder
   - `/admin` placeholder
   - `/health` JSON route
3. Add bootstrap support:
   - `scripts/bootstrap-template.py`
   - product config placeholders
   - dry-run support
4. Add Docker baseline and starter-specific ignore rules.
5. Extend validation and CI:
   - install dependencies in workflows
   - run lint/typecheck/build in `validate.sh`
   - run health smoke check in `ci-pr-check.sh`
6. Refresh core docs so the repository is described as a GitHub template repo and personal product OS.

## Validation

```bash
pnpm install
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
python3 scripts/bootstrap-template.py --slug sample-product --name "Sample Product" --dry-run
```

## Risks

- Dependency installation increases local and CI setup time.
- Build/lint failures now block repository validation because a runnable starter exists.
- Bootstrap must stay narrow to avoid accidental mass rewrites of non-product docs.
