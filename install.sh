#!/usr/bin/env bash
# Installs flutter-kickstart: the `fks` command (alias `flutter-kickstart`) plus the skills
# for every supported AI agent.
#
# One line, from anywhere (clones into ~/.flutter-kickstart):
#   curl -fsSL https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/main/install.sh | bash
#
# From a checkout:
#   ./install.sh               symlink (updates arrive with `fks update`)
#   ./install.sh --copy        copy instead (for agents that ignore symlinks)
#   ./install.sh --skills-only skip the command, only (re)link the skills
#   ./install.sh --uninstall
#
# Claude Code users can instead install it as a plugin:
#   /plugin marketplace add alamin-karno/flutter-kickstart
#   /plugin install flutter-kickstart@flutter-kickstart
set -euo pipefail

REPO_URL="${FLUTTER_KICKSTART_REPO:-https://github.com/alamin-karno/flutter-kickstart.git}"
INSTALL_DIR="${FLUTTER_KICKSTART_HOME:-$HOME/.flutter-kickstart}"
BIN_DIR="${FLUTTER_KICKSTART_BIN:-$HOME/.local/bin}"

# Piped through `curl | bash` (or run from outside a checkout): fetch the repo, then run its installer.
SELF="${BASH_SOURCE[0]:-}"
if [[ -z "$SELF" || ! -f "$SELF" || ! -d "$(dirname "$SELF")/skills/flutter-kickstart" ]]; then
  command -v git >/dev/null || { echo "error: git is required" >&2; exit 1; }
  if [[ -d "$INSTALL_DIR/.git" ]]; then
    echo "Updating $INSTALL_DIR"
    git -C "$INSTALL_DIR" pull --ff-only --quiet
  else
    echo "Cloning flutter-kickstart into $INSTALL_DIR"
    git clone --depth 1 --quiet "$REPO_URL" "$INSTALL_DIR"
  fi
  exec bash "$INSTALL_DIR/install.sh" "$@"
fi

REPO="$(cd "$(dirname "$SELF")" && pwd)"
MODE="link"
WITH_CLI=1
for arg in "$@"; do
  case "$arg" in
    --copy) MODE="copy" ;;
    --uninstall) MODE="uninstall" ;;
    --skills-only) WITH_CLI=0 ;;
    *) echo "usage: $0 [--copy] [--skills-only] [--uninstall]" >&2; exit 2 ;;
  esac
done

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

# `fks` is the short name; `flutter-kickstart` the long one. Both point at bin/flutter-kickstart.
CLI_NAMES=(fks flutter-kickstart)
if [[ "$MODE" == "uninstall" ]]; then
  for cli in "${CLI_NAMES[@]}"; do
    link="$BIN_DIR/$cli"
    if [[ -L "$link" && "$(readlink "$link")" == "$REPO/bin/flutter-kickstart" ]]; then rm "$link"; echo "unlink $link"; fi
  done
  [[ "$REPO" == "$INSTALL_DIR" ]] && echo "To delete the templates too: rm -rf $INSTALL_DIR"
  exit 0
fi

if [[ "$WITH_CLI" == 1 ]]; then
  chmod +x "$REPO/bin/flutter-kickstart"
  mkdir -p "$BIN_DIR"
  for cli in "${CLI_NAMES[@]}"; do
    link="$BIN_DIR/$cli"
    if [[ -e "$link" && ! -L "$link" ]]; then echo "skip   $link exists and was not installed by this script"; continue; fi
    ln -sf "$REPO/bin/flutter-kickstart" "$link"
    echo "link   $link -> $REPO/bin/flutter-kickstart"
  done
fi

command -v python3 >/dev/null || echo "warning: python3 not found; install Python 3.8+ before creating an app."
command -v flutter >/dev/null || command -v fvm >/dev/null || echo "warning: flutter not found; install Flutter (or fvm) before creating an app."

cat <<EOF

flutter-kickstart is installed. The command is \`fks\` (long name: flutter-kickstart).

  fks create              answer a few questions, get a verified app
  cd <app> && fks run     run it on the development flavor

Or ask your AI agent (start a NEW session first): "Create a new Flutter app called Acme Wallet for com.acme."
EOF

if [[ "$WITH_CLI" == 1 && ":$PATH:" != *":$BIN_DIR:"* ]]; then
  case "${SHELL:-}" in
    */zsh) rc="~/.zshrc" ;;
    */bash) rc="~/.bashrc" ;;
    *) rc="your shell profile" ;;
  esac
  cat <<EOF

$BIN_DIR is not on your PATH yet. Add it once:
  echo 'export PATH="$BIN_DIR:\$PATH"' >> $rc && source $rc
EOF
fi
