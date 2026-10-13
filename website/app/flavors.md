---
title: Flavors and config
description: Development, staging and production flavors, per-flavor AppConfig and --dart-define overrides in a Flutter Kickstart app.
---

# Flavors and config

## Three flavors, fully wired

| Flavor | Entrypoint | App name suffix |
| --- | --- | --- |
| `development` | `lib/main_development.dart` | `[DEV]` |
| `staging` | `lib/main_staging.dart` | `[STG]` |
| `production` | `lib/main_production.dart` | none |

Android product flavors and iOS schemes come from Very Good CLI, so the three
flavors can be installed side by side on one device.

```bash
fks run                 # development
fks run staging
flutter run --flavor production -t lib/main_production.dart
```

Custom flavors (`--flavors`) only get Dart entrypoints. The generator lists
the native steps you still need to do.

## AppConfig

`lib/core/config/app_config.dart` holds the per-flavor settings: flavor, app
name, API base URL, timeout and crash-reporting DSN. Each `main_<flavor>.dart`
builds one with `AppConfig.fromEnvironment(...)`.

The base URL you gave in the interview is the default for each flavor.
Override it at build time without touching code:

```bash
flutter run --flavor staging -t lib/main_staging.dart \
  --dart-define=API_BASE_URL=https://stg.api.acme.com \
  --dart-define=SENTRY_DSN=https://...
```

::: warning Keep secrets out of git
DSNs, keys and tokens belong in `--dart-define` values and CI secrets, never
in source files.
:::
