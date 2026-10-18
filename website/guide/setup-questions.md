---
title: Setup questions
description: The few setup questions Flutter Kickstart asks, the flag and default for each, and what each choice changes in the generated Flutter app.
---

# Setup questions

A handful of questions is all Flutter Kickstart needs. Most have a default, so
you can press **Enter** to accept it. Each answer maps to one generator flag,
so you can also skip the questions and pass flags (see
[Generator flags](/reference/flags)).

Agents ask one question at a time, skip questions an earlier answer makes
pointless, and read everything back before generating.

## The questions

| # | Question | Flag | Default |
| - | --- | --- | --- |
| 1 | App display name and description | `--app-name`, `--description` | from `--name` |
| 2 | Package name | `--name` | snake_case of the display name |
| 3 | Organization / reverse domain | `--org` | required |
| 4 | Platforms | `--platforms` | `android,ios` |
| 5 | State management: Bloc or Riverpod | `--state bloc\|riverpod` | none, always asked |
| 6 | Network client: viva_network_kit or plain Dio | `--network viva\|dio` | `viva`, always asked |
| 7 | Navigation: go_router, auto_route or Navigator | `--router go_router\|auto_route\|navigator` | `go_router`, always asked |
| 8 | API base URL per flavor | `--base-url flavor=url` (repeat) | `https://<flavor>.api.example.com` |
| 9 | Starter features beyond home | `--features auth,orders` | none |
| 10 | Languages besides English | `--locales en,bn` | `en` |
| 11 | Crash reporting: none, Sentry or Crashlytics | `--crash` | `none` |
| 12 | CI/CD: GitHub Actions + Fastlane, or none | `--ci github\|none` | `github` |
| 13 | Minimum test coverage, in percent | `--coverage-floor` | `80` |
| 14 | Figma file link | `--figma-url` | none |
| 15 | AI tools the team uses | `--agents` | `all` |

## What the choices change

### State management

**Bloc** gives you Cubits with `get_it` + `injectable` for dependency
injection. **Riverpod** gives you `riverpod_generator` controllers and a
provider graph. Both are asked every time, because the right one depends on
the team and the client. See [State management](/app/state-management).

### Network client

Feature code only ever depends on the `AppApiClient` contract. This choice
swaps one class in `lib/core/network/`:

- **viva** uses `viva_network_kit` (`VivaApiClient`). It also checks connectivity before each call.
- **dio** uses plain Dio (`DioApiClient`) and doesn't add the package at all.

Both share `dio_factory.dart`, `AppFailureConverter` and the same
`JsonSerializer` API, so features, repositories and the feature generator are
identical either way. See [Networking and errors](/app/networking).

### Navigation

**go_router** is the default, but you pick: **auto_route** for typed,
generated routes, or **Navigator** for Flutter's built-in named routes with
no package. The choice swaps `lib/core/routing/app_router.dart`, the app
widget and the `flutter-navigation` skill. `AppRoutes` constants and
`add_feature.py` work the same with all three. See [Navigation](/app/navigation).

### Languages

Each extra locale gets `lib/l10n/arb/app_<locale>.arb`, filled with the
English strings until someone translates them. The iOS locale list is updated
too. New features add their strings to every ARB file.

### Crash reporting

`none` logs to the console through `ConsoleCrashReporter`. `sentry` and
`crashlytics` add the SDK, an adapter behind the `CrashReporter` contract, and
raise Android `minSdk` if the SDK needs it.

### CI/CD

`github` generates the workflows, Fastlane and `docs/deployment-setup.md`.
`none` generates no workflows (Very Good CLI's own are removed too) and leaves
the deployment skill out of the AI layer. `scripts/quality_gate.sh` is
always generated. See [CI/CD and releases](/app/ci-cd).

### Coverage floor

CI enforces it on every pull request. The generator also fails if a freshly
generated app falls below it, so you start above the bar.

### Flavors

`development`, `staging` and `production` are fully wired, including native
Android and iOS setup. Custom flavors (`--flavors`) only get Dart entrypoints,
and the generator warns about the native parts left to do.
