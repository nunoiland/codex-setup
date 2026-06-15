# Platform Routing Matrix

Use this matrix when a product PRD declares a `Platform target`.

## Goals

- map each platform target to the right builder slice
- make validation expectations explicit
- preserve partial progress when one platform succeeds and another fails

## Routing table

| Platform target | Primary builders | Typical validation shape | Handoff expectation |
| --- | --- | --- | --- |
| `web` | `web_builder` | frontend lint, test, typecheck, build | single-platform web status |
| `ios` | `ios_builder` | Xcode or Swift build/test commands | single-platform iOS status |
| `android` | `android_builder` | Gradle lint/test/build | single-platform Android status |
| `api` | `api_builder` | backend lint/test/type or service checks | API-only status |
| `web+ios` | `web_builder`, `ios_builder` | web checks + iOS checks | per-platform success or partial-success |
| `web+android` | `web_builder`, `android_builder` | web checks + Android checks | per-platform success or partial-success |
| `ios+android` | `ios_builder`, `android_builder` | iOS checks + Android checks | per-platform success or partial-success |
| `web+ios+android` | `web_builder`, `ios_builder`, `android_builder` | checks by platform plus any shared contract checks | detailed multi-platform handoff |
| `multi-platform` | `prd_orchestrator` decides from PRD scope | validate every assigned slice | explicit routing summary required |

## Routing rules

- Keep one approved plan for the run unless there is explicit approval to split plans.
- Break work into the smallest platform-specific slices possible.
- Do not let one builder silently edit another platform’s files unless the plan explicitly assigns a shared contract boundary.
- If a platform target is ambiguous, stop in PRD intake and request clarification.

## Validation rules

- Validation commands should be grouped by platform in the PRD or plan whenever more than one platform is in scope.
- If one platform cannot validate because required tooling or secrets are unavailable, report that platform as blocked rather than hiding it.
- Shared backend or API checks should be listed separately from web or mobile checks.

## Partial-success policy

If a multi-platform run has mixed results:

- preserve the successful slices
- report failure or blockage per platform
- keep GitHub artifacts reviewable
- do not overstate overall success

Examples:
- web ✅ / iOS ⚠️ missing signing-related prerequisite
- web ✅ / Android ❌ build failure
- API ✅ / mobile not attempted because PRD was blocked before native work began

## Handoff requirements

Every multi-platform handoff should include:

- platform-by-platform status
- validations run per platform
- blockers per platform
- manual follow-up by platform

## Anti-patterns

- “multi-platform” PRD with one combined validation command and no platform breakdown
- direct protected-branch push after only one platform validates
- vague handoff such as “mobile failed” without identifying iOS vs Android
