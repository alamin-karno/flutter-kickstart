---
title: Adding features
description: Add a clean-architecture feature with domain, data and presentation layers, DI, a route, l10n strings and tests in one command.
---

# Adding features

A feature is a folder in `lib/features/<name>/` with its own domain, data and
presentation layers. Add one with:

```bash
fks add-feature orders --endpoint /v1/orders
```

or, without the CLI, from inside the app:

```bash
python3 tool/kickstart/add_feature.py --name orders --endpoint /v1/orders
```

The script lives inside every generated app, so it works on any machine,
even without Flutter Kickstart installed.

## What you get

```text
lib/features/orders/
  domain/
    entities/order.dart
    repositories/orders_repository.dart
    usecases/get_orders.dart
  data/
    models/order_model.dart
    datasources/orders_remote_data_source.dart
    repositories/orders_repository_impl.dart
  presentation/
    screens/orders_screen.dart
    cubit/ or controllers/          (Bloc or Riverpod)
  orders_module.dart / orders_providers.dart   DI wiring
  orders.dart                                  barrel: exports the screen
test/features/orders/...                       tests for every layer
```

It also:

- registers the model's JSON parser and the feature's DI,
- adds an `AppRoutes.orders` constant (`/orders`) and a `GoRoute`,
- adds the screen title string (`ordersTitle`) to **every** ARB file,
- runs `flutter analyze` and `flutter test`.

## Options

| Flag | What it does | Default |
| --- | --- | --- |
| `--name` | Feature name | required |
| `--entity` | Entity name | singular of `--name` |
| `--endpoint` | GET path for the list | `/<name>` |
| `--state` | `bloc` or `riverpod` | detected from `pubspec.yaml` |
| `--force` | Overwrite existing feature files | off |
| `--dry-run` | Print the plan only | off |
| `--no-verify` | Skip analyze and test | off |

## Next steps

The generated feature loads a list from the endpoint and shows it. Replace the
entity fields, the model and the screen with your real ones, keep the tests
passing, and run `./scripts/quality_gate.sh`.
