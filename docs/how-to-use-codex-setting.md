# API-key-free Product Template Guide

This is the default operating path for repositories generated from `codex_set`. It does not use `OPENAI_API_KEY`.

## The simple model

- PR means Pull Request. It is a request to merge one branch into the main branch after review.
- GitHub Actions means GitHub runs commands for the PR, such as tests and validation.
- Harness means the scripts collect failure evidence, logs, and a short report so local Codex can fix the right thing.
- Local Codex means the Codex app or CLI on your computer. This is where AI implementation, review, and fixing happen.

## Who does what

Local Codex does:

- implement code changes
- review and explain failures
- fix PR failures after you give it logs or artifacts
- update the branch and PR

GitHub Actions does:

- run `./scripts/validate.sh`
- run `git diff --check`
- run the local web health smoke check when the starter exists
- run `./scripts/browser-qa.sh`
- run `./scripts/harness-dry-run.sh`
- upload evidence artifacts
- merge only when the PR has the `automerge-approved` label and required checks pass

GitHub Actions does not:

- call OpenAI
- run `openai/codex-action`
- automatically write AI code
- require `OPENAI_API_KEY`

## Daily workflow

0. For a new product or meaningful feature, start with `/goal`.

Use the shape in [`product-factory-goal-contract.md`](./product-factory-goal-contract.md), then convert it into a PRD and plan before implementation.

If the goal creates a new service, also apply the service basecamp contracts:

- [`service-basecamp-architecture.md`](./service-basecamp-architecture.md)
- [`service-template-contract.md`](./service-template-contract.md)
- [`vps-deployment-contract.md`](./vps-deployment-contract.md)
- [`revenue-system-contract.md`](./revenue-system-contract.md)
- [`admin-observability-contract.md`](./admin-observability-contract.md)

If the goal touches UI, also apply the senior design layer:

- [`design-reference-library.md`](./design-reference-library.md)
- [`design-system-contract.md`](./design-system-contract.md)
- [`senior-designer-review-checklist.md`](./senior-designer-review-checklist.md)
- [`visual-qa-contract.md`](./visual-qa-contract.md)

Before writing the PRD or implementation plan, ask the local runtime which Agent Army team fits the service and phase:

```bash
python3 -m codex_runtime --recommend-agents --service-type web_saas --phase discovery --pretty
```

Use the returned primary agents for the current work and reviewer agents before handoff.

1. Start a branch locally.

```bash
git checkout -b codex/my-task
```

2. Ask local Codex to implement the task.

Give Codex the PRD or task and say what outcome you want. Keep secrets out of the prompt unless they are already available through a safe local secret mechanism.

3. Validate locally.

```bash
./scripts/validate.sh
./scripts/ci-pr-check.sh
```

4. Push the branch and open a PR.

```bash
git push -u origin codex/my-task
gh pr create --draft
```

5. Wait for GitHub Actions.

Open the PR checks. The required phase-1 check is `pr-validate`.

6. If the PR fails, open the uploaded artifact.

Look for:

- `harness-summary.md`
- `harness-evidence.json`
- `logs/validate.log`
- `logs/whitespace.log`
- `logs/browser-qa.log`

Then ask local Codex:

```text
이 PR의 GitHub Actions 실패를 고쳐줘.
API 키 없이 동작해야 하고, artifact의 harness-summary.md와 실패 로그 기준으로 수정해줘.
수정 후 ./scripts/ci-pr-check.sh도 실행해줘.
```

7. Push the fix.

```bash
git push
```

8. Merge.

When the PR is ready:

- all required checks must pass
- a human adds the `automerge-approved` label
- the automerge workflow performs a squash merge

## Browser QA

This template includes a starter web app, but browser QA still stays opt-in. If no explicit browser QA target or command is configured, `./scripts/browser-qa.sh` writes skip evidence and exits successfully.

For a product repository with a web target, configure one of these:

```bash
CODEX_WEB_QA_URL=http://127.0.0.1:3000
```

or:

```bash
CODEX_WEB_QA_COMMAND="npm run test:e2e"
```

Use the command form for Playwright tests or browser automation wrappers.

## Nightly harness

The nightly workflow runs the same API-key-free check path and uploads an evidence artifact. It is for finding repeated failures and setup gaps, not for writing code automatically.

The next morning, read the report and choose only the improvements that are worth doing.

## Product Factory readiness

Use this command to check whether the optional Product Factory layer is ready:

```bash
python3 -m codex_runtime --operator-readiness --pretty
```

The default state is ready with local Codex app plus JSON memory. Paperclip, Hermes, Graphiti, Neo4j, Docker, and provider keys stay optional and should appear as warnings or risks only when you explicitly enable those modes.

## Required repository settings

For safe automerge, configure branch protection or repository rules for the default branch:

- require the `pr-validate` check
- require PR review if your project needs it
- do not allow direct pushes to protected branches

The workflow also checks for the `automerge-approved` label and only merges same-repository branches.

## Phase-2 boundary

`openai/codex-action` is intentionally not enabled in phase 1. If you later decide to allow API-key-based AI review or AI fixes inside GitHub Actions, use [`future-codex-action.md`](./future-codex-action.md).
