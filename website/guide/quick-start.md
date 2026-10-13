---
title: Quick start
description: Create, run and grow your first Flutter Kickstart app in a few minutes.
---

# Quick start

This page takes you from nothing to a running app. It assumes you have
[installed Flutter Kickstart](/guide/installation).

## 1. Create the app

```bash
fks create
```

Answer the questions. Press **Enter** to accept the default shown in
brackets. In a hurry? `fks create --yes` only asks for the name, organization
and state management, and uses defaults for everything else.

```text
? App display name? [My App] Acme Wallet
? Package name (snake_case)? [acme_wallet]
? Organization / reverse domain? [com.example] com.acme
? State management? bloc (Cubit + get_it) / riverpod (riverpod_generator) [bloc]
? Network client? viva (viva_network_kit) / dio (plain Dio) [viva] dio
...
? Generate it now? [Y]
```

The generator then:

1. Creates a Very Good CLI base with development, staging and production flavors.
2. Writes the core layer, the app shell, a `home` feature and any starter features.
3. Adds tests, the quality gate script, CI/CD (if chosen) and the AI layer.
4. Runs codegen, format, `flutter analyze` and `flutter test`.

It only says it succeeded when every step passes.

## 2. Run it

```bash
cd acme_wallet
fks run              # development flavor
fks run staging      # any other flavor
```

`fks run` is short for
`flutter run --flavor <flavor> -t lib/main_<flavor>.dart`, and uses fvm if the
project pins a Flutter version.

## 3. Add a feature

```bash
fks add-feature orders --endpoint /v1/orders
```

You get the domain, data and presentation layers, dependency injection, a
route, localized strings and tests. See [Adding features](/guide/adding-features).

## 4. Check before you push

```bash
./scripts/quality_gate.sh
```

This runs the same checks as CI: format, analyze, and tests with coverage.

## Prefer asking your agent?

With the skills installed, you can skip the CLI and say:

> Create a new Flutter app called Acme Wallet for com.acme.

The agent asks the same questions one at a time, reads your answers back,
and runs the generator. See [Using it with AI agents](/guide/ai-agents).

## What still needs you

The app runs right away, but a few things only you can provide:

- **Real API URLs**, if you used the placeholders.
- **Store signing and secrets** for CI/CD. See `docs/deployment-setup.md` in your app.
- **Translations** for extra languages (they start as English copies).
- **Crash reporting keys**: a Sentry DSN, or `flutterfire configure` for Crashlytics.
- **App icons and the splash screen.**
