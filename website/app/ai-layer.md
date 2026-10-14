---
title: AI layer
description: AGENTS.md, project skills, Cursor and Windsurf rules, Copilot instructions and reviewer subagents that keep every AI coding agent on your app's conventions.
---

# AI layer

Every generated app teaches AI agents how it works. Claude Code, Cursor,
Windsurf, Antigravity, Codex, Gemini CLI and GitHub Copilot all read the same
rules, so the conventions hold no matter who, or what, writes the code.

## The files

```text
AGENTS.md                      the rules (Cursor, Windsurf, Antigravity, Codex, Copilot read it natively)
CLAUDE.md, GEMINI.md           one line each: @AGENTS.md
.agents/skills/<skill>/        the project skills
.claude/skills   -> .agents/skills
.cursor/skills   -> .agents/skills
.windsurf/skills -> .agents/skills
.cursor/rules/flutter-architecture.mdc     rule for lib/**/*.dart
.windsurf/rules/flutter-architecture.md    rule for lib/**/*.dart
.github/copilot-instructions.md
.claude/agents/architecture-reviewer.md
.claude/agents/test-reviewer.md
tool/kickstart/add_feature.py  the feature generator, vendored
```

**Edit only `AGENTS.md` and `.agents/skills/`.** Everything else points to
them, so every tool sees your change.

## Project skills

| Skill | Use when |
| --- | --- |
| `flutter-feature-architecture` | Adding a feature, screen, repository or use case; deciding where a file goes |
| `flutter-state-management` | Writing Bloc or Riverpod code (matches your choice) |
| `flutter-error-handling` | Anything that can fail |
| `flutter-navigation` | Adding a route or navigating |
| `flutter-theming` | Any styling; implementing a design |
| `flutter-testing` | Writing tests; the done-check after any change |
| `flutter-deployment` | CI/CD and releases (only with `--ci github`) |
| `flutter-architecture-review` | Reviewing a diff against the rules |
| `flutter-test-review` | Checking a diff has the tests it needs |
| `flutter-figma-to-flutter` | Implementing a Figma frame |

## Choosing agents

`--agents all` (the default) sets up every tool. To set up only some:

```bash
--agents claude,cursor,windsurf
```

Valid names: `claude`, `cursor`, `windsurf`, `antigravity`, `codex`,
`gemini`, `copilot`.

On Windows, or with `--copy-skills`, the skill mirrors are real copies
instead of symlinks.

## Refresh the layer

To add or update the AI files in an app Flutter Kickstart created earlier:

```bash
python3 ~/.flutter-kickstart/skills/flutter-kickstart/scripts/setup_ai.py --root path/to/app
```

It detects state management, network client and CI from the project.
