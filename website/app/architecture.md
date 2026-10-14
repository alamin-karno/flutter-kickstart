---
title: Architecture
description: The feature-first clean architecture of a Flutter Kickstart app, its folder layout, the dependency rule and the non-negotiable conventions.
---

# Architecture

Generated apps use **feature-first clean architecture**. Shared contracts
live in `lib/core/`. Each feature has its own domain, data and presentation
layers.

## Folder layout

```text
lib/
  app/                 App widget (MaterialApp.router, theme, l10n)
  bootstrap.dart       startup shared by every lib/main_<flavor>.dart
  core/
    config/            AppFlavor, AppConfig (base URL, DSNs via --dart-define)
    di/                dependency injection (get_it modules or Riverpod providers)
    error_reporting/   CrashReporter + adapter
    logging/           AppLogger
    network/           AppApiClient + implementation, AppFailure, converter, JsonSerializer, interceptors
    routing/           AppRoutes + buildAppRouter (go_router)
    theming/           AppTheme, AppColors, AppSpacing, AppRadius, context extensions
    widgets/           shared widgets (FailureView)
  features/<name>/
    domain/            entities, repository contracts, use cases (pure Dart)
    data/              models (JSON), remote data sources, repository implementations
    presentation/      screens + Cubits or Riverpod controllers
    <name>.dart        barrel: exports only the screen
```

## The dependency rule

```text
presentation  ->  domain  <-  data
```

- `domain/` imports nothing from `data/`, `presentation/` or Flutter. It is plain Dart.
- `data/` implements the repository contracts from `domain/`.
- `presentation/` talks to use cases, never to data sources.
- **Features never import other features.** Anything shared moves to `core/`.

## The rules

These are written into the app's `AGENTS.md`, so people and AI agents follow
the same list.

1. **Network only through `AppApiClient`.** Never import Dio or viva_network_kit outside `lib/core/network/`.
2. **Errors are values.** Data sources and repositories return `Either<AppFailure, T>`. Nothing throws across layers.
3. **State uses sealed classes**, in a Cubit or a Riverpod controller.
4. **Navigation** uses `context.push(AppRoutes.x)` or `context.go(...)`. Never `Navigator.push` or a raw path string.
5. **Theme tokens only**: `context.colors`, `context.appColors`, `context.textTheme`, `AppSpacing`, `AppRadius`. No `Color(0x...)`, no bare padding numbers.
6. **User-visible text** comes from `context.l10n.<key>`, with keys in `lib/l10n/arb/app_en.arb`.
7. **Log** through `AppLogger`, and report unexpected errors through `CrashReporter`. No `print`.
8. **Secrets and base URLs** never go in source. Use `--dart-define` or CI secrets.
9. **Every change ships with tests**, and `./scripts/quality_gate.sh` passes before the change is done.

## Theme tokens

```dart
Padding(
  padding: const EdgeInsets.all(AppSpacing.md), // 16
  child: Text(
    context.l10n.homeTitle,
    style: context.textTheme.titleLarge,
  ),
)
```

| Token | Values |
| --- | --- |
| `AppSpacing` | `xs` 4, `sm` 8, `md` 16, `lg` 24, `xl` 32 |
| `AppRadius` | `sm` 4, `md` 8, `lg` 16 |
| `AppColors` | Brand colours as a `ThemeExtension`, with `light` and `dark` |
