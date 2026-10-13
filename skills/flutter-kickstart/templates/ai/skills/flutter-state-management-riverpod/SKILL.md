---
name: flutter-state-management
description: Riverpod state management conventions for {{app_name}}. Use when adding or changing a provider, a @riverpod controller (AsyncNotifier), its state, or any widget that watches one.
---

# State management: Riverpod

This project uses `flutter_riverpod` with `riverpod_generator`. Don't
introduce Bloc, Provider, `get_it` or `setState` for feature state. The
provider graph is the DI graph.

## Two kinds of providers

- **DI providers** (`lib/core/di/providers.dart`, `<feature>_providers.dart`):
  plain `Provider<T>` returning a contract (`Provider<OrdersRepository>`).
  They are the only place an implementation class is named.
- **Controllers** (`presentation/controllers/`): `@riverpod` classes,
  code-generated. Run
  `dart run build_runner build --delete-conflicting-outputs` after adding
  or changing one.

```dart
@riverpod
class OrdersController extends _$OrdersController {
  @override
  Future<OrdersState> build() => _load();

  Future<void> reload() async {
    state = const AsyncLoading();
    state = AsyncData(await _load());
  }

  Future<OrdersState> _load() async {
    final result = await ref.read(getOrdersProvider).call();
    return result.fold(OrdersFailed.new, OrdersLoaded.new);
  }
}
```

Loading is `AsyncLoading`. Expected failures are a state value
(`OrdersFailed(failure)`), not a thrown error. `AsyncError` only ever
means a bug.

## Widgets

- `ref.watch` in `build`, `ref.read(...notifier).method()` in callbacks.
  Never `ref.watch` inside a callback.
- `switch` over `AsyncValue` and the sealed state exhaustively.

## Tests

Every controller has a `ProviderContainer` test overriding its use-case
provider: initial (loading), one success path and one `AppFailure` path per
public method. See `flutter-testing`.
