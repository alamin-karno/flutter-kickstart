---
title: What you get
description: Everything a Flutter Kickstart app includes out of the box, from flavors and clean architecture to tests, CI/CD and the AI-agent layer.
---

# What you get

Every app Flutter Kickstart creates has the same foundation. Here is what is
in the box.

| Area | Generated |
| --- | --- |
| **Base** | Very Good CLI app: native development/staging/production flavors, `very_good_analysis` lints, l10n in English plus any extra languages |
| **Architecture** | `lib/core/` contracts + `lib/features/<name>/{domain,data,presentation}` |
| **State** | Bloc/Cubit (`get_it` + `injectable`) or Riverpod (`riverpod_generator`) |
| **Network** | `AppApiClient` contract on viva_network_kit or plain Dio, sealed `AppFailure`, `Either` everywhere, auth and logging interceptors |
| **Shell** | `go_router` with `AppRoutes`, Material 3 light/dark theme with `AppColors`, `AppSpacing`, `AppRadius`, `AppLogger`, `CrashReporter` (console, Sentry or Crashlytics), per-flavor `AppConfig` with `--dart-define` overrides |
| **Features** | `home`, plus any starter features, each with every layer, DI, a route, l10n and tests |
| **Tests** | Unit, DI, bloc/controller and widget tests (about 95% line coverage), `AppApiClient` contract tests, `scripts/quality_gate.sh` |
| **CI/CD** | Optional: GitHub Actions for PR checks, Android and iOS builds and store uploads, Fastlane, symbol upload, a setup guide |
| **AI layer** | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, 10 project skills, Cursor and Windsurf rules, Copilot instructions, Claude reviewer subagents, and a vendored feature generator |

## The project at a glance

```text
my_app/
  lib/
    app/                    App widget (MaterialApp.router, theme, l10n)
    bootstrap.dart          startup shared by every flavor
    main_development.dart   one entrypoint per flavor
    main_staging.dart
    main_production.dart
    core/                   contracts and their single implementation
    features/               one folder per feature
    l10n/arb/               app_en.arb (+ one per extra language)
  test/                     mirrors lib/
  scripts/quality_gate.sh   the checks CI runs
  tool/kickstart/           add_feature.py, so the app can grow on its own
  .github/workflows/        pr_checks, android, ios (with --ci github)
  AGENTS.md                 rules every AI agent reads
  figma-token-map.md        Figma variables -> theme tokens
```

## Read more

- [Architecture](/app/architecture)
- [State management](/app/state-management)
- [Networking and errors](/app/networking)
- [Flavors and config](/app/flavors)
- [Testing and quality gate](/app/testing)
- [CI/CD and releases](/app/ci-cd)
- [AI layer](/app/ai-layer)
