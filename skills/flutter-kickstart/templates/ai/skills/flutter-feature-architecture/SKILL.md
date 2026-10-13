---
name: flutter-feature-architecture
description: Feature-first clean architecture for {{app_name}} (lib/core and lib/features/<name>/{domain,data,presentation}). Use when adding a feature, screen, repository, use case, data source, model or service, when deciding where a file belongs or what may import what, or when refactoring structure.
---

# Feature architecture

## Add a feature with the generator, not by hand

```bash
python3 tool/kickstart/add_feature.py --name orders [--entity order] [--endpoint /orders]
```

It creates every layer, DI wiring, the route, an l10n title, and tests,
then runs code generation, `analyze` and `test`. Then replace the stub
model fields (`id`, `title`) with the real API shape and extend from there.

## Layout

```
lib/features/<feature>/
  domain/
    entities/<entity>.dart              plain Dart, no JSON, no Flutter
    repositories/<feature>_repository.dart   abstract interface
    usecases/get_<feature>.dart         one action per class, `call()`
  data/
    models/<entity>_model.dart          fromJson/toJson/toEntity
    datasources/<feature>_remote_data_source.dart   uses AppApiClient
    repositories/<feature>_repository_impl.dart     models -> entities
  presentation/
    {{presentation_dirs}}
    screens/<feature>_screen.dart
    widgets/                            extracted widgets
  <feature>_{{feature_di_file}}.dart     DI wiring (the only file that names implementations)
  <feature>.dart                        barrel: exports the screen only
```

## Dependency rule

`presentation -> domain <- data`

- `domain/` imports only `dartz`, `core/network/app_failure.dart` and
  other domain files. Never `data/`, `presentation/` or Flutter.
- `data/` implements domain contracts and talks to `AppApiClient`.
- `presentation/` depends on use cases and entities. It reaches
  implementations only through the feature's DI file.
- A feature never imports another feature. Move shared code to
  `lib/core/` (contract + implementation) or `lib/core/widgets/`.

## core/ before new abstractions

Check `lib/core/{config,di,error_reporting,logging,network,routing,theming,widgets}`
before adding a cross-cutting service. A new third-party SDK gets an
interface in `core/` and its only import lives next to that interface.

## Widgets

- Extract any `build()` over ~30 lines into a widget class under
  `presentation/widgets/` (private `_Widget` classes in the same file are
  fine for small pieces).
- Keep a `StatefulWidget` and its `State` in the same file.
