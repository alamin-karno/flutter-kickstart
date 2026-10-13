---
name: flutter-error-handling
description: Error-handling conventions for {{app_name}}: the AppFailure hierarchy, Either-returning data sources and repositories, crash reporting and logging. Use when writing anything that can fail, mapping errors, showing an error to the user, or reporting/logging errors.
---

# Error handling

No raw exception crosses from `data/` into `domain/` or `presentation/`.

## AppFailure

`lib/core/network/app_failure.dart` defines a sealed hierarchy:
`NetworkFailure`, `ServerFailure(statusCode)`, `UnauthorizedFailure`,
`ParsingFailure`, `UnknownFailure`. Add a subtype there when none fits;
don't throw a custom exception instead.

## Conversion happens in exactly two places

1. `AppFailureConverter` (`lib/core/network/app_failure_converter.dart`)
   is plugged into `viva_network_kit`, so every `AppApiClient` call already
   returns `Either<AppFailure, T>`: offline -> `NetworkFailure`, 401 ->
   `UnauthorizedFailure`, other HTTP errors -> `ServerFailure`.
   `VivaApiClient` also turns decoding `TypeError`s (missing
   `addParser`, changed JSON) into `ParsingFailure`.
2. A data source doing non-HTTP work (cache, platform channel) wraps that
   work in its own `try/catch` and returns `Left(...)`.

```dart
// Wrong
Future<Profile> getProfile() async {
  final res = await dio.get('/profile');
  if (res.statusCode != 200) throw Exception('failed');
  return Profile.fromJson(res.data);
}

// Right (data source)
Future<Either<AppFailure, ProfileModel>> fetchProfile() =>
    _client.get<ProfileModel>('/profile');
```

## Presentation

State holders turn `Left` into a failure state carrying the `AppFailure`.
Widgets render `FailureView(failure: ..., onRetry: ...)` from
`lib/core/widgets/`. Never show `toString()` of an exception.

## Logging and crash reporting

- `AppLogger` (`lib/core/logging/`) for diagnostics, never `print`.
- `CrashReporter` (`lib/core/error_reporting/`, backed by {{crash_label}})
  for unexpected errors. `bootstrap.dart` already routes
  `FlutterError.onError` and `PlatformDispatcher.onError` to it.
- Never log tokens, passwords or personal data.
