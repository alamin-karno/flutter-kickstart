#!/usr/bin/env python3
"""Add a clean-architecture feature to a project created by flutter-kickstart.

Generates domain (entity, repository contract, use case), data (model,
remote data source, repository impl), presentation (Cubit or Riverpod
controller + screen), DI wiring, a route, l10n strings and tests, then runs
code generation and formatting.

    python3 add_feature.py --root . --name orders [--entity order]
        [--endpoint /orders] [--state bloc|riverpod] [--dry-run] [--no-verify]

Safe to re-run: existing files are kept unless --force is given, and route /
parser / l10n insertions are idempotent.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    TEMPLATES,
    add_arb_strings,
    camel,
    dart_cmd,
    detect_state_management,
    fail,
    flutter_cmd,
    info,
    insert_before_marker,
    pascal,
    read_package_name,
    render_tree,
    run,
    safe_fix,
    singular,
    snake,
    step,
    title,
    valid_package_name,
    warn,
)

RESERVED = {"core", "app", "l10n", "home", "shared"}


def register_route(root: Path, package: str, feature: str, path: str, screen: str, dry_run: bool) -> None:
    router = root / "lib/core/routing/app_router.dart"
    ok = all(
        [
            insert_before_marker(
                router,
                "scaffold:imports",
                f"import 'package:{package}/features/{feature}/{feature}.dart';",
                dry_run=dry_run,
            ),
            insert_before_marker(
                router,
                "scaffold:route-paths",
                f"static const {camel(feature)} = '{path}';",
                dry_run=dry_run,
            ),
            insert_before_marker(
                router,
                "scaffold:routes",
                f"GoRoute(\n"
                f"  path: AppRoutes.{camel(feature)},\n"
                f"  name: '{camel(feature)}',\n"
                f"  builder: (context, state) => const {screen}(),\n"
                f"),",
                dry_run=dry_run,
            ),
        ]
    )
    if ok:
        info(f"route  {path} -> {screen}")
    else:
        warn(
            "lib/core/routing/app_router.dart has no `// scaffold:*` markers. "
            f"Add `static const {camel(feature)} = '{path}';` to AppRoutes and a "
            f"GoRoute building `const {screen}()` by hand."
        )


def register_parser(root: Path, package: str, feature: str, entity: str, state: str, dry_run: bool) -> None:
    di = root / ("lib/core/di/register_module.dart" if state == "bloc" else "lib/core/di/providers.dart")
    model = f"{pascal(entity)}Model"
    ok = insert_before_marker(
        di,
        "scaffold:model-imports",
        f"import 'package:{package}/features/{feature}/data/models/{entity}_model.dart';",
        dry_run=dry_run,
    ) and insert_before_marker(
        di, "scaffold:parsers", f"serializer.addParser<{model}>({model}.fromJson);", dry_run=dry_run
    )
    if ok:
        info(f"parser {model} registered in {di.relative_to(root)}")
    else:
        warn(f"Register `addParser<{model}>({model}.fromJson)` on the JsonSerializer in {di.name} by hand.")


def generate(
    root: Path,
    name: str,
    *,
    entity: str | None = None,
    endpoint: str | None = None,
    state: str | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> None:
    feature = snake(name)
    if not valid_package_name(feature):
        fail(f"Feature name {name!r} must be snake_case letters/digits.")
    if feature in RESERVED:
        fail(f"{feature!r} is reserved by the app shell; pick another feature name.")
    entity = snake(entity) if entity else singular(feature)
    if entity == feature:
        entity = f"{feature}_item"
    endpoint = endpoint or f"/{feature.replace('_', '-')}"
    package = read_package_name(root)
    state = state or detect_state_management(root)

    values = {
        "package": package,
        "feature": feature,
        "Feature": pascal(feature),
        "feature_camel": camel(feature),
        "entity": entity,
        "Entity": pascal(entity),
        "endpoint": endpoint,
    }
    tokens = {"feature": feature, "entity": entity}
    step(f"Feature `{feature}` ({state}, entity {pascal(entity)}, GET {endpoint})")
    for part in ("common", state):
        render_tree(
            TEMPLATES / "feature" / part,
            root,
            values,
            path_tokens=tokens,
            overwrite=force,
            dry_run=dry_run,
        )
    register_route(root, package, feature, f"/{feature.replace('_', '-')}", f"{pascal(feature)}Screen", dry_run)
    register_parser(root, package, feature, entity, state, dry_run)
    add_arb_strings(root / "lib/l10n/arb/app_en.arb", {f"{camel(feature)}Title": title(feature)}, dry_run)


def post_generate(root: Path) -> None:
    step("Code generation and formatting")
    run([*flutter_cmd(root), "gen-l10n"], root, quiet=True)
    run([*dart_cmd(root), "run", "build_runner", "build", "--delete-conflicting-outputs"], root, quiet=True)
    safe_fix(root)
    run([*dart_cmd(root), "format", "lib", "test"], root, quiet=True)


def verify(root: Path) -> None:
    step("Verify")
    run([*flutter_cmd(root), "analyze"], root)
    run([*flutter_cmd(root), "test"], root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="Flutter project root (default: .)")
    parser.add_argument("--name", required=True, help="Feature name, e.g. orders")
    parser.add_argument("--entity", help="Entity name (default: singular of --name)")
    parser.add_argument("--endpoint", help="GET path for the list (default: /<name>)")
    parser.add_argument("--state", choices=["bloc", "riverpod"], help="Default: detected from pubspec.yaml")
    parser.add_argument("--force", action="store_true", help="Overwrite existing feature files")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-verify", action="store_true", help="Skip flutter analyze/test")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    generate(
        root,
        args.name,
        entity=args.entity,
        endpoint=args.endpoint,
        state=args.state,
        force=args.force,
        dry_run=args.dry_run,
    )
    if args.dry_run:
        return
    post_generate(root)
    if not args.no_verify:
        verify(root)
    print(
        "\nDone. Next: replace the stub model fields with the real API shape, "
        "then link to the screen with `context.push(AppRoutes."
        f"{camel(snake(args.name))})`."
    )


if __name__ == "__main__":
    main()
