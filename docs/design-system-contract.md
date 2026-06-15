# Design System Contract

Future services should start from a small, durable design system rather than one-off screens.

This contract defines the minimum design system expected by the future `web-saas` template.

## Design direction

Default tone:

- calm
- premium
- practical
- human
- trustworthy
- not generic AI

Primary taste anchor: Midday-style premium SaaS restraint.

Secondary anchors:

- Dub for B2B trust and dashboards
- PostHog for product personality
- Twenty for data-heavy screens
- Huly for complex app shells

## Token requirements

Every service template should define:

- color tokens for background, surface, border, text, muted text, brand, success, warning, error, info
- typography scale for display, heading, body, caption, label, and mono
- spacing scale with consistent section, card, form, and list rhythm
- radius scale for controls, cards, and panels
- shadow/elevation rules with restrained usage
- density modes for comfortable and data-dense screens
- focus ring and keyboard state tokens
- chart and analytics color tokens when dashboards exist

## Component requirements

Minimum reusable components:

- button
- input
- textarea
- select/combobox
- checkbox/radio/switch
- form field with label, hint, and error
- card/panel
- table/data grid wrapper
- tabs
- dialog/sheet/drawer
- dropdown/menu
- toast/notification
- empty state
- error state
- loading state
- badge/status pill
- metric card
- sidebar/nav item
- breadcrumbs

Components must define:

- default, hover, active, disabled, loading, focus, error states
- accessible labels and keyboard behavior
- responsive behavior
- density behavior for admin/data screens

## Page pattern requirements

Future products should provide patterns for:

- landing page
- pricing page
- onboarding flow
- authenticated app shell
- dashboard overview
- table/list page
- record/detail page
- settings page
- billing/subscription page
- admin overview
- empty/error/permission pages

## Layout rules

- Landing pages should be clear and conversion-oriented without excessive motion.
- App shells should prioritize navigation clarity and current state.
- Dashboards should show decision-relevant metrics first.
- Tables should preserve scanability with stable columns and clear row actions.
- Settings should be grouped by user mental model, not internal implementation.
- Admin views should prefer clarity, auditability, and safe actions over visual flair.

## Anti-generic-AI rules

Avoid:

- random purple/blue gradients
- excessive glassmorphism
- floating cards without structure
- generic sparkle or robot motifs
- over-rounded pill everything
- fake dashboards with meaningless metrics
- decorative animation that does not clarify state

Prefer:

- real product copy
- specific empty states
- honest data labels
- calm transitions
- consistent spacing rhythm
- clear status language

## Accessibility baseline

Design and implementation must support:

- keyboard navigation
- visible focus state
- semantic headings and labels
- sufficient color contrast
- non-color-only status communication
- reduced motion support
- screen-reader friendly labels for icon-only controls

## Review requirement

Before UI implementation:

- choose primary and secondary references
- define target feel
- identify the page pattern
- list required states

After UI implementation:

- run senior designer review
- run browser/screenshot QA when the product has a runnable UI
- record follow-up polish issues instead of hiding them
