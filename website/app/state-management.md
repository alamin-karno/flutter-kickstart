---
title: State management
description: Bloc/Cubit with get_it and injectable, or Riverpod with riverpod_generator. How each option is wired in a Flutter Kickstart app.
---

# State management

You choose **Bloc** or **Riverpod** in the setup questions. There is no default,
because the right answer depends on your team and your client. Everything else
in the app (domain, data, network, routing, theme) stays the same.

## Side by side

| | Bloc | Riverpod |
| --- | --- | --- |
| Flag | `--state bloc` | `--state riverpod` |
| State holder | Cubit | `riverpod_generator` controller |
| Dependency injection | `get_it` + `injectable` modules | the provider graph |
| DI file in a feature | `<name>_module.dart` | `<name>_providers.dart` |
| Presentation folder | `presentation/cubit/` | `presentation/controllers/` |
| State type | sealed class | sealed class |
| App-wide DI | `lib/core/di/injector.dart`, `register_module.dart` | `lib/core/di/providers.dart` |

## Sealed state

Both options model screen state as a sealed class, so the UI handles every
case and the compiler tells you when one is missing:

```dart
sealed class OrdersState {}
final class OrdersLoading extends OrdersState {}
final class OrdersLoaded extends OrdersState { OrdersLoaded(this.orders); final List<Order> orders; }
final class OrdersFailed extends OrdersState { OrdersFailed(this.failure); final AppFailure failure; }
```

## After changing DI or providers

Both options use code generation. Run:

```bash
dart run build_runner build --delete-conflicting-outputs
```

## Tests

- **Bloc**: `bloc_test` for every Cubit, and a module test that checks the feature's DI registrations.
- **Riverpod**: controller tests with a `ProviderContainer`, and a providers test for the feature graph.
