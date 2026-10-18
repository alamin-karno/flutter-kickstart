---
name: flutter-navigation
description: Navigation conventions for {{app_name}}: Flutter's built-in Navigator with named routes from AppRoutes, one onGenerateAppRoute table. Use when adding a screen or route, navigating, passing route arguments, or gating screens behind auth/onboarding.
---

# Navigation (Navigator, named routes)

The app uses Flutter's built-in `Navigator`; there is no routing package.
`lib/core/routing/app_router.dart` owns `AppRoutes` (route names) and
`onGenerateAppRoute`, the single table mapping a name to its screen.
`add_feature.py` registers new feature routes at the `// scaffold:*`
markers; keep those markers.

## Rules

```dart
// Wrong
Navigator.push(context, MaterialPageRoute(builder: (_) => const OrdersScreen()));
Navigator.pushNamed(context, '/orders');

// Right
Navigator.of(context).pushNamed(AppRoutes.orders);
```

- Every screen gets an `AppRoutes` constant and a case in
  `onGenerateAppRoute` before anything links to it. Widgets never build a
  `MaterialPageRoute` themselves.
- `pushNamed`, `pushReplacementNamed`, `pushNamedAndRemoveUntil` and `pop`
  only, always with an `AppRoutes` constant.
- Arguments: pass one typed value, `pushNamed(AppRoutes.orderDetail,
  arguments: order.id)`, and read it once in `onGenerateAppRoute`
  (`settings.arguments! as String`), handing a typed value to the screen
  constructor. Screens never read `ModalRoute.of(context)!.settings`.
- Auth or onboarding gating happens where the route is built (a check in
  `onGenerateAppRoute` or the initial route), not in a widget that
  conditionally renders one screen or another.
- Need deep links, web URLs or nested navigators later? That is the point
  to move to go_router; don't hand-roll a Router delegate.
