# Visual QA Contract

This contract defines how future services should verify visual quality.

This repository does not install visual QA tools in the current phase. The contract becomes active when a generated service has a runnable UI.

## Current phase

- No Storybook dependency.
- No Chromatic dependency.
- No Figma dependency.
- No screenshot baseline required for `codex-setting` validation.
- Browser QA may continue to skip when no web target is configured.

## Future service requirement

When `templates/web-saas` or a product repo exists, add one of:

- Playwright screenshot smoke tests
- Storybook component stories with accessibility checks
- Chromatic or equivalent visual regression if an external visual QA service is approved
- local screenshot diff if external SaaS is not approved

## Required screenshots

At minimum, capture:

- landing page
- pricing page when monetization exists
- login/auth surface
- onboarding first step
- dashboard overview
- table/list page
- settings page
- billing page when monetization exists
- admin overview
- loading, empty, and error states for one critical flow

## Review rules

- Screenshots are evidence, not decoration.
- Visual changes should be reviewed intentionally in PRs.
- Do not auto-accept visual diffs without human review.
- Accessibility failures must be treated as quality failures.
- Screenshot artifacts must not expose secrets or private user data.

## CI behavior

Default `codex-setting` CI must remain API-key-free and visual-SaaS-free.

Future product repos may add visual QA only when:

- the PRD approves the tool
- secrets are external
- costs are understood
- screenshots are sanitized
- required checks are documented

## Senior designer handoff

Every UI-heavy PR should report:

- design reference used
- screens changed
- states verified
- screenshots captured or reason skipped
- accessibility checks run or reason skipped
- known polish follow-ups
