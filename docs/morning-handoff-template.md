# Morning Handoff Template


## Delivery rules

- Always produce the handoff in GitHub-friendly form first.
- Treat all business outputs as drafts for human review.
- Treat all self-improvement proposals as drafts for human review.

## Handoff sections

### 1. Run summary

- Run name:
- Source PRD:
- Platform target:
- Delivery mode:
- Reporting mode:
- Start time:
- End time:
- Overall status: success | partial-success | blocked | failed

### 2. GitHub artifacts

- Repository:
- Base branch:
- Working branch:
- Commit range or head SHA:
- Draft PR link:

### 3. Platform status

For each platform in scope:

- Web: success | partial | failed
- iOS: success | partial | failed
- Android: success | partial | failed
- API/backend: success | partial | failed

Include one or two lines for each platform:
- what was completed
- what is blocked or missing

### 4. Validation results

- Commands run:
- Passed:
- Failed:
- Not run and why:

### 5. Product state

- core goal
- target user
- problem solved
- current stage
- top blockers
- top next actions

### 6. QA checklist

- primary flows to test
- high-risk screens or modules
- platform-specific checks
- anything generated but not fully verified

### 7. Manual follow-up

- infra or server setup
- domain or DNS work
- App Store / Play Store / signing work
- release approvals still needed

### 8. Risks, blockers, and lessons learned

- unresolved bugs
- delivery problems
- platform gaps
- assumptions that need confirmation
- reusable lessons from the run

### 9. Product and business drafts

For each section below, provide multiple ranked options rather than a single paragraph.

#### Positioning draft
- recommendation
- 2 to 3 positioning options
- rationale, tradeoffs, and next actions per option

#### Growth draft
- recommendation
- 2 to 3 acquisition or activation experiments
- rationale, tradeoffs, and next actions per option

#### Revenue draft
- recommendation
- 2 to 3 monetization or pricing options
- rationale, tradeoffs, and next actions per option

#### Launch draft
- recommendation
- 2 to 3 launch sequencing options
- rationale, tradeoffs, and next actions per option

#### Ops draft
- recommendation
- top operator actions for today
- memory, QA, and approval reminders

### 10. Self-improvement proposals

- proposed skill updates
- checklist improvements
- prompt or guardrail refinements
- each item must be explicitly marked as draft-only and human-reviewed


When reporting to a local handoff artifact, keep it short:

1. overall status
2. PR link
3. platform summary
4. top blocker
5. top 3 human actions

Example shape:

```text
Overnight run: partial-success
PR: <link>
Platforms: web ✅ iOS ⚠️ android not in scope
Top blocker: missing signing credential for iOS archive
Today: QA onboarding, set env secrets, choose one pricing test
```
