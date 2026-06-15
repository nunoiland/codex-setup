# Future Codex Action Option

This is a phase-2 option only. It is not active in the current API-key-free setup.

## Current status

- No workflow uses `openai/codex-action`.
- No workflow requires `OPENAI_API_KEY`.
- AI implementation and fixing stay local in the Codex app or CLI.
- GitHub Actions only validates, collects evidence, and gates merges.

## When to consider this

Consider adding `openai/codex-action` only when all of these are true:

- you explicitly want AI review or AI fixes to run inside GitHub Actions
- you accept OpenAI API usage and cost from CI
- the repository has clear branch protection and review rules
- secrets are managed through GitHub Secrets
- generated changes still require human review before merge

## Minimum security rules

- Store the API key only as a GitHub Secret.
- Never print the key in logs.
- Use the smallest practical workflow permissions.
- Keep AI write jobs separate from validation jobs.
- Do not allow AI jobs to merge their own changes.
- Keep `automerge-approved` human-controlled.

## Suggested phase-2 shape

If enabled later, add a separate workflow such as:

- `codex-review.yml` for AI review comments
- `codex-fix.yml` for manually triggered AI fix PR updates

Keep `pr-validate.yml` as the required non-AI gate. That way the repository still has an API-key-free source of truth for whether the PR is mechanically safe.

## Rollback

To return to phase 1:

- delete or disable the Codex Action workflow
- remove `OPENAI_API_KEY` from GitHub Secrets if no longer needed
- keep `pr-validate`, `nightly-harness`, and `automerge`
