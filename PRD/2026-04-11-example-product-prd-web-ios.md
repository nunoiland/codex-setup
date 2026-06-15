# Example Product PRD: Web Plus iOS Launch Sprint

## Goal

Create an initial web plus iOS product slice for a waitlist-driven AI study planner, with enough code, documentation, and handoff detail that a human can review the branch the next morning and decide whether to continue toward launch.

## Scope

- In scope:
  - Generate or update the web experience and iOS experience from one product PRD.
  - Deliver work through GitHub using a branch and draft PR handoff.
  - Produce a morning report that includes implementation status, validation status, QA checklist, and marketing plus revenue draft ideas.
- In scope:
  - Keep secrets external and document any missing credentials as blockers.

## Non-goals

- Out of scope:
  - Automatic production deployment.
  - Automatic domain, DNS, App Store, or backend infrastructure cutover.

## Context

The product owner wants to test a lightweight planning product quickly. The repository should support a single PRD that targets both web and iOS, routes each platform to the right builder, and reports partial success if one platform completes while the other fails.

## Constraints

- Technical constraints:
  - Keep GitHub as the system of record and avoid direct pushes to protected branches.
  - Do not store provider keys, GitHub credentials, or reporting-channel secrets in the repository.
- Product constraints:
  - The first overnight run can ship drafts and scaffolding, but the morning handoff must be explicit about what is incomplete.
- Time or release constraints:
  - The run is intended to complete overnight and be ready for human QA in the morning.

## Acceptance criteria

1. The PRD is explicit enough for Codex to route web work and iOS work from the same request.
2. The run produces GitHub branch output and a draft PR rather than an unreviewed protected-branch push.
3. The morning handoff includes engineering status plus draft positioning, pricing, and launch-channel suggestions.

## Edge cases

- Web succeeds while iOS fails.
- Required secrets are missing or invalid.
- GitHub delivery succeeds but local handoff reporting fails.

## Platform target

- web+ios

## Delivery mode

- existing repository + branch + draft PR
- no direct push to protected branches without explicit approval

## Reporting mode

- github_only

## Secret profile

- Required secret: GitHub credential with repo write and PR scope
- Source of injection: external secret store or environment injection
- Owner or approver: repository owner
- Required secret: LLM provider key if the target workflow needs one
- Source of injection: external secret store or environment injection
- Owner or approver: operator

## Human handoff

- QA checks: verify onboarding, key screens, navigation, and any generated tests or build outputs
- Manual release or infra tasks: production env setup, domain or backend configuration, store signing, release approval
- Final approver: human operator

## Validation commands

```bash
pnpm lint
pnpm test
xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 16' build
```

## Done when

- The work is delivered to GitHub through a reviewable branch and draft PR.
- The morning handoff clearly states what succeeded, what failed, and what needs human follow-up.
- The run does not commit secrets or claim automatic deployment.
