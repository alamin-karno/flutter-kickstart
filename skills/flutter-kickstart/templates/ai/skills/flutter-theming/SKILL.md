---
name: flutter-theming
description: Theming conventions for {{app_name}}: Material 3 ColorScheme plus AppColors/AppSpacing/AppRadius tokens, no hardcoded values, dark mode. Use when styling any widget, adding a colour/spacing/typography token, implementing a design or mockup, or changing the theme.
---

# Theming

- `lib/core/theming/app_theme.dart`: `AppTheme.light` / `AppTheme.dark`
  (the only place colours enter the app).
- `lib/core/theming/app_theme_extension.dart`: `AppColors` (brand,
  success, warning, info) as a `ThemeExtension`, `AppSpacing`, `AppRadius`,
  and the `context.theme / colors / textTheme / appColors` extensions.

## No hardcoded values

```dart
// Wrong
Container(color: const Color(0xFF2962FF), padding: const EdgeInsets.all(16));

// Right
Container(
  color: context.colors.primary,
  padding: const EdgeInsets.all(AppSpacing.md),
);
```

- Material roles first: `context.colors.primary`, `.surface`, `.error`.
- Brand/semantic colours Material lacks: `context.appColors.success`.
- Text: `context.textTheme.titleMedium`, adjusted with `copyWith` only
  for weight/colour.
- Spacing and radius: `AppSpacing.*`, `AppRadius.*`. No bare numbers.
- A new token goes into `AppColors` (both `light` and `dark`),
  `AppSpacing` or `AppRadius` first, then gets used.

## Dark mode

Dark mode is already wired (`darkTheme: AppTheme.dark`). Never branch on
`Theme.of(context).brightness` in a feature widget; add a token instead.

## From a design

Implementing Figma: use the `flutter-figma-to-flutter` skill and keep
`figma-token-map.md` in sync. Other design hand-offs (tokens JSON, CSS,
style guides): map them onto these same tokens and record the mapping in
`figma-token-map.md`.
