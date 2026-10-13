---
title: Changing the templates
description: How Flutter Kickstart's templates, variants and generator scripts are organized, and how to verify a template change.
---

# Changing the templates

## Repository layout

```text
.claude-plugin/{plugin,marketplace}.json   Claude Code plugin + marketplace
bin/flutter-kickstart                      the fks CLI
install.sh, install.ps1                    one-line installers
skills/
  flutter-kickstart/
    SKILL.md                               setup questions + how to run the generator
    scripts/scaffold.py                    full project generator
    scripts/add_feature.py                 feature generator (also copied into apps)
    scripts/setup_ai.py                    cross-agent AI layer installer
    templates/lib, test                    core + app shell (Dart)
    templates/feature/{common,bloc,riverpod,home}
    templates/project                      always generated: quality gate, Figma token map
    templates/ci/github                    GitHub Actions, Fastlane, deployment docs
    templates/ai                           AGENTS.md, rules, project skills, subagents
  flutter-figma-to-flutter/SKILL.md        design-to-code skill
website/                                   this docs site (VitePress)
```

## Variant templates

A template named `x.<choice>.dart.tmpl` is generated only for that choice
(`bloc`, `riverpod`, `viva`, `dio`), and loses the `.<choice>` part:

```text
dio_api_client.dio.dart.tmpl      ->  lib/core/network/dio_api_client.dart   (only with --network dio)
injector.bloc.dart.tmpl           ->  lib/core/di/injector.dart              (only with --state bloc)
```

Placeholders use `{{name}}`. In file and folder names, `__feature__` and
`__entity__` are replaced by the feature and entity names.

## Verify a change

Generate both sides of every choice and make sure both pass. The generator
runs analyze, the tests and the coverage floor for you:

```bash
cd /tmp
python3 <repo>/skills/flutter-kickstart/scripts/scaffold.py \
  --name demo_bloc --org com.acme --state bloc --network viva \
  --ci github --locales en,bn --features orders --crash sentry

python3 <repo>/skills/flutter-kickstart/scripts/scaffold.py \
  --name demo_rp --org com.acme --state riverpod --network dio \
  --ci none --features orders --crash crashlytics
```

Then add a feature to each to check `add_feature.py`:

```bash
cd demo_bloc && python3 tool/kickstart/add_feature.py --name invoices
```

## Before you open the PR

- Mention both generation runs in the PR description.
- Update the docs in `website/` if flags, output or behaviour changed.
- Add a line under `Unreleased` in `CHANGELOG.md`.
- Don't bump the version; that happens on the release branch.
