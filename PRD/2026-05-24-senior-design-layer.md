# Senior Design Layer

## Goal

Add a senior-designer-quality operating layer to `codex-setting` so future services are not only functional and safe, but also visually coherent, product-specific, accessible, and commercially polished.

The design layer should turn selected open-source product references into reusable design direction, review gates, and future visual QA expectations.

## Scope

- In scope:
  - Document a design reference library based on Midday, Dub, PostHog, Huly, and Twenty.
  - Add a design system contract for future service templates.
  - Add a senior designer review checklist.
  - Add a visual QA contract for future screenshot, Storybook, or visual regression checks.
  - Add a `senior_product_designer` agent configuration.
  - Link the design layer from existing docs and validation.
- Out of scope:
  - Installing Storybook, Chromatic, Playwright visual diff, or design dependencies.
  - Copying code, assets, visual identity, trademarks, or proprietary design from reference repositories.
  - Creating a runnable UI scaffold.
  - Adding Figma, external design services, or new secrets.

## Non-goals

- Do not replace the existing `DESIGN.md`; extend it with reference-backed contracts.
- Do not make GitHub Actions require Storybook, Chromatic, Figma, or any design SaaS.
- Do not claim visual QA exists until a real product template and screenshot flow are implemented.

## Context

The repository already has a general design operating guide and a `ui_specialist` agent, but it lacks a clear reference library and a stronger senior product design review gate.

The user selected five strong references:

- `midday-ai/midday` for premium indie SaaS tone, spacing, typography, and calm density.
- `dubinc/dub` for landing, analytics, dashboard, table, settings, and B2B trust.
- `PostHog/posthog` for distinctive brand voice and human product personality.
- `hcengineering/platform` for complex work-app structure and high-density collaboration UI.
- `twentyhq/twenty` for CRM-like data-heavy SaaS screens.

## Constraints

- References are inspiration only.
- Keep all design additions dependency-free.
- Keep accessibility, responsive behavior, and state design required.
- Preserve the default API-key-free GitHub Actions path.
- Keep design output reviewable through PRs and validation.

## Acceptance criteria

1. Design reference library exists and captures what to borrow and avoid from each reference.
2. Design system contract exists and defines tokens, components, page patterns, states, and density rules.
3. Senior designer review checklist exists and can be used before and after UI implementation.
4. Visual QA contract exists and keeps Storybook/screenshot tooling future-optional.
5. A senior product designer agent exists under `.codex/agents`.
6. README and docs index link the new design layer.
7. Validation requires the new docs and agent config.

## Edge cases

- A future product copies reference UI too closely.
- A future product becomes generic AI-looking despite using shadcn/Tailwind.
- Data-heavy screens become cramped and unreadable.
- Landing pages look polished but admin screens lack quality.
- Visual QA is skipped because no screenshot baseline exists yet.
- Accessibility is treated as an afterthought.

## Platform target

- docs
- agent-config
- runtime-readiness

## Delivery mode

- existing repository + branch + draft PR
- no protected branch direct push by default

## Reporting mode

- local_thread
- github

## Secret profile

- Required secret: none.
- Future optional design tooling secrets, if any, must be injected externally and are out of scope for this phase.

## Human handoff

- QA checks:
  - Confirm docs reference the intended design direction.
  - Confirm no reference code or assets were copied.
  - Confirm validation passes without design SaaS or new dependencies.
- Manual release or infra tasks:
  - None.
- Final approver:
  - repository operator.

## Validation commands

```bash
python3 -m codex_runtime --operator-readiness --pretty
./scripts/validate.sh
./scripts/ci-pr-check.sh
git diff --check
```

## Done when

- Senior design docs and agent config are present.
- Readiness and validation acknowledge the design layer.
- No dependency, secret, or external design service is required.
