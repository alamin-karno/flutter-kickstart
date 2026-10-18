---
name: flutter-figma-to-flutter
description: Turns a Figma frame or component into Flutter widget code that uses the app's existing theme tokens, shared widgets, routing and tests, for apps created with flutter-kickstart. Use when the user shares a Figma link or node, or asks to implement, build or code up a design, screen or component from Figma.
---

# Figma to Flutter

Needs a Figma MCP server connected to the agent: Figma's official Dev Mode
MCP server, or the community `figma-flutter-mcp`. Both return design context
(nodes, variables, screenshots), not Flutter code. This skill turns that
context into code that follows the app's conventions. If no Figma tool is
available, say so and ask the user to connect one. Don't guess a design from
a screenshot alone.

## 1. Read the design context

Call the server's context tool for the file/node (`get_design_context` on
the official server, or the node/screen extraction tool on
`figma-flutter-mcp`). Collect:

- Layout, spacing and sizing of the frame and its children.
- Colours, typography, radii and the variables/styles behind them.
- Text content and layer names.
- A screenshot, as a sanity check only. Metadata beats pixels.

## 2. Map tokens before writing a widget

Open `lib/core/theming/app_theme_extension.dart`,
`lib/core/theming/app_theme.dart` and `figma-token-map.md` (repo root).

- Variable already mapped: use the mapped `context.colors.<role>`,
  `context.appColors.<token>`, `context.textTheme.<style>`,
  `AppSpacing.<step>` or `AppRadius.<step>`. Never re-emit a literal.
- Variable not mapped: that is a design-system gap, not permission to
  hardcode. Prefer a Material `ColorScheme` role when it fits. Otherwise add
  the token to `AppColors` (both `light` and `dark`), `AppSpacing` or
  `AppRadius`, add the row to `figma-token-map.md`, then use it. List every
  new token in your summary.
- Off-scale values (e.g. 14px spacing): snap to the nearest token and say
  so, unless the designer confirms a new step is needed.

## 3. Reuse components first

Before writing a button, card, list tile or input:

1. Check the component table in `figma-token-map.md` (kept by hand, or by
   Code Connect if the team uses it).
2. Check `lib/core/widgets/` and the feature's `presentation/widgets/`.

Write a new widget only when neither has one. Shared widgets go in
`lib/core/widgets/`, feature-only ones in `presentation/widgets/`. Record
the new widget in the component table.

## 4. Place the screen

A screen for an existing flow goes in that feature's `presentation/screens/`.
A new flow gets a feature. Inside the app, run
`python3 tool/kickstart/add_feature.py --name <feature>` to generate all
layers, the route and tests, then replace the generated view with the
design. User-visible text goes into `lib/l10n/arb/app_en.arb` and is read
through `context.l10n`.

## 5. Export images and icons

Vector layers (icons, logos, illustrations) are exported as SVG with the
Figma tool's asset/download call; raster artwork as PNG at 1x, 2x and 3x.
Never screenshot a layer to use it as an asset, and never use an image for
something a Material icon or a themed widget can draw.

- Icons go in `assets/icons/ic_<name>.svg`, everything else in
  `assets/images/<name>.<ext>`, in snake_case.
- Add one entry per file to `ImageResourceResolver`
  (`lib/core/asset_resolver/resource_resolver.dart`) and render it with
  `ImageResourceResolver.x.getImageWidget(...)`, tinting icons with a theme
  colour. The `flutter-assets` skill has the details.
- No `'assets/...'` string, `Image.asset` or `SvgPicture.asset` in screen
  code.

## 6. Wire navigation

Every screen is registered in `lib/core/routing/app_router.dart` with an
`AppRoutes` constant, and is linked to the way the app's
`flutter-navigation` skill describes for its router (go_router, auto_route
or Navigator). A screen nothing routes to is not done.

## 7. Verify

Add a widget test for the screen (`tester.pumpApp`). Add an `alchemist`
golden for shared components. Then run `./scripts/quality_gate.sh` and fix
whatever it reports.

## 8. Report reused vs new

State which parts came from existing tokens and widgets, which tokens,
widgets and assets are new, and any values you snapped to the scale.
