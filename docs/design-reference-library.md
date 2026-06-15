# Design Reference Library

This library captures the product design references that should guide future services created from `codex-setting`.

References are for direction only. Do not copy code, assets, logos, illustrations, exact layouts, or brand identity without checking licenses and ownership.

## Default taste hierarchy

1. **Midday** for the default premium SaaS feel.
2. **Dub** for B2B trust, landing, analytics, and settings patterns.
3. **PostHog** for brand personality and human product voice.
4. **Twenty** for data-heavy CRM/admin quality.
5. **Huly** for complex collaboration and desktop-grade app density.

## References

| Reference | Use for | Borrow | Avoid |
| --- | --- | --- | --- |
| [midday-ai/midday](https://github.com/midday-ai) | Premium indie SaaS baseline | calm spacing, restrained cards, clean typography, business OS feel | copying finance-specific flows or brand identity |
| [dubinc/dub](https://github.com/dubinc/dub) | B2B SaaS trust | landing clarity, analytics cards, tables, settings IA, pricing trust | overfitting to link-management concepts |
| [PostHog/posthog](https://github.com/PostHog/posthog) | Product personality | distinctive copy, playful but useful brand tone, product-led education | making every product quirky or visually loud |
| [hcengineering/platform](https://github.com/hcengineering/platform) | Complex app shell | dense workspaces, sidebars, collaboration structure, desktop-grade UX | bringing heavy multi-app complexity into MVPs too early |
| [twentyhq/twenty](https://github.com/twentyhq/twenty) | Data-heavy SaaS | CRM lists, record detail, object views, sidebar/settings patterns | copying CRM domain assumptions into unrelated products |

## How to use references in a PRD

Every UI-heavy PRD should include a short design direction:

```text
Design reference:
- Primary reference:
- Secondary reference:
- Borrow:
- Avoid:
- Target feel:
```

Example:

```text
Design reference:
- Primary reference: Midday
- Secondary reference: Dub
- Borrow: calm business SaaS spacing, clear analytics cards, trustworthy settings
- Avoid: finance-specific flows, link-management-specific copy
- Target feel: premium solo-founder business tool
```

## Product archetype mapping

| Product type | Primary references |
| --- | --- |
| Solo founder or freelancer tool | Midday + Dub |
| Marketing or analytics SaaS | Dub + PostHog |
| Data-heavy admin or CRM | Twenty + Dub |
| Complex collaboration app | Huly + Twenty |
| AI utility that must not feel generic | Midday + PostHog |

## Non-negotiable reference rules

- Use references to set taste, not to clone.
- Keep product-specific differentiation in copy, IA, and visual rhythm.
- Prefer fewer, stronger patterns over many borrowed fragments.
- If two references conflict, choose the simpler pattern unless the PRD proves the product needs higher density.
- Accessibility and usability override visual imitation.
