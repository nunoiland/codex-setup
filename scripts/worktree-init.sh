#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: ./scripts/worktree-init.sh <lane> <slug> [base-ref]

Examples:
  ./scripts/worktree-init.sh orchestrator worktree-hardening
  ./scripts/worktree-init.sh web worktree-hardening origin/main
USAGE
}

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  usage >&2
  exit 1
fi

lane="$1"
slug_raw="$2"
base_ref="${3:-origin/main}"
repo_root="$(git rev-parse --show-toplevel)"
repo_name="$(basename "$repo_root")"
parent_dir="$(cd "$repo_root/.." && pwd)"

slug="$(printf '%s' "$slug_raw" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g; s/-+/-/g')"
if [ -z "$slug" ]; then
  echo "slug must contain at least one alphanumeric character" >&2
  exit 1
fi

branch_name=""
path_suffix=""
case "$lane" in
  orchestrator)
    branch_name="codex/$slug"
    path_suffix="$slug"
    ;;
  review)
    branch_name="codex/${slug}-review"
    path_suffix="${slug}-review"
    ;;
  web|ios|android|api)
    branch_name="codex/${slug}-${lane}"
    path_suffix="${slug}-${lane}"
    ;;
  *)
    branch_name="codex/${slug}-${lane}"
    path_suffix="${slug}-${lane}"
    ;;
esac

worktree_path="$parent_dir/${repo_name}-${path_suffix}"

if [ -e "$worktree_path" ]; then
  echo "worktree path already exists: $worktree_path" >&2
  exit 1
fi

if git -C "$repo_root" show-ref --verify --quiet "refs/heads/$branch_name"; then
  echo "branch already exists locally: $branch_name" >&2
  exit 1
fi

if git -C "$repo_root" remote get-url origin >/dev/null 2>&1; then
  git -C "$repo_root" fetch origin --prune >/dev/null 2>&1 || true
  if git -C "$repo_root" show-ref --verify --quiet "refs/remotes/origin/$branch_name"; then
    echo "branch already exists on origin: $branch_name" >&2
    exit 1
  fi
fi

if ! git -C "$repo_root" rev-parse --verify --quiet "$base_ref" >/dev/null; then
  echo "base ref not found: $base_ref" >&2
  exit 1
fi

git -C "$repo_root" worktree add "$worktree_path" -b "$branch_name" "$base_ref"

echo "worktree_path=$worktree_path"
echo "branch_name=$branch_name"
echo "base_ref=$base_ref"
