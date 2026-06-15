---
name: frontend-taste-review
description: Review frontend and product UI work for brief fit, non-generic design taste, layout rhythm, accessibility, states, and design-system consistency.
---

# Frontend Taste Review

Use before accepting UI-heavy work, redesigns, landing pages, onboarding, dashboards, pricing, settings, and admin screens.

## Workflow

1. State the design read: audience, product type, trust level, and intended visual language.
2. Check the chosen design system or project-native component pattern.
3. Review hierarchy, spacing, typography, color, density, motion, and responsive behavior.
4. Verify required states: loading, empty, error, disabled, success, permission, and offline where relevant.
5. Check accessibility: keyboard, focus, contrast, screen-reader labels, touch targets, and reduced motion.
6. Flag generic AI patterns and suggest the smallest fix.

## Rules

- Work with the existing stack and design system.
- Do not require new libraries, GSAP, icon sets, SaaS tools, or external assets by default.
- Design references guide taste only; never copy code, assets, logos, exact layouts, or brand identity.
- Prefer product-specific copy and real state handling over visual decoration.
- Public trust, billing, auth, admin, and data-heavy screens must favor clarity over novelty.

## Output

Return:

- design read
- pass/fail summary
- findings by severity
- smallest recommended fixes
- screenshot or browser QA gaps
