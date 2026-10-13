---
title: Figma to Flutter
description: Turn a Figma frame into Flutter widgets that reuse your theme tokens, shared widgets, routes and tests with the flutter-figma-to-flutter skill.
---

# Figma to Flutter

The `flutter-figma-to-flutter` skill turns a Figma frame or component into
Flutter code that follows the app's conventions. It works on apps created by
Flutter Kickstart.

## What you need

A Figma MCP server connected to your agent, for example Figma's official Dev
Mode MCP server or the community `figma-flutter-mcp`. These servers return
design data (layers, variables, a screenshot), not Flutter code. The skill
turns that data into code.

If no Figma tool is connected, the agent tells you and asks you to connect
one. It does not guess a design from a screenshot alone.

## How to use it

> Implement this Figma frame: https://www.figma.com/design/...

## What the agent does

1. **Reads the design**: layout, spacing, colours, text styles and the variables behind them.
2. **Maps tokens first.** Colours, text, spacing and radius come from `context.colors`, `context.textTheme`, `AppSpacing` and `AppRadius`. A colour that isn't mapped yet gets added as a token (light and dark) and recorded in `figma-token-map.md`, never hard-coded.
3. **Reuses widgets** from `lib/core/widgets/` and the feature before writing new ones.
4. **Places the screen** in the right feature. A new flow gets a new feature through `add_feature.py`.
5. **Wires navigation** with an `AppRoutes` constant and a `GoRoute`.
6. **Adds tests**: a widget test for the screen, and a golden test for shared components.
7. **Reports** what was reused, what is new, and any values it rounded to the spacing scale.

## figma-token-map.md

Every generated app has a `figma-token-map.md` at the root. It maps Figma
variables to theme tokens, and Figma components to Flutter widgets. Keep it
up to date and the agent reuses more on every screen.
