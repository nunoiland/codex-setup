# Secret Policy

This repository treats secrets as external runtime inputs, never as tracked source files.

## Core rules

- Never commit secrets to the repository.
- Never place secrets in PRDs, plans, README examples, or tracked templates.
- Never hardcode GitHub credentials, provider keys, production passwords, or service tokens.
- Use least privilege for every credential.
- Separate creation, delivery, reporting, and deployment credentials whenever possible.

## Secret classes

### GitHub credentials

Use for:
- repository creation
- branch creation
- commit and push
- PR creation

Preferred order:
1. GitHub App with narrow repository permissions
2. fine-grained PAT when GitHub App is not practical

Avoid:
- broad classic PATs
- shared long-lived credentials with unnecessary org-wide scope

### LLM or provider keys

Use for:
- model inference
- research or analysis tools
- external orchestration integrations

Rules:
- inject from environment or external secret manager
- scope to the minimum set of services needed
- rotate if exposure is suspected

### Reporting artifacts

- local handoff artifacts must not contain real credentials
- reporting output must redact private URLs and tokens
- do not embed secrets in docs or tracked config

### Deployment or infrastructure secrets

These stay outside the repository and outside unattended coding runs unless the PRD explicitly allows a safe documented handoff.

Examples:
- cloud credentials
- production database passwords
- signing keys
- DNS provider tokens

## Approved storage locations

Prefer one of:

- GitHub App installation credentials
- GitHub repository or organization secrets
- local environment injection outside tracked files
- dedicated secret manager such as 1Password, Doppler, Vault, or equivalent

## What can be tracked

Tracked files may include:

- placeholder names
- secret IDs or variable names
- `.env.example` style examples without real values
- documentation explaining who owns a secret and where it is injected

Tracked files may not include:

- real tokens
- service tokens
- live passwords
- private keys

Common local secret files such as `.env`, `.env.local`, `.env.*`, `.pem`, and `.key` files should stay ignored unless there is a very explicit, reviewed reason to track a non-secret placeholder.

## Ownership and approval

Each delivery-oriented PRD should define:

- required secret
- source of injection
- owner or approver

If any of those are unknown, the run should stop or mark the dependency as a blocker.

## Rotation and exposure response

If a secret is exposed or suspected to be exposed:

1. revoke or rotate it immediately
2. remove it from any temporary files or logs if possible
3. document the exposure in the handoff
4. re-run only after a safe replacement is available

## Policy for examples and demos

Examples in this repository must always use:

- placeholder service identifiers
- placeholder environment variable names

Never use “real-looking” sample values that could be mistaken for active credentials.

## Validation reminder

Before using real credentials against real repositories, follow:

- [`docs/live-validation-playbook.md`](./live-validation-playbook.md)


## Strategy and self-improvement outputs

- Strategy drafts, launch ideas, pricing options, and self-improvement proposals must not contain real secrets.
- Future publishing credentials for WordPress, Threads, video, or other channels must remain external and optional until explicitly approved.
