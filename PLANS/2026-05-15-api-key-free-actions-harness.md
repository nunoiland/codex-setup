# API-key-free Actions and Harness Plan

## Summary

Codex-setting phase 1 runs AI work locally only. GitHub Actions validates PRs, collects harness evidence, runs browser QA wrappers, and performs label-gated squash merge without requiring `OPENAI_API_KEY`.

## Implemented scope

- Add PR validation workflow.
- Add nightly dry-run harness workflow.
- Add same-repository `automerge-approved` squash merge workflow.
- Add API-key-free CI wrapper script.
- Add browser QA wrapper with skip evidence when no web target is configured.
- Add dry-run harness report generation from captured check logs.
- Document how to use the setup and keep `openai/codex-action` as a future option only.

## Non-goals

- No AI review inside GitHub Actions.
- No AI code fixes inside GitHub Actions.
- No self-hosted runner default path.
- No `OPENAI_API_KEY` requirement.

## Validation

Run:

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
```

Then test on GitHub with a temporary PR:

- confirm `pr-validate` runs without API secrets
- confirm evidence artifact uploads
- confirm no merge happens without `automerge-approved`
- confirm squash merge happens only after `pr-validate` passes and the label is added
