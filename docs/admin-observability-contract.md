# Admin and Observability Contract

Every service created from this basecamp needs enough operational visibility to support real users.

The goal is not enterprise observability in v1. The goal is to diagnose failures, protect users, and recover safely on a small VPS.

## Required admin areas

Future services should include `/admin` with:

- overview dashboard
- users
- subscriptions or entitlements
- credits and ledger
- payments and billing events
- background jobs
- audit logs
- error logs
- deploy or release notes
- backup status

Admin access must require explicit authorization, not only authentication.

## Audit log requirements

Audit these events:

- admin login
- admin role or permission changes
- user suspension or restoration
- plan or entitlement changes
- credit adjustments
- payment/refund actions
- data export
- destructive or irreversible actions
- configuration changes

Audit records should include:

- actor
- action
- target
- timestamp
- reason when manually triggered
- request or correlation id when available

Do not store secrets in audit logs.

## Error log requirements

Capture:

- unhandled server errors
- failed webhooks
- failed jobs
- failed database operations
- failed auth/session checks
- failed external provider calls

Error logs should be useful without exposing secrets, tokens, payment card data, or private payloads.

## Job log requirements

For background jobs, record:

- job type
- status
- start and finish time
- retry count
- failure reason
- related user or entity when safe

Retries must be bounded. Repeated failures should become visible admin issues, not silent loops.

## Health and status

The service should provide:

- public-safe `/health`
- admin-only deeper status
- latest deploy version
- database connection status
- queue or worker status
- backup recency

## Backup visibility

Admin or ops docs should answer:

- when the last backup ran
- whether it succeeded
- where restore instructions live
- when restore was last tested
- what data may be lost after rollback

## Privacy and security notes

- Never log raw secrets.
- Never log full provider webhook secrets or auth tokens.
- Mask email or personal data where possible in shared reports.
- Keep admin actions least-privilege.
- Require human approval for destructive user or billing actions.
