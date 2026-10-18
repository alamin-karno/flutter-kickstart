---
title: Images and icons
description: The asset resolver in a Flutter Kickstart app. Every bundled SVG or PNG goes through ImageResourceResolver, with a test that blocks raw asset paths and missing files.
---

# Images and icons

Every generated app has an asset resolver in `lib/core/asset_resolver/`, the
same pattern the team's production apps use. Asset paths are written in one
file, and screens ask for a widget instead of building `Image.asset` or
`SvgPicture.asset` from a string.

```text
assets/
  icons/               small UI glyphs: ic_<name>.svg
  images/              logos, illustrations, photos: <name>.svg / <name>.png
lib/core/asset_resolver/
  image_resource.dart       ImageResource: getPath + getImageWidget(...)
  asset_image_provider.dart AssetImageProvider: .assetImage
  svg_image_resource.dart   SVGImageResource (flutter_svg)
  png_image_resource.dart   PNGImageResource (Image.asset + AssetImage)
  resource_resolver.dart    ImageResourceResolver: one entry per file
```

Both folders are declared in `pubspec.yaml`, and `flutter_svg` is a
dependency. The app starts with one example, `assets/images/app_logo.svg`.

## Adding an asset

1. Put the file in the right folder with a snake_case name, e.g.
   `assets/icons/ic_search.svg`. Use SVG for anything vector, and PNG with
   `2.0x/` and `3.0x/` variants for photos.
2. Add one entry to `ImageResourceResolver`:

   ```dart
   static const SVGImageResource searchIcon = SVGImageResource(
     '$iconBasePath/ic_search.svg',
   );
   ```

3. Use it:

   ```dart
   ImageResourceResolver.searchIcon.getImageWidget(
     width: 24,
     height: 24,
     color: context.colors.primary, // tints the SVG
   );

   // Raster images also work where an ImageProvider is needed:
   DecorationImage(image: ImageResourceResolver.emptyOrders.assetImage);
   ```

A new sub-folder such as `assets/images/onboarding/` must also be added to
`pubspec.yaml`, because asset folders aren't recursive.

## What keeps it honest

`test/core/asset_resolver/resource_resolver_test.dart` runs with the rest of
the suite (and so in `quality_gate.sh` and CI). It fails when:

- a path in `ImageResourceResolver` has no file on disk, or
- any Dart file under `lib/` outside `lib/core/asset_resolver/` contains an
  `'assets/...'` string.

The `flutter-assets` skill and the rule in `AGENTS.md` tell AI agents the
same thing, and the architecture review checks for raw `Image.asset` and
`SvgPicture.asset` calls. The Figma-to-Flutter skill exports icons and images
straight into these folders and registers them in the resolver.
