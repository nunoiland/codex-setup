# Design Operating Guide

## Design goal
- Deliver one recognizable product experience across Android, iOS, and Web while respecting each platform's native interaction model.
- Support global expansion by making localization, accessibility, responsiveness, and clarity part of the default design bar.
- Preserve a senior-designer-quality product feel by using the reference-backed contracts in [`design-reference-library.md`](./design-reference-library.md), [`design-system-contract.md`](./design-system-contract.md), and [`senior-designer-review-checklist.md`](./senior-designer-review-checklist.md).

## Product experience principle
- The product should feel like one brand, one system, and one level of quality everywhere.
- Platform differences should improve usability, not create a different product.
- Every screen should feel intentionally designed by humans, not generated from a generic AI pattern library.

## Core design principles
- Prefer clarity over decoration.
- Make the primary action obvious.
- Reduce cognitive load, steps, and ambiguity.
- Design for real tasks, real constraints, and imperfect conditions.
- Keep interactions predictable, learnable, and forgiving.
- Reuse proven patterns before introducing new ones.

## Visual tone
- Calm, confident, modern, and product-specific.
- Use clear hierarchy, purposeful spacing, and restrained emphasis.
- Favor strong layout rhythm and readable content over ornamental effects.
- Use illustration, motion, and accents sparingly and only when they support comprehension.

## Reference anchors
- Use Midday as the default taste anchor for premium indie SaaS restraint.
- Use Dub for B2B trust, landing, analytics, settings, and pricing patterns.
- Use PostHog for human brand voice and distinctive product personality.
- Use Twenty for data-heavy CRM, list, record-detail, sidebar, and settings quality.
- Use Huly only when the PRD needs complex collaboration or desktop-grade app density.
- References guide taste and patterns; do not copy code, assets, exact layouts, logos, or brand identity.

## Anti-patterns
- Do not ship generic AI-looking UI: glowing gradients everywhere, floating glass cards by default, excessive rounded pills, random sparkle icons, or decorative assistant motifs.
- Do not mix unrelated visual languages across platforms.
- Do not hide primary actions behind menus or ambiguous icons.
- Do not overload screens with equal-weight elements.
- Do not rely on color alone to communicate status, urgency, or errors.
- Do not let responsive layouts become stretched, sparse, or visually unbalanced.

## Cross-platform consistency rules
- Keep core information architecture, terminology, priority order, and success criteria consistent across Android, iOS, and Web.
- Keep the same meaning for colors, icons, statuses, and component states across platforms.
- Keep critical flows structurally aligned: onboarding, navigation, creation, editing, confirmation, and error recovery.
- Keep content and copy intent aligned even when controls are platform-native.
- If one platform requires a different interaction pattern, preserve the same user goal, hierarchy, and outcome.

## Platform adaptation rules
### Android
- Follow Material-aligned interaction expectations for navigation, sheets, menus, and system back behavior.
- Respect Android density, touch targets, keyboard behavior, and edge-to-edge layout conventions.
- Prefer Android-native patterns when they improve speed or learnability for Android users.

### iOS
- Follow Apple-aligned expectations for navigation stacks, modal presentation, pickers, and gestures.
- Respect iOS spacing, motion restraint, safe areas, and platform control conventions.
- Prefer iOS-native patterns when they improve familiarity and reduce friction for iPhone and iPad users.

### Web
- Optimize for mouse, keyboard, touch, and large-screen workflows.
- Use clear hover, focus, and active states.
- Design for browser resizing, multi-column layouts where useful, and efficient desktop task completion.
- Keep web interactions fast, obvious, and accessible without mimicking mobile UI unnecessarily.

## Information hierarchy
- Each screen must make the page purpose clear within one glance.
- Prioritize content in this order: page goal, current status, primary action, supporting context, secondary actions.
- Show the most decision-relevant information first.
- Group related content into clear sections with distinct headings and spacing.
- Avoid deep nesting when a flatter structure improves comprehension.

## Layout rules
- Start with a stable page frame: header, content area, primary action zone, and optional supporting panel.
- Use consistent alignment and predictable section rhythm.
- Keep reading width controlled for text-heavy screens.
- Use cards, panels, and dividers only when they improve structure.
- Avoid crowded dashboards and avoid empty layouts that waste space.

## Responsive and adaptive rules
- Design mobile-first for essential flows, then expand thoughtfully for tablet and desktop.
- On larger screens, increase efficiency with width, grouping, and parallel visibility rather than simply scaling everything up.
- Reflow layout before shrinking text or controls.
- Preserve action visibility and hierarchy at every breakpoint.
- Test common global cases: long text, small devices, tablets, laptops, and ultra-wide screens.

## Spacing and density
- Use a consistent spacing scale and apply it predictably.
- Default to comfortable density with room for scanning and touch interaction.
- Increase density only when task efficiency clearly benefits and readability remains strong.
- Keep spacing relationships intentional: related items close, unrelated items clearly separated.

## Typography
- Use typography to express hierarchy, not decoration.
- Keep type scales simple, readable, and consistent across platforms.
- Prioritize legibility at small sizes and in localized layouts.
- Avoid overly light weights, cramped line heights, or excessive style variation.
- Support dynamic type or platform text scaling where available.

## Color
- Use a restrained palette with clear semantic roles.
- Brand color should support recognition, not overwhelm the interface.
- Semantic colors for success, warning, error, and info must be consistent across platforms.
- Maintain strong contrast in all themes and states.
- Never rely on color alone for meaning.

## Component rules
- Prefer a small, durable component set over many near-duplicates.
- Components must have consistent states, labels, spacing, and behavior across the product.
- Shared components should preserve the same role across platforms even if rendered with platform-native styling.
- Destructive, high-risk, and primary actions must be visually and behaviorally distinct.
- Empty states, confirmation patterns, and error messages should follow repeatable product rules.

## Navigation rules
- Navigation should make current location, available actions, and return paths obvious.
- Keep top-level navigation stable and limited.
- Use the navigation model users expect on each platform, but keep destination structure consistent.
- Avoid hidden navigation that users must guess.
- Do not change navigation style between adjacent flows without a strong reason.

## Form UX rules
- Minimize required input and ask only for what is needed now.
- Keep labels always understandable without relying on placeholder text.
- Validate early when helpful and after submission when necessary.
- Errors must explain what is wrong, where, and how to fix it.
- Use input types, keyboards, pickers, and autofill behaviors appropriate to the platform.
- Preserve entered data whenever safely possible.

## State design rules
- Every important screen and component must define loading, empty, error, success, offline, and permission states when relevant.
- States must preserve layout stability where possible.
- Loading should communicate progress without blocking unnecessarily.
- Empty states should explain what happened and what to do next.
- Error states should support recovery, not just failure reporting.

## Accessibility rules
- Accessibility is required, not optional polish.
- Support screen readers, keyboard access where applicable, visible focus states, sufficient contrast, and touch target minimums.
- Use semantic structure, meaningful labels, and predictable interaction order.
- Do not encode meaning with color, motion, or position alone.
- Respect reduced motion and platform accessibility settings.

## Globalization rules
- Design all flows for localization from the start.
- Support text expansion, local date/time/number formats, and culturally neutral layouts by default.
- Avoid copy or layout that depends on English length or Western-only assumptions.
- Use icons, imagery, and examples that can travel globally without confusion.
- When local market adaptation is needed, preserve the core product identity and behavior.

## Copy tone
- Clear, concise, human, and practical.
- Prefer direct language over jargon or hype.
- Make actions, consequences, and next steps explicit.
- Keep microcopy calm and helpful, especially in errors, empty states, and confirmations.

## Senior designer standard
- Every shipped screen should look intentional, coherent, and review-ready.
- The design should show disciplined hierarchy, polished spacing, strong state handling, and a clear product point of view.
- If a screen feels templated, trendy without purpose, or interchangeable with any generic AI app, it is below the bar.
- UI-heavy PRs should run a senior product designer review before final handoff.

## Final rule
- If a design choice improves one platform but weakens product clarity, trust, accessibility, or cross-platform coherence, redesign it until it satisfies both product quality and platform usability.
