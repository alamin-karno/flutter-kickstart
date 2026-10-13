---
title: Networking and errors
description: The AppApiClient contract, viva_network_kit or plain Dio, typed AppFailure errors and Either results in a Flutter Kickstart app.
---

# Networking and errors

## One contract

Every network call goes through `AppApiClient`, defined in
`lib/core/network/app_api_client.dart`:

```dart
abstract interface class AppApiClient {
  Future<Either<AppFailure, T>> get<T>(String path, {...});
  Future<Either<AppFailure, List<T>>> getList<T>(String path, {...});
  Future<Either<AppFailure, T>> post<T>(String path, {...});
  Future<Either<AppFailure, T>> put<T>(String path, {...});
  Future<Either<AppFailure, T>> patch<T>(String path, {...});
  Future<Either<AppFailure, T>> delete<T>(String path, {...});
}
```

Features only see this interface. The implementation is picked in the
interview:

| Choice | Class | Notes |
| --- | --- | --- |
| `--network viva` | `VivaApiClient` | Built on viva_network_kit; checks connectivity before each call |
| `--network dio` | `DioApiClient` | Plain Dio; no extra package |

Both share `dio_factory.dart`, the auth and logging interceptors,
`AppFailureConverter` and the `JsonSerializer`.

## Decoding JSON

Each model the client decodes gets one parser registration in `lib/core/di/`:

```dart
serializer.addParser<OrderModel>(OrderModel.fromJson);
```

`add_feature.py` adds this line for you.

## Errors are values

Nothing throws across layers. Data sources and repositories return
`Either<AppFailure, T>` (from `dartz`). `AppFailure` is a sealed class:

| Failure | When |
| --- | --- |
| `NetworkFailure` | No connection, timeout |
| `ServerFailure` | The server answered with an error status |
| `UnauthorizedFailure` | 401 / expired session |
| `ParsingFailure` | The response didn't match the model |
| `UnknownFailure` | Anything else |

`AppFailureConverter` is the one place that turns Dio errors into an
`AppFailure`. In the UI, `FailureView` shows a failure with a retry button.

```dart
final result = await getOrders();
result.fold(
  (failure) => emit(OrdersFailed(failure)),
  (orders) => emit(OrdersLoaded(orders)),
);
```

## Tests

`AppApiClient` contract tests run against whichever client you picked, using a
fake HTTP adapter. That way both implementations are held to the same
behaviour.
