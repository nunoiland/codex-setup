# Senior Design Layer Plan

## Source PRD

- `PRD/2026-05-24-senior-design-layer.md`

## Status

- approved for implementation from the user-provided proposed plan

## Platform target

- docs
- agent-config
- runtime-readiness

## Affected areas

- Design operating docs
- Product Factory service template docs
- Codex agent configs
- Operator readiness output
- Validation script

## Tasks

1. Add design reference, design system, senior review, and visual QA contracts.
2. Add `senior_product_designer` agent config with strict review boundaries.
3. Link the design layer from README, docs index, service template, and design guide.
4. Add design layer readiness output without requiring external tools.
5. Tighten validation so the docs and agent config are required.
6. Run validation and report exact results.

## Risks and edge cases

- Do not install Storybook, Chromatic, Figma, Playwright visual diff, or any dependencies.
- Do not copy reference code, assets, screenshots, branding, or trade dress.
- Do not make GitHub Actions depend on external design tooling.
- Keep reference use as product/design guidance only.

## Validation commands

```bash
python3 -m codex_runtime --operator-readiness --pretty
./scripts/validate.sh
./scripts/ci-pr-check.sh
git diff --check
```

## Review gates

- QA: docs are decision-useful for the future `web-saas` scaffold.
- Security/legal: no copied assets, secrets, or dependency additions.
- Design: senior designer agent and checklist are explicit enough to enforce quality.

## Release / rollback notes

- This phase is docs/readiness/agent-config only.
- Rollback is a normal revert of the added docs, agent config, readiness field, and validation checks.
