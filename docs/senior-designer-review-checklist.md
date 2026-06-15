# Senior Designer Review Checklist

Use this checklist before accepting UI work as complete.

The goal is to catch generic, low-quality, confusing, or inaccessible UI before it reaches a PR merge.

## 3-second test

- The screen purpose is clear within three seconds.
- The primary action is obvious.
- The current state or status is visible.
- The user can tell what changed after an action.

## Information hierarchy

- Page title, primary action, and status are correctly prioritized.
- Related content is grouped.
- Secondary actions do not compete with primary actions.
- Destructive actions are visually and behaviorally distinct.
- Dense screens still preserve scanning paths.

## Visual quality

- Spacing rhythm is consistent.
- Typography scale is restrained and intentional.
- Cards and panels have a clear reason to exist.
- Color is semantic and not decorative noise.
- The screen does not look like a generic AI-generated SaaS template.

## Reference alignment

- The PRD names a primary design reference when UI quality matters.
- Borrowed patterns are adapted, not copied.
- The UI matches the intended product archetype.
- The product still has its own point of view.

## State quality

Confirm the relevant states exist:

- loading
- empty
- error
- success
- disabled
- permission denied
- offline or degraded when relevant

State copy must explain what happened and what to do next.

## Accessibility

- Keyboard focus is visible.
- Icon-only controls have accessible labels.
- Color is not the only way to convey state.
- Text contrast is sufficient.
- Modal, drawer, and menu behavior is keyboard-safe.
- Reduced-motion preferences are respected when motion exists.

## Responsive behavior

- Mobile layout keeps the primary action accessible.
- Tablet layout does not feel like stretched mobile.
- Desktop layout uses space for efficiency, not clutter.
- Long text and localized labels do not break the layout.
- Tables have a small-screen strategy.

## Product copy

- Copy is specific to the product and user.
- Empty states are helpful, not cute filler.
- Error messages are actionable.
- Pricing and billing copy is precise.
- Admin and destructive action copy states consequences clearly.

## Data-heavy screens

For admin, analytics, CRM, or dashboard screens:

- Columns are prioritized.
- Filters are discoverable.
- Row actions are predictable.
- Bulk actions are safe.
- Metrics have units, time ranges, and context.
- Empty dashboards do not show fake confidence.

## Final acceptance

Do not accept UI as done if:

- the primary flow cannot be understood without explanation
- important states are missing
- visual polish only exists on the landing page
- admin/settings screens look unfinished
- accessibility is unverified
- screenshot/browser QA was skipped without explanation
