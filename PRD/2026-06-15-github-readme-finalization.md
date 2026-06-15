# PRD: GitHub README Finalization

## Goal

Make the GitHub README clearly explain what this Codex setting/product template contains, how to use it, and what safety boundaries remain.

## Scope

- Reorganize the root `README.md` for GitHub readers.
- Keep the `TEMPLATE_IDENTITY` block intact for bootstrap compatibility.
- Add a concise inventory of the operating stack, agents, validation, security, and optional future layers.
- Link the product workspace boundary guard added in the previous hardening change.
- Run validation and QA checks after editing.

## Non-goals

- Do not add dependencies.
- Do not change runtime behavior outside documentation/readme wiring.
- Do not add secrets, deployment automation, auth, billing, or third-party service setup.
- Do not commit or push unless explicitly requested after QA.

## Acceptance criteria

1. README explains the repo as a personal product template and local Codex operating system.
2. README lists included capabilities without hype or unsupported claims.
3. README makes clear that GitHub Actions remain API-key-free.
4. README explains the product repo boundary: real products should live outside `codex_set`.
5. `./scripts/validate.sh` and `./scripts/ci-pr-check.sh` pass.

## Delivery mode

- local repo change
- GitHub-ready documentation update

## Reporting mode

- github_only

## Secret profile

- Required secret: none
- Source of injection: none

## Validation commands

```bash
git diff --check
./scripts/validate.sh
./scripts/ci-pr-check.sh
python3 -m codex_runtime --operator-readiness --pretty
```
