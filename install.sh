#!/usr/bin/env bash
# Installs this plugin's skills globally for every supported AI agent.
#
#   ./install.sh            symlink (updates arrive with `git pull`)
#   ./install.sh --copy     copy instead (for agents that ignore symlinks)
#   ./install.sh --uninstall
#
# Claude Code users can instead install it as a plugin:
#   /plugin marketplace add <this repo URL or path>
#   /plugin install flutter-kickstart@flutter-kickstart
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
MODE="link"
case "${1:-}" in
  --copy) MODE="copy" ;;
  --uninstall) MODE="uninstall" ;;
  "") ;;
  *) echo "usage: $0 [--copy|--uninstall]" >&2; exit 2 ;;
esac

# Global skill folders, one per agent. Add yours and open a PR.
AGENT_DIRS=(
  "$HOME/.claude/skills"                # Claude Code
  "$HOME/.agents/skills"                # shared location: Codex, Cursor, Gemini CLI, Devin/Windsurf
  "$HOME/.codex/skills"                 # OpenAI Codex CLI
  "$HOME/.cursor/skills"                # Cursor
  "$HOME/.codeium/windsurf/skills"      # Windsurf (Cascade)
  "$HOME/.gemini/config/skills"         # Antigravity 2.x (all products)
  "$HOME/.gemini/antigravity/skills"    # Antigravity IDE
  "$HOME/.gemini/skills"                # Gemini CLI
)

for skill in "$REPO"/skills/*/; do
  skill="${skill%/}"
  name="$(basename "$skill")"
  for dir in "${AGENT_DIRS[@]}"; do
    target="$dir/$name"
    if [[ "$MODE" == "uninstall" ]]; then
      if [[ -L "$target" ]]; then rm "$target"; echo "unlink $target"
      elif [[ -d "$target" && -f "$target/.installed-by-flutter-kickstart" ]]; then rm -rf "$target"; echo "remove $target"
      fi
      continue
    fi
    mkdir -p "$dir"
    if [[ -e "$target" && ! -L "$target" && ! -f "$target/.installed-by-flutter-kickstart" ]]; then
      echo "skip   $target exists and was not installed by this script"
      continue
    fi
    rm -rf "$target"
    if [[ "$MODE" == "copy" ]]; then
      cp -R "$skill" "$target"
      touch "$target/.installed-by-flutter-kickstart"
      echo "copy   $target"
    else
      ln -s "$skill" "$target"
      echo "link   $target -> $skill"
    fi
  done
done

[[ "$MODE" == "uninstall" ]] || echo "Done. Start a NEW agent session so it picks up the skills."
