#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PLACEHOLDERS = {
    "__TEMPLATE_PRODUCT_SLUG__": "slug",
    "__TEMPLATE_PRODUCT_NAME__": "name",
    "__TEMPLATE_PACKAGE_NAME__": "package_name",
    "__TEMPLATE_REPO_NAME__": "repo_name",
}

TARGET_FILES = [
    Path("package.json"),
    Path("src/config/product.ts"),
]

README_START = "<!-- TEMPLATE_IDENTITY:START -->"
README_END = "<!-- TEMPLATE_IDENTITY:END -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Personalize the codex_set product template.")
    parser.add_argument("--slug", required=True, help="Product slug, e.g. sample-product")
    parser.add_argument("--name", required=True, help="Display name, e.g. Sample Product")
    parser.add_argument("--package-name", help="Optional package.json name override")
    parser.add_argument("--repo-name", help="Optional repository name override")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files")
    return parser.parse_args()


def validate_slug(value: str, field_name: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise SystemExit(f"{field_name} must use lowercase kebab-case: {value}")
    return value


def identity_block(name: str, repo_name: str) -> str:
    return "\n".join(
        [
            README_START,
            f"# {name}",
            "",
            f"A product repository generated from the `codex_set` template for `{repo_name}`.",
            "",
            "> This repo keeps the full local Codex operating stack, validation, harness, and Product Factory contracts.",
            README_END,
        ]
    )


def render_replacements(values: dict[str, str]) -> list[dict[str, object]]:
    changed: list[dict[str, object]] = []

    for path in TARGET_FILES:
        original = path.read_text(encoding="utf-8")
        updated = original
        for placeholder, key in PLACEHOLDERS.items():
            updated = updated.replace(placeholder, values[key])
        if path.name == "package.json":
            package_payload = json.loads(updated)
            package_payload["name"] = values["package_name"]
            updated = json.dumps(package_payload, indent=2, ensure_ascii=False) + "\n"
        if updated != original:
            changed.append({"path": str(path), "before": original, "after": updated})

    readme_path = Path("README.md")
    readme_original = readme_path.read_text(encoding="utf-8")
    if README_START in readme_original and README_END in readme_original:
        pattern = re.compile(
            re.escape(README_START) + r".*?" + re.escape(README_END),
            re.DOTALL,
        )
        updated = pattern.sub(identity_block(values["name"], values["repo_name"]), readme_original, count=1)
        if updated != readme_original:
            changed.append({"path": str(readme_path), "before": readme_original, "after": updated})

    return changed


def main() -> None:
    args = parse_args()
    values = {
        "slug": validate_slug(args.slug.strip(), "slug"),
        "name": args.name.strip(),
        "package_name": validate_slug((args.package_name or args.slug).strip(), "package-name"),
        "repo_name": validate_slug((args.repo_name or args.slug).strip(), "repo-name"),
    }
    if not values["name"]:
        raise SystemExit("name must not be empty")

    changed = render_replacements(values)
    summary = {
        "dry_run": args.dry_run,
        "values": values,
        "files": [{"path": item["path"]} for item in changed],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if args.dry_run:
        return

    for item in changed:
        Path(item["path"]).write_text(item["after"], encoding="utf-8")


if __name__ == "__main__":
    main()
