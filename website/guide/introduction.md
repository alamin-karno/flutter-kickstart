---
title: Introduction
description: What Flutter Kickstart is, who it is for, and how the setup questions, the generator and the AI-agent skills fit together.
---

# Introduction

Flutter Kickstart turns *"start a new Flutter app"* into a few quick questions
and gives you a codebase that is ready for real work.

Most Flutter projects begin the same way. You set up flavors, pick an
architecture, wire dependency injection, write a network layer, add routing,
theming and localization, then set up tests and CI. That takes days, and every
project ends up slightly different. Flutter Kickstart does all of it in a few
minutes, the same way every time.

## What it is

Flutter Kickstart has three parts:

| Part | What it does |
| --- | --- |
| **The `fks` command** | A small CLI. `fks create` asks the questions, `fks run` starts a flavor, `fks add-feature` grows the app. |
| **The generator** (`scaffold.py`) | Builds the project from templates. Same answers in, same project out. |
| **Agent skills** | Let Claude Code, Cursor, Windsurf, Antigravity, Codex, Gemini CLI or Copilot ask the setup questions for you in plain words. |

You can use any one of them. They all end up running the same generator.

## Who it is for

- **Teams** who want every new app to start with the same structure and rules.
- **Freelancers and agencies** who start many client apps and want a solid base each time.
- **Developers using AI agents** who want the agent to follow fixed conventions instead of guessing.

## What makes it different

**It checks its own work.** The generator runs `flutter analyze` and
`flutter test` at the end and checks the coverage floor. You only see
"success" when the app really builds and passes its tests.

**It asks instead of assuming.** State management (Bloc or Riverpod) and the
network client (viva_network_kit or plain Dio) are always asked, because
the right answer depends on the project.

**It keeps your AI agent on track.** The generated app includes an
`AGENTS.md` and project skills, so your agent knows where files go, how errors
work and what "done" means. Read more in [AI layer](/app/ai-layer).

## Next steps

- [Install it](/guide/installation)
- [Create your first app](/guide/quick-start)
- [See what you get](/app/overview)
