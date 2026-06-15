# Template Bootstrap

Use this repository as a GitHub template for new products, then personalize only the product-facing identity.

## What changes

The bootstrap script updates:

- product slug
- display name
- optional package name
- optional repo name

It updates template placeholders in product-facing starter files only. It does not:

- create or rename GitHub repositories
- push commits
- change secrets or environment values
- enable auth, billing, or deployment integrations

## Usage

```bash
python3 scripts/bootstrap-template.py --slug sample-product --name "Sample Product" --dry-run
python3 scripts/bootstrap-template.py --slug sample-product --name "Sample Product"
```

Optional:

```bash
python3 scripts/bootstrap-template.py \
  --slug sample-product \
  --name "Sample Product" \
  --package-name sample-product-app \
  --repo-name sample-product
```

## Defaults

- `package-name` defaults to the slug.
- `repo-name` defaults to the slug.
- dry-run prints the planned file updates and leaves tracked files untouched.

## After bootstrap

1. Run `pnpm install`
2. Run `./scripts/validate.sh`
3. Run `./scripts/ci-pr-check.sh`
4. Update PRD, landing copy, and starter placeholders with product-specific details
