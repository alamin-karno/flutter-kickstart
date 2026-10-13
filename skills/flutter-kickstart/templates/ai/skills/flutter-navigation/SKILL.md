---
name: flutter-navigation
description: Navigation conventions for {{app_name}}: go_router only, path constants in AppRoutes, redirects for guards. Use when adding a screen or route, navigating, passing route parameters, handling deep links, or gating routes behind auth/onboarding.
---

# Navigation

`lib/core/routing/app_router.dart` owns `AppRoutes` (path constants) and
`buildAppRouter()`. `add_feature.py` registers new feature routes at the
`// scaffold:*` markers; keep those markers.

## Rules

```dart
// Wrong
Navigator.push(context, MaterialPageRoute(builder: (_) => const OrdersScreen()));
context.push('/orders');

// Right
context.push(AppRoutes.orders);
```

- Every screen gets an `AppRoutes` constant and a `GoRoute` before
  anything links to it.
- `context.push` / `context.go` / `context.pop` only. No `Navigator.*`.
- Path parameters: declare `/orders/:id`, read `state.pathParameters['id']`
  once in the `GoRoute` builder, and pass a typed value to the screen
  constructor. Don't put required data in `extra`; it is lost on deep
  links and web refresh.
- Auth or onboarding gating is a `redirect` on `GoRouter` or the route,
  not a widget that conditionally renders one screen or another.
