---
title: FAQ
description: Answers to common questions about Flutter Kickstart, its supported agents, existing apps, Bloc vs Riverpod, pricing and updates.
---

# FAQ

## Is it free?

Yes. Flutter Kickstart is open source under the
[MIT license](https://github.com/alamin-karno/flutter-kickstart/blob/main/LICENSE).

## Do I need an AI agent to use it?

No. `fks create` runs the same interview in your terminal. The agent skills
are an extra way in.

## Which AI agents are supported?

Claude Code, Cursor, Windsurf, Antigravity, Codex, Gemini CLI and GitHub
Copilot. Other agents can read the skill file directly. See
[Using it with AI agents](/guide/ai-agents#agents-without-skill-support).

## Can I use it on an existing app?

Not to regenerate it. The generator is for new apps, and agents won't run it
over an app Flutter Kickstart didn't create. For an app it did create, you can
add features (`fks add-feature`) and refresh the AI layer (`setup_ai.py`).

## Bloc or Riverpod: which should I pick?

Pick the one your team knows. Both give you the same architecture, sealed
states, DI and tests. See [State management](/app/state-management).

## What is viva_network_kit?

A networking package built on Dio that also checks connectivity before each
call. If you'd rather not depend on it, choose `--network dio`. Feature code is
the same either way.

## Which platforms can the app target?

Android and iOS by default. Web, macOS and Windows can be added with
`--platforms`.

## Does it lock me in?

No. The output is a normal Flutter project. Nothing in it needs Flutter
Kickstart to build or run. Even the feature generator is copied into the app
(`tool/kickstart/add_feature.py`).

## How do I get updates?

Run `fks update`. You only get released versions; see
[Branches and releases](/contributing/git-flow).

## How do I suggest a feature or report a bug?

[Open an issue](https://github.com/alamin-karno/flutter-kickstart/issues/new/choose).
Pull requests are welcome too; read [How to contribute](/contributing/) first.
