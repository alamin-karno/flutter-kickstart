---
name: flutter-assets
description: Image and icon asset conventions for {{app_name}}: every bundled SVG/PNG goes through ImageResourceResolver in lib/core/asset_resolver/, never a raw 'assets/...' string. Use when adding, renaming, replacing or deleting an image or icon, exporting assets from Figma, showing a logo/illustration/icon from a file, or seeing a raw Image.asset / SvgPicture.asset call.
---

# Assets

Bundled images live in two folders, both declared in `pubspec.yaml`:

| Folder | Holds | File name |
| --- | --- | --- |
| `assets/icons/` | small UI glyphs, usually tinted | `ic_<name>.svg` |
| `assets/images/` | logos, illustrations, photos, backgrounds | `<name>.svg` / `<name>.png` |

`lib/core/asset_resolver/` is the only code that knows those paths:

- `ImageResource`: the contract, `getPath` + `getImageWidget(...)`.
- `SVGImageResource`: vector files, rendered with `flutter_svg`.
- `PNGImageResource`: raster files (PNG, JPG, WebP); also an
  `AssetImageProvider` with `.assetImage` for `DecorationImage`,
  `CircleAvatar.backgroundImage` and similar.
- `ImageResourceResolver` (`resource_resolver.dart`): one static per file.

## Adding an asset

1. Export SVG when the design is vector (icons nearly always are). Use
   raster only for photos or complex artwork, and add `2.0x/` and `3.0x/`
   variants beside the 1x file.
2. Name it in snake_case: `assets/icons/ic_search.svg`,
   `assets/images/empty_orders.png`. No spaces, no capitals, no `-`.
3. Add one entry to `ImageResourceResolver`, typed by format, in the
   matching section and sorted by name:

   ```dart
   static const SVGImageResource searchIcon = SVGImageResource(
     '$iconBasePath/ic_search.svg',
   );
   ```

4. Use it:

   ```dart
   // Wrong
   SvgPicture.asset('assets/icons/ic_search.svg', color: Color(0xFF2962FF));
   Image.asset('assets/images/empty_orders.png');

   // Right
   ImageResourceResolver.searchIcon.getImageWidget(
     width: 24,
     height: 24,
     color: context.colors.primary,
   );
   ImageResourceResolver.emptyOrders.getImageWidget(height: 160);
   DecorationImage(image: ImageResourceResolver.emptyOrders.assetImage);
   ```

5. A new sub-folder (e.g. `assets/images/onboarding/`) must also be added
   under `flutter: assets:` in `pubspec.yaml`; folders are not recursive.

## Rules

- No `'assets/...'` string anywhere outside `lib/core/asset_resolver/`.
  `test/core/asset_resolver/resource_resolver_test.dart` fails the build
  if one appears, or if a resolver path has no file on disk.
- Tint with theme colours (`context.colors.*`, `context.appColors.*`),
  never a hex literal. Don't tint full-colour illustrations.
- Prefer Material `Icons.*` when the design uses a stock Material icon;
  the resolver is for the app's own artwork.
- Deleting an asset means deleting its file and its resolver entry
  together, after checking nothing still uses it.
- Network images (URLs from the API) are not assets and don't belong in
  the resolver.
- Fonts are declared in `pubspec.yaml` and used through the theme's
  `TextTheme`, never by family name in a widget.
