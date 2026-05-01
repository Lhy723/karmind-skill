#!/usr/bin/env bash
set -euo pipefail

REPO="${KARMIND_REPO:-Lhy723/karmind-skill}"
REF="${KARMIND_REF:-main}"
AGENT="${KARMIND_AGENT:-}"
FORCE="${KARMIND_FORCE:-0}"
SOURCE_DIR="${KARMIND_SOURCE_DIR:-}"
KARMIND_TMP=""

RUNTIME_SCRIPTS=(
  ingest_cache.py
  init_wiki.py
  mirror_assets.py
  model_batch_ingest.py
  smoke_test.py
  wiki_doctor.py
)

log() {
  printf '%s\n' "$*"
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing required command: $1"
}

read_tty() {
  local prompt="$1"
  local answer=""
  if [ -r /dev/tty ]; then
    printf '%s' "$prompt" >/dev/tty
    IFS= read -r answer </dev/tty || true
  fi
  printf '%s' "$answer"
}

normalize_agent() {
  case "$1" in
    ""|"1"|"codex"|"generic"|"agents") printf 'codex' ;;
    "2"|"opencode") printf 'opencode' ;;
    "3"|"trae") printf 'trae' ;;
    "4"|"claude"|"claude-code") printf 'claude' ;;
    "5"|"all") printf 'all' ;;
    *) die "unknown KARMIND_AGENT: $1" ;;
  esac
}

select_agent() {
  if [ -n "$AGENT" ]; then
    normalize_agent "$AGENT"
    return
  fi

  if [ -r /dev/tty ]; then
    cat >/dev/tty <<'EOF'
Install karmind-skill for:
  1) Codex / generic agents (.agents/skills)
  2) OpenCode (.opencode/skills)
  3) Trae (.trae/rules + .trae/skills)
  4) Claude Code manual fallback (.claude/skills)
  5) All project-level locations
Choose [1]:
EOF
    local choice
    choice="$(read_tty "> ")"
    normalize_agent "${choice:-1}"
    return
  fi

  normalize_agent codex
}

prepare_source() {
  if [ -n "$SOURCE_DIR" ]; then
    [ -f "$SOURCE_DIR/SKILL.md" ] || die "KARMIND_SOURCE_DIR does not look like the repository root: $SOURCE_DIR"
    printf '%s' "$SOURCE_DIR"
    return
  fi

  need_cmd curl
  need_cmd tar
  local tmp
  tmp="$(mktemp -d)"
  KARMIND_TMP="$tmp"
  trap 'rm -rf "$KARMIND_TMP"' EXIT
  curl -fsSL "https://github.com/${REPO}/archive/refs/heads/${REF}.tar.gz" | tar -xz -C "$tmp"
  local root
  root="$(find "$tmp" -maxdepth 1 -type d -name 'karmind-skill-*' | head -n 1)"
  [ -n "$root" ] || die "failed to unpack karmind-skill"
  printf '%s' "$root"
}

replace_dir() {
  local dst="$1"
  if [ -e "$dst" ]; then
    if [ "$FORCE" = "1" ]; then
      rm -rf "$dst"
      return
    fi
    local answer
    answer="$(read_tty "$dst already exists. Replace it? [y/N] ")"
    case "$answer" in
      y|Y|yes|YES) rm -rf "$dst" ;;
      *) die "aborted; set KARMIND_FORCE=1 to replace without prompting" ;;
    esac
  fi
}

copy_runtime_skill() {
  local root="$1"
  local dst="$2"
  local include_agents="${3:-0}"

  replace_dir "$dst"
  mkdir -p "$dst/scripts"
  cp "$root/SKILL.md" "$dst/SKILL.md"
  cp -R "$root/references" "$dst/references"
  for name in "${RUNTIME_SCRIPTS[@]}"; do
    cp "$root/scripts/$name" "$dst/scripts/$name"
  done
  if [ "$include_agents" = "1" ]; then
    cp -R "$root/agents" "$dst/agents"
  fi
  log "installed skill: $dst"
}

install_codex() {
  copy_runtime_skill "$1" ".agents/skills/karmind-skill" 1
}

install_opencode() {
  copy_runtime_skill "$1" ".opencode/skills/karmind-skill" 0
}

install_claude() {
  copy_runtime_skill "$1" ".claude/skills/karmind-skill" 0
}

install_trae() {
  local root="$1"
  copy_runtime_skill "$root" ".trae/skills/karmind-skill" 0
  mkdir -p ".trae/rules"
  cp "$root/adapters/trae_project_rules.md" ".trae/rules/project_rules.md"
  log "installed Trae project rules: .trae/rules/project_rules.md"
}

main() {
  local agent root
  agent="$(select_agent)"
  root="$(prepare_source)"

  case "$agent" in
    codex) install_codex "$root" ;;
    opencode) install_opencode "$root" ;;
    trae) install_trae "$root" ;;
    claude) install_claude "$root" ;;
    all)
      install_codex "$root"
      install_opencode "$root"
      install_trae "$root"
      install_claude "$root"
      ;;
    *) die "unknown agent: $agent" ;;
  esac

  log "done. Open your agent in this project and ask it to use karmind-skill."
}

main "$@"
