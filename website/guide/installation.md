---
title: Installation
description: Install Flutter Kickstart with one command on macOS, Linux or Windows, as a Claude Code plugin, or from a git clone.
---

# Installation

## Requirements

- **Flutter**, or [fvm](https://fvm.app)
- **Python 3.8 or newer** (`python3`)
- **git**
- Network access for `flutter pub get`
- For iOS builds: macOS and Xcode

[Very Good CLI](https://cli.vgv.dev) is installed for you the first time you
create an app.

## One line (recommended)

::: code-group

```bash [macOS / Linux]
curl -fsSL https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/main/install.sh | bash
```

```powershell [Windows (PowerShell)]
irm https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/main/install.ps1 | iex
```

:::

This will:

1. Clone the latest release into `~/.flutter-kickstart`.
2. Add the `fks` and `flutter-kickstart` commands to `~/.local/bin`. It tells you if that folder is not on your `PATH`.
3. Link the skills into every AI agent's global skills folder.

Then check your setup:

```bash
fks doctor
```

::: tip Installs come from releases only
The installer always uses the `main` branch, which only holds released
versions. Work in progress lives on `dev` and never reaches your machine
by accident.
:::

### Options

| Variable | Default | Use it to |
| --- | --- | --- |
| `FLUTTER_KICKSTART_HOME` | `~/.flutter-kickstart` | Install somewhere else |
| `FLUTTER_KICKSTART_BIN` | `~/.local/bin` | Put the commands in another folder |
| `FLUTTER_KICKSTART_BRANCH` | `main` | Install a release tag such as `v1.0.0`, or try an unreleased branch (for contributors) |

### Install a specific version

Every [release](https://github.com/alamin-karno/flutter-kickstart/releases)
has a `vX.Y.Z` tag. Point the installer at a tag to get exactly that version:

::: code-group

```bash [macOS / Linux]
curl -fsSL https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/v1.0.0/install.sh | FLUTTER_KICKSTART_BRANCH=v1.0.0 bash
```

```powershell [Windows (PowerShell)]
$env:FLUTTER_KICKSTART_BRANCH = "v1.0.0"; irm https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/v1.0.0/install.ps1 | iex
```

:::

Each release page lists these commands for its own version and attaches
`install.sh` and `install.ps1`. Run `fks --version` to see what you have.

## Claude Code plugin

```text
/plugin marketplace add alamin-karno/flutter-kickstart
/plugin install flutter-kickstart@flutter-kickstart
```

Start a new Claude Code session after installing.

## From a clone

Use this if you want to change the templates, or your agent ignores symlinks.

```bash
git clone https://github.com/alamin-karno/flutter-kickstart.git ~/flutter-kickstart
~/flutter-kickstart/install.sh               # symlinks; `fks update` keeps them current
~/flutter-kickstart/install.sh --copy        # real copies, for agents that ignore symlinks
~/flutter-kickstart/install.sh --skills-only # skills only, no `fks` command
```

## Where the skills go

| Agent | Global skills folder |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/`, `~/.agents/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |
| Antigravity | `~/.gemini/config/skills/`, `~/.gemini/antigravity/skills/` |
| Codex | `~/.codex/skills/`, `~/.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/`, `~/.agents/skills/` |

If your agent does not support skills, tell it:
*"Read `~/.flutter-kickstart/skills/flutter-kickstart/SKILL.md` and follow it."*

::: warning Restart your agent
Agents load skills when a session starts. Open a **new** session after
installing or updating.
:::

## Update

```bash
fks update
```

## Uninstall

```bash
fks uninstall
```

This removes the commands and the linked skills. Delete
`~/.flutter-kickstart` too if you want everything gone.
