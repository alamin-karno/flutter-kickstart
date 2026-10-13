---
name: flutter-testing
description: Testing conventions and the mandatory done-check for {{app_name}}. Use after writing or changing any Dart code, when adding tests for a repository, use case, Cubit/controller, widget or screen, when tests fail, or when coverage drops.
---

# Testing

New code ships with its tests in the same change. `test/` mirrors `lib/`.

| Change | Required test |
| --- | --- |
| Repository / use case | Unit test with the data source or repository mocked |
| {{state_test_row}} |
| Screen or shared widget | Widget test using `tester.pumpApp(...)` from `test/helpers/` |
| Critical user flow (login, checkout) | `integration_test/` smoke test |

## Mocking: mocktail

```dart
class _MockOrdersRemote extends Mock implements OrdersRemoteDataSource {}

when(() => remote.fetchOrders())
    .thenAnswer((_) async => const Right([OrderModel(id: '1', title: 'A')]));
```

No `mockito` or generated mocks.

## Goldens

For shared components and key screens, add `alchemist` golden tests
(`flutter pub add dev:alchemist`). Run with `--update-goldens` only when
the visual change is intended.

## Done-check (mandatory)

```bash
./scripts/quality_gate.sh     # dart format check, analyze, tests + coverage
```

Fix whatever it reports. "Looks done" is not done. {{coverage_enforcement}}
