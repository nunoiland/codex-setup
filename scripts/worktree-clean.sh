#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: ./scripts/worktree-clean.sh <worktree-path> [--merged-into <ref>] [--delete-branch] [--force]

Examples:
  ./scripts/worktree-clean.sh ../codex-setting-worktree-hardening-web --merged-into codex/worktree-hardening
  ./scripts/worktree-clean.sh ../codex-setting-worktree-hardening-review --merged-into origin/main --delete-branch
USAGE
}

if [ "$#" -lt 1 ]; then
  usage >&2
  exit 1
fi

worktree_path=""
merged_into=""
delete_branch=0
force=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --delete-branch)
      delete_branch=1
      shift
      ;;
    --force)
      force=1
      shift
      ;;
    --merged-into)
      if [ "$#" -lt 2 ]; then
        echo "--merged-into requires a ref" >&2
        exit 1
      fi
      merged_into="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [ -z "$worktree_path" ]; then
        worktree_path="$1"
        shift
      else
        echo "unexpected argument: $1" >&2
        exit 1
      fi
      ;;
  esac
done

if [ -z "$worktree_path" ]; then
  usage >&2
  exit 1
fi

repo_root="$(git rev-parse --show-toplevel)"
resolved_path="$(cd "$(dirname "$worktree_path")" && pwd)/$(basename "$worktree_path")"

if ! git -C "$resolved_path" rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "not a git worktree: $resolved_path" >&2
  exit 1
fi

branch_name="$(git -C "$resolved_path" branch --show-current)"
base_branch="${CODEX_DEFAULT_BASE_BRANCH:-main}"
merge_target="$merged_into"
if [ -z "$merge_target" ]; then
  merge_target="$base_branch"
  if git -C "$repo_root" rev-parse --verify --quiet "origin/$base_branch" >/dev/null; then
    merge_target="origin/$base_branch"
  fi
fi

if [ -z "$branch_name" ]; then
  echo "could not determine branch for $resolved_path" >&2
  exit 1
fi

if ! git -C "$repo_root" rev-parse --verify --quiet "$merge_target" >/dev/null; then
  echo "merge target not found: $merge_target" >&2
  exit 1
fi

case "$branch_name" in
  main|master|"$base_branch")
    if [ "$force" -ne 1 ]; then
      echo "refusing to clean a protected branch worktree without --force: $branch_name" >&2
      exit 1
    fi
    ;;
esac

if [ -n "$(git -C "$resolved_path" status --short)" ] && [ "$force" -ne 1 ]; then
  echo "worktree has uncommitted changes; use --force to override: $resolved_path" >&2
  exit 1
fi

if ! git -C "$repo_root" merge-base --is-ancestor "$branch_name" "$merge_target" >/dev/null 2>&1 && [ "$force" -ne 1 ]; then
  echo "branch is not merged into $merge_target; use --force to override: $branch_name" >&2
  exit 1
fi

if [ "$force" -eq 1 ]; then
  git -C "$repo_root" worktree remove --force "$resolved_path"
else
  git -C "$repo_root" worktree remove "$resolved_path"
fi

if [ "$delete_branch" -eq 1 ]; then
  if [ "$force" -eq 1 ]; then
    git -C "$repo_root" branch -D "$branch_name"
  else
    git -C "$repo_root" branch -D "$branch_name"
  fi
fi

echo "removed_worktree=$resolved_path"
echo "branch_name=$branch_name"
echo "merged_into=$merge_target"
