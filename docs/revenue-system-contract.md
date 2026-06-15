# Revenue System Contract

This contract defines the default monetization model for future services.

The goal is to make every product ready for subscriptions and credits without hardcoding a single provider into domain logic.

## Default provider strategy

- Stripe is the first billing adapter for global SaaS.
- Toss Payments may be added as a Korean payment adapter when the PRD requires it.
- Provider credentials, webhook secrets, and live product IDs stay outside tracked files.

## Domain primitives

Future service templates should support these concepts:

| Primitive | Purpose |
| --- | --- |
| `users` | Account identity |
| `plans` | Sellable product tiers |
| `subscriptions` | Recurring entitlement state |
| `payments` | Payment attempts and results |
| `invoices` | Billing documents or provider invoice references |
| `credits` | Current credit balance projection |
| `credit_ledger` | Source of truth for credit changes |
| `usage_events` | Billable or quota-consuming activity |
| `refunds` | Reversal tracking |
| `audit_logs` | Admin and system action history |

Exact schema is template-specific, but the invariants are not.

## Invariants

- Payment state changes must come from verified provider events.
- Webhooks must be idempotent.
- Duplicate or out-of-order webhooks must not double-credit users.
- Credit balance must be derived from a ledger, not edited directly.
- Admin credit adjustments require reason and audit log.
- Subscription entitlement checks must be server-owned.
- Provider customer IDs must not become the only user identity.

## Billing adapter boundary

Provider-specific code should live behind a billing adapter with responsibilities such as:

- create checkout session
- read subscription status
- verify webhook signature
- normalize webhook event
- map provider plan IDs to internal plans
- record payment, invoice, refund, and subscription changes

Domain logic should consume normalized events, not raw provider payloads.

## Required logs

When monetization is enabled, the admin surface must expose:

- payment events
- webhook processing attempts
- subscription changes
- credit ledger entries
- admin credit adjustments
- refund events
- failed billing jobs

## Human approval boundaries

Require explicit approval before:

- enabling live payments
- changing plan prices
- changing credit grant rules
- issuing refunds
- bulk-adjusting credits
- running billing migrations
- exposing paid features publicly

## Template phase boundary

This basecamp phase does not implement Stripe or Toss code. It defines the contract future service templates must follow.
