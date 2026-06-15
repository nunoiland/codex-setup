# Service Agent Routing Matrix

Use this matrix to choose the right Agent Army team for a product service type and lifecycle phase.

## Service types

| Service type | Use when | Extra reviewers |
| --- | --- | --- |
| `web_saas` | Standard web-first SaaS product | senior_product_designer, security_reviewer |
| `subscription_credit_saas` | SaaS with subscriptions, credits, billing, or usage limits | payment_auth_specialist, pricing_revenue_strategist, compliance_risk_reviewer |
| `marketplace` | Multi-sided product with sellers, buyers, listings, payouts, or trust workflows | business_model_strategist, compliance_risk_reviewer, customer_success_reviewer |
| `mobile_app` | Android/iOS app or app-extension product | android_builder, ios_builder, app_store_optimizer |
| `ai_agent_service` | AI workflow, assistant, automation, or agent product | ai_integration_engineer, security_reviewer, observability_specialist |
| `data_dashboard` | Analytics, reporting, metrics, BI, or admin dashboard product | data_model_specialist, database_optimizer, observability_specialist |
| `finance_sensitive` | Financial data, investment-adjacent, billing-sensitive, or regulated copy | compliance_risk_reviewer, security_reviewer, copy_quality_reviewer |
| `consumer_content_app` | Content, creator, social, media, or consumer engagement product | brand_guardian, growth_marketer, app_store_optimizer |

## Lifecycle phases

| Phase | Primary emphasis | Must review before exit |
| --- | --- | --- |
| `discovery` | problem, ICP, market, competitor, constraints | product_manager, business_analyst |
| `prd` | requirements, success criteria, scope, risks | prd_orchestrator, qa_reviewer |
| `ux` | flows, IA, visual direction, empty/error states | senior_product_designer, copy_quality_reviewer |
| `architecture` | system design, boundaries, data, auth/payment/deployment risk | solution_architect, security_reviewer |
| `implementation` | focused product build with the assigned platform builder | qa_reviewer, security_reviewer |
| `qa` | test strategy, evidence, failure loops, regressions | verification_loop_specialist |
| `release` | deployment readiness, observability, rollback, support | release_specialist, security_reviewer |
| `growth` | acquisition, pricing, retention, copy, funnel quality | growth_marketer, pricing_revenue_strategist |

## Routing examples

```bash
python3 -m codex_runtime --recommend-agents --service-type web_saas --phase discovery --pretty
python3 -m codex_runtime --recommend-agents --service-type subscription_credit_saas --phase architecture --pretty
python3 -m codex_runtime --recommend-agents --service-type mobile_app --phase qa --pretty
python3 -m codex_runtime --recommend-agents --service-type finance_sensitive --phase release --pretty
```

## Exit rule

Do not advance from one phase to the next until:

- primary agent output is reflected in the PRD or plan
- reviewer findings are resolved or explicitly accepted as risks
- validation gates for the phase are run or marked unavailable with a reason
