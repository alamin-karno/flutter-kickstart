---
name: flutter-state-management
description: Bloc/Cubit state management conventions for {{app_name}}. Use when adding or changing a Cubit or Bloc, its states or events, a BlocProvider/BlocBuilder/BlocListener, or a widget that reads them.
---

# State management: Bloc / Cubit

This project uses `flutter_bloc`. Don't introduce Riverpod, Provider,
`ChangeNotifier` or `setState` for feature state.

## Cubit by default, Bloc when events matter

Use a `Cubit` with methods (`load()`, `submit()`). Switch to a `Bloc` only
when you need event transformers (debounce, droppable). Bloc event names
are past-tense facts: `OrdersRefreshRequested`, never `LoadOrders`.

## States are a sealed hierarchy

```dart
sealed class OrdersState { const OrdersState(); }
final class OrdersInitial extends OrdersState { const OrdersInitial(); }
final class OrdersLoading extends OrdersState { const OrdersLoading(); }
final class OrdersLoaded extends OrdersState {
  const OrdersLoaded(this.items);
  final List<Order> items;
}
final class OrdersFailed extends OrdersState {
  const OrdersFailed(this.failure);
  final AppFailure failure;
}
```

Widgets `switch` over the state exhaustively. No boolean flags
(`isLoading`) standing in for states, no `is` chains.

```dart
Future<void> load() async {
  emit(const OrdersLoading());
  final result = await _getOrders();
  emit(result.fold(OrdersFailed.new, OrdersLoaded.new));
}
```

## Wiring

- Cubits take use cases through the constructor and are registered in
  the feature's `<feature>_module.dart` (`@injectable`). Run
  `dart run build_runner build --delete-conflicting-outputs` after
  changing a module.
- Create them at the screen: `BlocProvider(create: (_) => getIt<OrdersCubit>()..load())`.
  Split the screen into `OrdersScreen` (provides) and `OrdersView`
  (renders) so the view can be tested with a mock cubit.
- Only DI code, the router and screen-level `BlocProvider.create` call
  `getIt`.

## Tests

Every Cubit/Bloc has a `bloc_test` suite: initial state, one success path,
one `AppFailure` path per public method or event. See `flutter-testing`.
