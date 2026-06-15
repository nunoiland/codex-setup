# Taste and Copy Quality Contract

This contract keeps generated UI and prose from feeling generic, overproduced, or AI-written.

## Design taste review

Use for:

- landing pages
- onboarding
- dashboards
- pricing
- settings
- admin screens
- visual QA handoff
- redesigns of existing products

Review for:

- brief fit before style choices
- one clear product point of view
- restrained palette and consistent accent use
- non-generic layout rhythm
- useful motion only when it clarifies state
- full loading, empty, error, disabled, focus, and responsive states
- design-system consistency over decorative novelty

Do not require:

- GSAP
- random layout generation
- external image services
- new icon libraries
- new component libraries
- visual SaaS

## Copy quality review

Use for:

- PRDs
- README and docs
- landing copy
- app microcopy
- pricing and billing copy
- release notes and handoffs
- investor or marketing drafts

Review for:

- direct language
- specific nouns and verbs
- active voice
- product-specific details
- no hype, filler, or vague claims
- no fake urgency or inflated certainty
- no formulaic AI structure

## Scoring

Reviewer output should score 1 to 5:

- clarity
- specificity
- trust
- density
- human tone

Any score below 3 requires concrete edits before final handoff.

## Levels

- `CODEX_TASTE_REVIEW_LEVEL=standard|strict`
- `CODEX_COPY_REVIEW_LEVEL=standard|strict`

Standard catches quality regressions. Strict applies to public-facing docs, landing pages, pricing, investor materials, and regulated or trust-sensitive product surfaces.
