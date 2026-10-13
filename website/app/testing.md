---
title: Testing and quality gate
description: The tests every Flutter Kickstart app ships with, the coverage floor, and the quality gate script that CI runs on every pull request.
---

# Testing and quality gate

## Tests from day one

A freshly generated app has roughly **95% line coverage**:

| Kind | Covers |
| --- | --- |
| Unit | Entities, models, use cases, repositories, data sources, failures, logger, config |
| DI | Every registration (Bloc modules) or provider (Riverpod) |
| State | Every Cubit (`bloc_test`) or Riverpod controller |
| Widget | Every screen, through `tester.pumpApp` |
| Contract | `AppApiClient` behaviour, run against your chosen client |

`test/` mirrors `lib/`, so each file's test is easy to find. Shared helpers
live in `test/helpers/` (`pumpApp`, test config, a fake HTTP adapter, DI setup).

## The quality gate

```bash
./scripts/quality_gate.sh
```

It runs exactly what CI runs:

1. `dart format --set-exit-if-changed lib test`
2. `flutter analyze`
3. `flutter test --coverage --test-randomize-ordering-seed random`

It uses fvm if the project has a `.fvmrc`.

## Coverage floor

You set the minimum coverage in the interview (`--coverage-floor`, default
80). The `pr_checks` workflow fails any pull request below it. Generated code,
l10n output and flavor entrypoints don't count toward it.

The generator checks the floor too. If a freshly generated app is below it,
generation fails, so you always start above the bar.

## "Done" means

`dart format .`, `flutter analyze` and `flutter test` all pass, and the change
follows the [architecture rules](/app/architecture#the-rules). The same
definition is in `AGENTS.md`, so AI agents use it too.
