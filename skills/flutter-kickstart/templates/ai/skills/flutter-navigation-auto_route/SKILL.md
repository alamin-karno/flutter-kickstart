---
name: flutter-navigation
description: Navigation conventions for {{app_name}}: auto_route only, typed generated routes, path constants in AppRoutes, guards for gating. Use when adding a screen or route, navigating, passing route parameters, handling deep links, or gating routes behind auth/onboarding.
---

# Navigation (auto_route)

`lib/core/routing/app_router.dart` owns `AppRoutes` (path constants) and
`AppRouter` (`@AutoRouterConfig`). `build_runner` generates the typed
`XRoute` classes into `app_router.gr.dart`; never edit that file.
`add_feature.py` registers new feature routes at the `// scaffold:*`
markers; keep those markers.

## Adding a screen

1. Annotate the screen widget with `@RoutePage()`. The generated route
   drops `Screen`: `OrdersScreen` becomes `OrdersRoute`.
2. Add `static const orders = '/orders';` to `AppRoutes`.
3. Add `AutoRoute(page: OrdersRoute.page, path: AppRoutes.orders),` to
   `AppRouter.routes`.
4. Run `{{dart}} run build_runner build --delete-conflicting-outputs`.

## Rules

```dart
// Wrong
Navigator.push(context, MaterialPageRoute(builder: (_) => const OrdersScreen()));
context.router.pushPath('/orders');

// Right
context.router.push(const OrdersRoute());
context.router.push(OrderDetailRoute(id: order.id));
```

- Navigate with the typed route: `context.router.push(...)`,
  `context.router.replace(...)`, `context.router.maybePop()`. No
  `Navigator.*`, no raw path strings.
- Path parameters: declare `/orders/:id` and mark the screen parameter
  `@PathParam('id')`. Required data goes in the path or as a typed
  constructor argument the URL can rebuild; not in an object that is lost
  on deep links and web refresh.
- Auth or onboarding gating is an `AutoRouteGuard` (on the route's
  `guards:`), not a widget that conditionally renders one screen or
  another.
- Nested navigation (tabs, bottom bars) uses `AutoTabsRouter` with child
  routes, not a hand-managed `IndexedStack` of screens.
