---
name: codebase-understanding
description: Map an unfamiliar or large codebase before implementation, including domains, entrypoints, data flow, risky modules, validation commands, and optional graph readiness.
---

# Codebase Understanding

Use before medium or large work in a repo that is unfamiliar, cross-layer, or hard to navigate.

## Workflow

1. Read the repository instructions and README.
2. Identify package manifests, app entrypoints, routing, data access, tests, and deployment files.
3. Map domain boundaries and platform layers.
4. List the smallest files likely affected by the task.
5. Identify risk hotspots: auth, billing, secrets, data migrations, admin actions, privacy, and deployment.
6. Decide whether normal search is enough or an optional knowledge graph would help.
7. Return a map that another agent can use without repeating broad exploration.

## Rules

- Inspect the repo before asking questions.
- Prefer local source truth over generated summaries.
- Do not require external graph tools for small tasks.
- Treat committed graph artifacts as advisory.
- Do not expose secrets or private data in maps.

## Output

Return:

- repo shape
- key entrypoints
- domain map
- affected files
- validation commands
- risks and unknowns
- optional graph recommendation
