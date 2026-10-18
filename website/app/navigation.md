---
title: Navigation
description: go_router, auto_route or Flutter's built-in Navigator. How each router option is wired in a Flutter Kickstart app, and how features register and link to routes.
---

# Navigation

You choose the router in the setup questions (`--router`). **go_router** is
the default because it covers deep links, web URLs and redirects with the
least code, but the choice is yours: Flutter Kickstart doesn't lock a project
into one routing package.

Whatever you pick, two things stay the same:

- `lib/core/routing/app_router.dart` holds `AppRoutes`, one constant per
  screen, and the single place routes are registered.
- `add_feature.py` registers every new feature's route for you, at the
  `// scaffold:*` markers in that file.

## Side by side

| | go_router (default) | auto_route | Navigator |
| --- | --- | --- | --- |
| Package | `go_router` | `auto_route` + `auto_route_generator` | none |
| Route table | `buildAppRouter()` with `GoRoute`s | `AppRouter` with `AutoRoute`s | `onGenerateAppRoute()` switch |
| Screens | plain widgets | annotated `@RoutePage()` | plain widgets |
| Navigate | `context.push(AppRoutes.orders)` | `context.router.push(const OrdersRoute())` | `Navigator.of(context).pushNamed(AppRoutes.orders)` |
| Parameters | `/orders/:id`, `state.pathParameters` | `@PathParam`, typed route args | one typed `arguments` value |
| Guards | `redirect` | `AutoRouteGuard` | checks in `onGenerateAppRoute` |
| Deep links and web URLs | yes | yes | limited |
| Code generation | no | yes (`app_router.gr.dart`) | no |
| App widget | `MaterialApp.router` | `MaterialApp.router` | `MaterialApp` |

## Which one?

- **go_router** for most apps. It is maintained by the Flutter team, needs
  no code generation, and handles deep links, web and auth redirects.
- **auto_route** when the team wants compile-time typed routes and
  arguments, and is happy running `build_runner` after adding a screen.
- **Navigator** for small apps with no deep links or web target, or when
  the client doesn't want a routing dependency. If deep links arrive later,
  move to go_router rather than hand-writing a `RouterDelegate`.

## Adding a route

`python3 tool/kickstart/add_feature.py --name orders` adds the `AppRoutes`
constant and the route entry for whichever router the app uses (it reads
`pubspec.yaml`), and prints how to link to the new screen. For a screen added
by hand, the project's `flutter-navigation` skill tells the AI agent (and
you) the exact steps for your router.

## Rules the AI layer enforces

- Every screen gets an `AppRoutes` constant and one registration in
  `app_router.dart` before anything links to it.
- No raw path strings, and no `MaterialPageRoute` built inside a widget.
- Data a deep link would lose isn't passed through untyped extras.
- Auth or onboarding gating lives in the router (redirect, guard or the
  route table), not in a widget that swaps screens.
