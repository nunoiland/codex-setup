# Agent Army Operating Model

The Agent Army is the local Codex-native specialist layer for building many products from this template.

It does not install external agent frameworks. It uses rewritten local agents, existing skills, PRD-first workflow, and runtime routing to recommend the right team for each service and phase.

## Default flow

1. Start with a product goal or `/goal` request.
2. Turn it into a PRD and select service type plus current phase.
3. Run the routing command:

```bash
python3 -m codex_runtime --recommend-agents --service-type web_saas --phase discovery --pretty
```

4. Use the recommended primary agents for the work plan.
5. Use reviewer agents before handoff.
6. Run normal validation and GitHub evidence workflows.

## Agent roles

Agent categories:

- product and business: shape the problem, market, ICP, pricing, and business model
- design and UX: shape flow, research assumptions, visual quality, brand, and implementation fit
- engineering: architecture, backend reliability, database, AI integration, and platform execution support
- QA, security, release: test strategy, API checks, compliance risk, observability, and release readiness
- growth and revenue: acquisition, app store, sales, customer success, and monetization review

## Routing contract

The router returns:

- `primary_agents`: agents that should directly shape the current phase
- `reviewer_agents`: agents that should review before moving forward
- `optional_agents`: agents to add only if the PRD says the product needs them
- `validation_gates`: checks expected before the phase is considered ready
- `risks`: phase or service-specific risks to keep visible

## How to ask Codex

Use natural language plus the runtime output:

```text
Use the Agent Army recommendation for service_type=subscription_credit_saas phase=architecture.
Have solution_architect produce the architecture plan, payment_auth_specialist review auth/billing boundaries, and security_reviewer check secret and permission risks.
```

For UI-heavy work:

```text
Use ux_architect, senior_product_designer, frontend_ux_engineer, and copy_quality_reviewer to review this flow before implementation.
```

For release:

```text
Use release_specialist, devops_sre_specialist, observability_specialist, security_reviewer, and compliance_risk_reviewer for release readiness.
```

## Safety rules

- Agents are specialists, not permission bypasses.
- PRD-first and plan-first still apply.
- Ask before dependencies, auth, payment, secrets/env handling, deployment, or destructive git actions.
- External frameworks are reference-only unless a separate PRD approves installation.
- Strategy, pricing, legal, compliance, and growth outputs are drafts for human review.
- Never commit secrets or private provider credentials.

## Generated product repos

Generated product repos keep this layer in Full codex_set mode. The recommended first command in a new product is:

```bash
python3 -m codex_runtime --recommend-agents --service-type web_saas --phase discovery --pretty
```
