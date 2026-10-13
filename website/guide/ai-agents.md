---
title: Using it with AI agents
description: Create and grow Flutter apps by asking Claude Code, Cursor, Windsurf, Antigravity, Codex, Gemini CLI or GitHub Copilot in plain words.
---

# Using it with AI agents

After you [install](/guide/installation), every supported agent has two
skills:

| Skill | What it does |
| --- | --- |
| `flutter-kickstart` | Runs the interview, generates the app, adds features, sets up the AI layer |
| `flutter-figma-to-flutter` | Turns a Figma frame into widgets that use the app's theme tokens and widgets |

<ul class="fk-chips">
  <li>Claude Code</li><li>Cursor</li><li>Windsurf</li><li>Antigravity</li>
  <li>Codex</li><li>Gemini CLI</li><li>GitHub Copilot</li>
</ul>

## Things you can ask

- *"Create a new Flutter app called Acme Wallet for com.acme."*
- *"Add an orders feature that loads `/v1/orders`."* (inside a generated app)
- *"Implement this Figma frame: &lt;link&gt;"* (needs a Figma MCP server)
- *"Set up the AI rules for this app."* (for an app Flutter Kickstart created earlier)

## What the agent does

1. Asks the [interview](/guide/interview) questions one at a time.
2. Reads your answers back and waits for a yes.
3. Runs the same generator as `fks create`.
4. Tells you what was created, and what still needs a human (secrets, signing, translations).

Because the agent runs a script instead of writing the project by hand, every
agent produces the same app.

## Which path the agent picks

| Situation | What happens |
| --- | --- |
| New app | Interview, then the generator |
| Add a feature to an app Flutter Kickstart created | `tool/kickstart/add_feature.py` inside the app |
| App was created before, AI files missing or old | `setup_ai.py --root <app>` refreshes them |
| App **not** created by Flutter Kickstart | The agent does not run the generator over it. It follows that app's own conventions. |

## Agents without skill support

Point the agent at the skill file directly:

> Read `~/.flutter-kickstart/skills/flutter-kickstart/SKILL.md` and follow it.

## After the app exists

The generated app carries its own `AGENTS.md` and project skills, so your
agent keeps following the rules without the global skill. See
[AI layer](/app/ai-layer).
