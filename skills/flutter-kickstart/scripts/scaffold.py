#!/usr/bin/env python3
"""Scaffold a production-ready Flutter app from the flutter-kickstart setup questions.

    python3 scaffold.py --name acme_wallet --app-name "Acme Wallet" \
        --org com.vivasoftltd --platforms android,ios --state bloc \
        --base-url development=https://dev.api.acme.com \
        --base-url staging=https://stg.api.acme.com \
        --base-url production=https://api.acme.com \
        --network viva --router go_router --ci github --locales en \
        --features auth,orders --crash sentry --agents all

    python3 scaffold.py --config answers.json      # same keys as the flags
    python3 scaffold.py ... --dry-run              # print the plan only

Steps: Very Good CLI base (flavors, lints, l10n) -> core abstractions ->
app shell + asset resolver -> home + starter features -> dependencies -> CI/CD -> AI-agent
layer for every supported agent -> codegen -> format -> analyze -> test.
Stdlib only; needs Flutter (or fvm) and Very Good CLI (activated if missing).
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

import add_feature  # noqa: E402
import setup_ai  # noqa: E402
from _common import (  # noqa: E402
    API_CLIENTS,
    ARB_DIR,
    ASSET_DIRS,
    NETWORK_LABELS,
    CI_CHOICES,
    DEFAULT_NETWORK,
    DEFAULT_ROUTER,
    NETWORK_CHOICES,
    ROUTER_CHOICES,
    ROUTER_LABELS,
    STATE_CHOICES,
    TEMPLATE_LOCALE,
    TEMPLATES,
    camel,
    dart_cmd,
    fail,
    flutter_cmd,
    info,
    insert_before_marker,
    render_tree,
    route_entry,
    router_values,
    run,
    safe_fix,
    snake,
    step,
    title,
    valid_package_name,
    warn,
)

DEFAULT_FLAVORS = ["development", "staging", "production"]
FLAVOR_SUFFIX = {"development": " [DEV]", "staging": " [STG]", "production": ""}
CRASH_CHOICES = ("none", "sentry", "crashlytics")
# Not counted towards the coverage floor: generated code and entrypoints.
# Used by the scaffold's own check and rendered into pr_checks.yml.
COVERAGE_EXCLUDES = ("**/*.g.dart", "**/*.gr.dart", "**/*.config.dart", "lib/l10n/gen/**", "lib/main_*.dart", "lib/bootstrap.dart")

BLOC_DEPS = ["get_it", "injectable", "dev:injectable_generator"]
RIVERPOD_DEPS = ["flutter_riverpod", "riverpod_annotation", "dev:riverpod_generator"]
COMMON_DEPS = ["dio", "dartz", "flutter_svg", "meta", "dev:build_runner"]
ROUTER_DEPS = {"go_router": ["go_router"], "auto_route": ["auto_route", "dev:auto_route_generator"], "navigator": []}
NETWORK_DEPS = {"viva": ["viva_network_kit"], "dio": []}
CRASH_DEPS = {"none": [], "sentry": ["sentry_flutter"], "crashlytics": ["firebase_core", "firebase_crashlytics"]}
# Android minSdk each crash SDK requires (Flutter's default is lower).
CRASH_MIN_SDK = {"none": 0, "sentry": 26, "crashlytics": 23}
CRASH_CTOR = {
    "none": ("console_crash_reporter.dart", "ConsoleCrashReporter(logger)"),
    "sentry": ("sentry_crash_reporter.dart", "SentryCrashReporter(config)"),
    "crashlytics": ("crashlytics_crash_reporter.dart", "CrashlyticsCrashReporter(logger)"),
}


# --------------------------------------------------------------------------- #
# Answers
# --------------------------------------------------------------------------- #

def parse_args() -> Dict:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", help="JSON file with the answers (keys match the flags, dashes -> underscores)")
    p.add_argument("--name", help="Package name, snake_case (e.g. acme_wallet)")
    p.add_argument("--app-name", help="Display name (default: from --name)")
    p.add_argument("--description", default="")
    p.add_argument("--org", help="Organization / reverse domain, e.g. com.vivasoftltd")
    p.add_argument("--platforms", default="android,ios", help="Comma list: android,ios,web,macos,windows")
    p.add_argument("--state", choices=STATE_CHOICES, help="State management (always ask the user)")
    p.add_argument("--network", choices=NETWORK_CHOICES, default=DEFAULT_NETWORK,
                   help="HTTP client behind AppApiClient: viva (viva_network_kit) or dio (plain Dio)")
    p.add_argument("--router", choices=ROUTER_CHOICES, default=DEFAULT_ROUTER,
                   help="Navigation: go_router (default), auto_route or navigator (Flutter's built-in, no package)")
    p.add_argument("--ci", choices=CI_CHOICES, default="github",
                   help="CI/CD to generate: github (Actions + Fastlane) or none")
    p.add_argument("--locales", default=TEMPLATE_LOCALE,
                   help=f"Comma list of supported locales; {TEMPLATE_LOCALE} is always included and is the template")
    p.add_argument("--flavors", default=",".join(DEFAULT_FLAVORS))
    p.add_argument("--base-url", action="append", default=[], metavar="FLAVOR=URL",
                   help="Per-flavor API base URL; repeat. A bare URL applies to every flavor.")
    p.add_argument("--features", default="", help="Starter features beyond home, comma list (e.g. auth,orders)")
    p.add_argument("--crash", choices=CRASH_CHOICES, default="none")
    p.add_argument("--figma-url", default="")
    p.add_argument("--agents", default="all", help=f"'all' or comma list of: {', '.join(setup_ai.AGENTS)}")
    p.add_argument("--copy-skills", action="store_true", help="Copy skills per agent instead of symlinking")
    p.add_argument("--coverage-floor", type=int, default=80)
    p.add_argument("--output-dir", default=".", help="Parent directory for the new project")
    p.add_argument("--skip-create", action="store_true", help="Use an existing Very Good CLI project at <output-dir>/<name>")
    p.add_argument("--skip-verify", action="store_true", help="Skip analyze/test at the end")
    p.add_argument("--dry-run", action="store_true")
    args = vars(p.parse_args())

    if args.get("config"):
        data = json.loads(Path(args["config"]).read_text(encoding="utf-8"))
        for key, value in data.items():
            key = key.replace("-", "_")
            if isinstance(value, list) and key not in ("base_url",):
                value = ",".join(value)
            if key == "base_url" and isinstance(value, dict):
                value = [f"{k}={v}" for k, v in value.items()]
            if key == "base_url" and isinstance(value, str):
                value = [value]
            args[key] = value
    return args


def normalize(args: Dict) -> Dict:
    name = snake(args.get("name") or "")
    if not name or not valid_package_name(name):
        fail("--name is required and must be a valid Dart package name (snake_case).")
    if not args.get("org") or not re.fullmatch(r"[a-zA-Z][\w]*(\.[a-zA-Z][\w]*)+", args["org"]):
        fail("--org is required, e.g. com.vivasoftltd")
    if not args.get("state"):
        fail("--state is required (bloc or riverpod). Ask the user; there is no default.")
    flavors = [snake(f) for f in str(args["flavors"]).split(",") if f.strip()]
    if not flavors:
        fail("--flavors needs at least one flavor.")
    urls: Dict[str, str] = {}
    for item in args.get("base_url") or []:
        if "=" in item and not item.split("=", 1)[0].startswith("http"):
            flavor, url = item.split("=", 1)
            urls[snake(flavor)] = url.strip()
        else:
            urls.update({f: item.strip() for f in flavors})
    for f in flavors:
        urls.setdefault(f, f"https://{f}.api.example.com")
    platforms = [p.strip() for p in str(args["platforms"]).split(",") if p.strip()]
    features = [snake(f) for f in str(args.get("features") or "").split(",") if f.strip()]
    features = [f for f in features if f != "home"]
    locales = [l.strip() for l in str(args.get("locales") or "").split(",") if l.strip()]
    bad = [l for l in locales if not re.fullmatch(r"[a-z]{2,3}(_[A-Z]{2}|_[A-Z][a-z]{3})?", l)]
    if bad:
        fail(f"--locales {bad} are not locale codes like en, bn, pt_BR or zh_Hant.")
    locales = [TEMPLATE_LOCALE] + [l for l in dict.fromkeys(locales) if l != TEMPLATE_LOCALE]
    return {
        **args,
        "name": name,
        "app_name": args.get("app_name") or title(name),
        "flavors": flavors,
        "base_urls": urls,
        "platforms": platforms,
        "features": features,
        "locales": locales,
        "agents": setup_ai.parse_agents(args.get("agents") or "all"),
    }


# --------------------------------------------------------------------------- #
# Steps
# --------------------------------------------------------------------------- #

def ensure_very_good() -> List[str]:
    def works() -> bool:
        exe = shutil.which("very_good")
        if not exe:
            return False
        return subprocess.run([exe, "--version"], capture_output=True, text=True).returncode == 0

    if not works():
        info("Very Good CLI missing or broken; (re)activating it")
        run(["dart", "pub", "global", "activate", "very_good_cli"], Path.cwd(), quiet=True)
        if not works():
            fail("Could not run `very_good`. Ensure ~/.pub-cache/bin is on PATH, then re-run.")
    return ["very_good"]


def create_base(a: Dict, root: Path) -> None:
    step("Very Good CLI base project")
    if a["skip_create"]:
        if not (root / "pubspec.yaml").exists():
            fail(f"--skip-create given but {root} has no pubspec.yaml")
        info(f"using existing project at {root}")
        return
    if root.exists() and any(root.iterdir()):
        fail(f"{root} already exists and is not empty. Use --skip-create to reuse it, or pick another --name/--output-dir.")
    cmd = [
        *ensure_very_good(), "create", "flutter_app", a["name"],
        "--org-name", a["org"],
        "--description", a["description"] or f"{a['app_name']} Flutter app",
        "--platforms", ",".join(a["platforms"]),
        "-o", str(root.parent),
    ]
    run(cmd, root.parent, quiet=True)


def read_ids(root: Path, a: Dict) -> Dict[str, str]:
    android_id = f"{a['org']}.{a['name']}"
    gradle = root / "android/app/build.gradle.kts"
    if gradle.exists():
        m = re.search(r'applicationId\s*=\s*"([^"]+)"', gradle.read_text(encoding="utf-8"))
        if m:
            android_id = m.group(1)
    ios_id = f"{a['org']}.{a['name'].replace('_', '-')}"
    pbx = root / "ios/Runner.xcodeproj/project.pbxproj"
    if pbx.exists():
        ids = re.findall(r"PRODUCT_BUNDLE_IDENTIFIER = ([\w.\-]+);", pbx.read_text(encoding="utf-8"))
        base = sorted((i for i in ids if not i.endswith(("RunnerTests", ".dev", ".stg"))), key=len)
        if base:
            ios_id = base[0]
    return {"android_id": android_id, "ios_id": ios_id}


def flutter_info(root: Path) -> Dict[str, str]:
    try:
        out = subprocess.run([*flutter_cmd(root), "--version", "--machine"], cwd=root, capture_output=True, text=True)
        return json.loads(out.stdout[out.stdout.index("{"):])
    except Exception:  # noqa: BLE001
        return {}


def flutter_version(root: Path) -> str:
    version = flutter_info(root).get("frameworkVersion")
    if not version:
        warn("Could not read the Flutter version; CI will use the latest stable.")
    return version or "3.x"


def _version_tuple(v: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3])


def align_android_kotlin(root: Path) -> None:
    """Very Good CLI's template can pin a Kotlin Gradle plugin older than the
    installed Flutter SDK accepts (e.g. VGC 1.5.0 pins 2.2.10, Flutter 3.47
    requires >= 2.2.20), which breaks every Android build. Raise it to the
    SDK's recommended minimum (read from flutter_tools, so it tracks the SDK),
    and move `kotlinOptions` to the `compilerOptions` DSL that newer Kotlin
    versions require."""
    settings = root / "android/settings.gradle.kts"
    app_gradle = root / "android/app/build.gradle.kts"
    sdk = flutter_info(root).get("flutterRoot")
    if not (settings.exists() and sdk):
        return
    checker = Path(sdk) / "packages/flutter_tools/gradle/src/main/kotlin/DependencyVersionChecker.kt"
    text = checker.read_text(encoding="utf-8") if checker.exists() else ""
    m = re.search(r"warnKGPVersion: Version = Version\((\d+), (\d+), (\d+)\)", text) or re.search(
        r"errorKGPVersion: Version = Version\((\d+), (\d+), (\d+)\)", text
    )
    if not m:
        return
    target = ".".join(m.groups())
    settings_text = settings.read_text(encoding="utf-8")
    cur = re.search(r'id\("org\.jetbrains\.kotlin\.android"\) version "([\d.]+)"', settings_text)
    if not cur or _version_tuple(cur.group(1)) >= _version_tuple(target):
        return
    settings.write_text(settings_text.replace(cur.group(0), cur.group(0).replace(cur.group(1), target)), encoding="utf-8")
    if app_gradle.exists():
        app_text = re.sub(r"(org\.jetbrains\.kotlin:kotlin-stdlib:)[\d.]+", rf"\g<1>{target}", app_gradle.read_text(encoding="utf-8"))
        legacy = re.search(r"\n\s*kotlinOptions \{\s*jvmTarget = JavaVersion\.VERSION_(\d+)\.toString\(\)\s*\}\n", app_text)
        if legacy:
            app_text = app_text.replace(legacy.group(0), "\n")
            app_text = app_text.rstrip("\n") + (
                "\n\nkotlin {\n    compilerOptions {\n"
                f"        jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_{legacy.group(1)})\n"
                "    }\n}\n"
            )
        app_gradle.write_text(app_text, encoding="utf-8")
    info(f"android: Kotlin Gradle plugin {cur.group(1)} -> {target} (Flutter SDK minimum)")


def remove_starter_code(root: Path, dry: bool) -> None:
    step("Remove the Very Good counter demo")
    for rel in ("lib/counter", "test/counter", "test/app", "lib/l10n/arb/app_es.arb",
                "lib/l10n/gen", ".github/workflows/main.yaml"):
        path = root / rel
        if path.exists():
            info(f"remove {rel}")
            if not dry:
                shutil.rmtree(path) if path.is_dir() else path.unlink()


def write_shell(a: Dict, root: Path, values: Dict[str, str], dry: bool) -> None:
    step("Core abstractions, app shell and tests")
    selected = (a["state"], a["network"], a["router"])
    render_tree(TEMPLATES / "lib", root / "lib", values, selected=selected, dry_run=dry)
    render_tree(TEMPLATES / "test", root / "test", values, selected=selected, dry_run=dry)
    # Keep only the chosen crash adapter (console is always kept for tests).
    for _, (file, _) in CRASH_CTOR.items():
        if file not in ("console_crash_reporter.dart", CRASH_CTOR[a["crash"]][0]):
            path = root / "lib/core/error_reporting" / file
            if path.exists() and not dry:
                path.unlink()
    # One entrypoint per flavor; drop the template itself.
    template = root / "lib/main_flavor.dart"
    if not dry:
        text = template.read_text(encoding="utf-8")
        template.unlink()
        for flavor in a["flavors"]:
            out = (
                text.replace("{{flavor_camel}}", camel(flavor))
                .replace("{{flavor_suffix}}", FLAVOR_SUFFIX.get(flavor, f" [{flavor.upper()}]"))
                .replace("{{base_url}}", a["base_urls"][flavor])
            )
            (root / f"lib/main_{flavor}.dart").write_text(out, encoding="utf-8")
            info(f"write  lib/main_{flavor}.dart ({a['base_urls'][flavor]})")
    if a["flavors"] != DEFAULT_FLAVORS:
        warn(
            "Custom flavors: Dart entrypoints were generated, but Very Good CLI only "
            "configures development/staging/production natively. Add matching Android "
            "productFlavors and iOS schemes/configurations by hand, and update the "
            "branch -> flavor maps in .github/workflows/*.yml."
        )


def write_locales(a: Dict, root: Path, dry: bool) -> None:
    """One ARB per extra locale, seeded with the English strings so gen-l10n
    passes until translators replace them, and the iOS locale list to match."""
    extra = a["locales"][1:]
    if extra:
        step(f"Locales: {', '.join(a['locales'])}")
    if dry:
        return
    template = root / ARB_DIR / f"app_{TEMPLATE_LOCALE}.arb"
    data = json.loads(template.read_text(encoding="utf-8"))
    for locale in extra:
        arb = root / ARB_DIR / f"app_{locale}.arb"
        arb.write_text(json.dumps({**data, "@@locale": locale}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        info(f"write  {arb.relative_to(root)} (English placeholders, needs translation)")
    plist = root / "ios/Runner/Info.plist"
    if plist.exists():
        text = plist.read_text(encoding="utf-8")
        entries = "".join(f"\t\t<string>{l}</string>\n" for l in a["locales"])
        new = re.sub(
            r"(<key>CFBundleLocalizations</key>\s*<array>\n).*?(\s*</array>)",
            lambda m: m.group(1) + entries.rstrip("\n") + m.group(2),
            text,
            count=1,
            flags=re.DOTALL,
        )
        plist.write_text(new, encoding="utf-8")


def write_home(a: Dict, root: Path, values: Dict[str, str], dry: bool) -> None:
    step("Home feature")
    render_tree(TEMPLATES / "feature/home", root, values, dry_run=dry)
    if dry:
        return
    router = root / "lib/core/routing/app_router.dart"
    if a["router"] != "auto_route":
        insert_before_marker(router, "scaffold:imports", f"import 'package:{values['package']}/features/home/home.dart';")
    insert_before_marker(router, "scaffold:route-paths", "static const home = '/';")
    insert_before_marker(router, "scaffold:routes", route_entry(a["router"], "home", "HomeScreen"))


def write_assets(root: Path, dry: bool) -> None:
    """Declare the image folders in pubspec.yaml. The folders themselves and
    the resolver come from templates/project and templates/lib."""
    step("Asset resolver")
    pubspec = root / "pubspec.yaml"
    if dry or not pubspec.exists():
        return
    text = pubspec.read_text(encoding="utf-8")
    missing = [d for d in ASSET_DIRS if f"- {d}" not in text]
    if not missing:
        return
    entries = "".join(f"    - {d}\n" for d in missing)
    if re.search(r"^  assets:\s*$", text, re.MULTILINE):
        text = re.sub(r"^(  assets:[ \t]*\n)", lambda m: m.group(1) + entries, text, count=1, flags=re.MULTILINE)
    elif re.search(r"^flutter:\s*$", text, re.MULTILINE):
        text = re.sub(r"^(flutter:[ \t]*\n)", lambda m: m.group(1) + "  assets:\n" + entries, text, count=1, flags=re.MULTILINE)
    else:
        text = text.rstrip("\n") + "\n\nflutter:\n  assets:\n" + entries
    pubspec.write_text(text, encoding="utf-8")
    info(f"pubspec.yaml assets: {', '.join(missing)}")


def configure_dependencies(a: Dict, root: Path) -> None:
    step("Dependencies")
    fl = flutter_cmd(root)
    deps = (
        COMMON_DEPS
        + NETWORK_DEPS[a["network"]]
        + ROUTER_DEPS[a["router"]]
        + (BLOC_DEPS if a["state"] == "bloc" else RIVERPOD_DEPS)
        + CRASH_DEPS[a["crash"]]
    )
    run([*fl, "pub", "add", *deps], root, quiet=True)
    if a["state"] == "riverpod":
        pubspec = (root / "pubspec.yaml").read_text(encoding="utf-8")
        bloc_pkgs = [p for p in ("bloc", "flutter_bloc", "bloc_test", "bloc_lint", "bloc_tools")
                     if re.search(rf"^\s+{p}:", pubspec, re.MULTILINE)]
        if bloc_pkgs:
            run([*fl, "pub", "remove", *bloc_pkgs], root, quiet=True)
        analysis = root / "analysis_options.yaml"
        analysis.write_text(
            "\n".join(l for l in analysis.read_text(encoding="utf-8").splitlines() if "bloc_lint" not in l) + "\n",
            encoding="utf-8",
        )
    # The shell uses package:flutter/material.dart; drop Very Good's material_ui
    # copy if nothing imports it any more (mixing both breaks Theme lookups).
    uses_material_ui = any(
        "package:material_ui/" in p.read_text(encoding="utf-8")
        for d in ("lib", "test") for p in (root / d).rglob("*.dart")
    )
    if not uses_material_ui and "material_ui:" in (root / "pubspec.yaml").read_text(encoding="utf-8"):
        run([*fl, "pub", "remove", "material_ui"], root, quiet=True)


def raise_android_min_sdk(root: Path, minimum: int) -> None:
    gradle = root / "android/app/build.gradle.kts"
    if minimum <= 0 or not gradle.exists():
        return
    text = gradle.read_text(encoding="utf-8")
    new = text.replace("minSdk = flutter.minSdkVersion", f"minSdk = maxOf(flutter.minSdkVersion, {minimum})")
    if new != text:
        gradle.write_text(new, encoding="utf-8")
        info(f"android: minSdk >= {minimum} (required by the crash-reporting SDK)")


def write_project_files(a: Dict, root: Path, values: Dict[str, str], dry: bool) -> None:
    step(f"Scripts, docs and CI/CD ({a['ci']})")
    written = render_tree(TEMPLATES / "project", root, values, dry_run=dry)
    if a["ci"] != "none":
        written += render_tree(TEMPLATES / "ci" / a["ci"], root, values, dry_run=dry)
    elif not dry:
        # "none" means no pipelines at all, including Very Good CLI's own.
        shutil.rmtree(root / ".github/workflows", ignore_errors=True)
    if "ios" not in a["platforms"] and not dry:
        for rel in (".github/workflows/ios.yml", "ios/fastlane", "ios/Gemfile"):
            path = root / rel
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
    if "android" not in a["platforms"] and not dry:
        (root / ".github/workflows/android.yml").unlink(missing_ok=True)
    # figma-token-map lives at the project root.
    src = root / "design/figma-token-map.md"
    if src.exists() and not dry:
        src.replace(root / "figma-token-map.md")
        src.parent.rmdir()
    gitignore = root / ".gitignore"
    if gitignore.exists() and not dry:
        text = gitignore.read_text(encoding="utf-8")
        extra = ["", "# flutter-kickstart", "ios/fastlane/report.xml", "ios/fastlane/README.md", "coverage/"]
        if "# flutter-kickstart" not in text:
            gitignore.write_text(text.rstrip("\n") + "\n" + "\n".join(extra) + "\n", encoding="utf-8")
    info(f"{len(written)} files")


def crash_doc_values(crash: str) -> Dict[str, str]:
    if crash == "sentry":
        return {
            "crash_secrets": "| `SENTRY_DSN`, `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT` | Sentry events and symbol upload |",
            "crash_setup": (
                "Sentry is wired in `lib/core/error_reporting/sentry_crash_reporter.dart` and stays a no-op "
                "until a DSN is passed: `--dart-define=SENTRY_DSN=...` locally, the `SENTRY_DSN` secret in CI."
            ),
        }
    if crash == "crashlytics":
        return {
            "crash_secrets": "| `FIREBASE_TOKEN`, `FIREBASE_APP_ID_IOS` | Crashlytics symbol upload |",
            "crash_setup": (
                "Crashlytics is wired in `lib/core/error_reporting/crashlytics_crash_reporter.dart` but needs "
                "Firebase configured per flavor first. Run `flutterfire configure` once per flavor (one Firebase "
                "app per application id above) and commit the generated config; until then the reporter logs a "
                "warning and does nothing."
            ),
        }
    return {
        "crash_secrets": "",
        "crash_setup": (
            "No backend was chosen: `ConsoleCrashReporter` logs errors locally. To add one, implement "
            "`CrashReporter` next to it in `lib/core/error_reporting/` and construct it in `lib/bootstrap.dart`."
        ),
    }


def line_coverage(lcov: Path) -> float:
    """Percent of lines hit in an lcov report, skipping COVERAGE_EXCLUDES."""
    found = hit = 0
    skip = False
    for line in lcov.read_text(encoding="utf-8").splitlines():
        if line.startswith("SF:"):
            skip = any(fnmatch.fnmatch(line[3:], pattern) for pattern in COVERAGE_EXCLUDES)
        elif not skip and line.startswith("LF:"):
            found += int(line[3:])
        elif not skip and line.startswith("LH:"):
            hit += int(line[3:])
    return hit * 100 / found if found else 100.0


def codegen_and_verify(a: Dict, root: Path) -> None:
    step("Code generation")
    fl, da = flutter_cmd(root), dart_cmd(root)
    run([*fl, "gen-l10n"], root, quiet=True)
    run([*da, "run", "build_runner", "build", "--delete-conflicting-outputs"], root, quiet=True)
    step("Format")
    safe_fix(root)
    run([*da, "format", "lib", "test"], root, quiet=True)
    if a["skip_verify"]:
        warn("Skipped analyze/test (--skip-verify).")
        return
    step("Verify")
    run([*fl, "analyze"], root)
    run([*fl, "test", "--coverage"], root)
    coverage = line_coverage(root / "coverage/lcov.info")
    if coverage < a["coverage_floor"]:
        fail(f"Line coverage {coverage:.1f}% is below the {a['coverage_floor']}% floor.")
    info(f"line coverage {coverage:.1f}% (floor {a['coverage_floor']}%)")


def summary(a: Dict, root: Path, ids: Dict[str, str]) -> None:
    flavors = a["flavors"]
    print(f"""
==========================================================================
{a['app_name']} is ready at {root}

  State management : {a['state']}
  Network          : {API_CLIENTS[a['network']][1]} ({NETWORK_LABELS[a['network']]})
  Navigation       : {ROUTER_LABELS[a['router']]}
  Locales          : {', '.join(a['locales'])}
  CI/CD            : {a['ci']}
  Flavors          : {', '.join(flavors)}
  Features         : home{''.join(', ' + f for f in a['features'])}
  Crash reporting  : {a['crash']}
  AI agents        : {', '.join(a['agents'])}  (AGENTS.md + .agents/skills)

Run it:
  cd {root.name}
  flutter run --flavor {flavors[0]} -t lib/main_{flavors[0]}.dart

Still needs a human{' (see docs/deployment-setup.md)' if a['ci'] == 'github' else ''}:
  - {'GitHub secrets for signing and store upload; Android keystore; iOS team/certs' if a['ci'] == 'github' else 'CI/CD: none generated; run ./scripts/quality_gate.sh in whatever CI you use'}
  - Real API base URLs if the defaults in lib/main_<flavor>.dart are placeholders
  - {'Sentry DSN' if a['crash'] == 'sentry' else '`flutterfire configure` per flavor' if a['crash'] == 'crashlytics' else 'A crash-reporting backend (ConsoleCrashReporter for now)'}
{'  - Translations for ' + ', '.join(a['locales'][1:]) + ' (lib/l10n/arb/)' + chr(10) if a['locales'][1:] else ''}  - Figma link in figma-token-map.md when design work starts{'' if not a.get('figma_url') else ' (already set)'}
  - App icons and splash screen
==========================================================================""")


def main() -> None:
    a = normalize(parse_args())
    out_dir = Path(a["output_dir"]).expanduser().resolve()
    root = out_dir / a["name"]
    dry = a["dry_run"]

    step("Plan")
    for key in ("name", "app_name", "org", "platforms", "state", "network", "router", "flavors", "base_urls",
                "locales", "features", "crash", "ci", "agents"):
        info(f"{key:10}: {a[key]}")
    info(f"{'project':10}: {root}")
    if dry:
        info("(dry run: nothing will be written)")
        if not root.exists():
            return

    if not dry:
        create_base(a, root)
    fl = flutter_cmd(root) if root.exists() else ["flutter"]
    ids = read_ids(root, a)
    values = {
        "package": a["name"],
        "app_name": a["app_name"],
        "description": a["description"] or f"{a['app_name']} Flutter app.",
        "org": a["org"],
        "flavor_enum_values": "\n".join(f"  {camel(f)}," for f in a["flavors"]),
        "crash": a["crash"],
        "crash_import": f"import 'package:{a['name']}/core/error_reporting/{CRASH_CTOR[a['crash']][0]}';",
        "crash_ctor": CRASH_CTOR[a["crash"]][1],
        "api_client_import": f"import 'package:{a['name']}/core/network/{API_CLIENTS[a['network']][0]}';",
        "api_client_class": API_CLIENTS[a["network"]][1],
        "flutter_version": flutter_version(root) if root.exists() else "3.x",
        "coverage_floor": str(a["coverage_floor"]),
        "coverage_exclude": " ".join(COVERAGE_EXCLUDES),
        "figma_url": a.get("figma_url") or "_not set yet: add the Figma file link when design work starts_",
        **ids,
        **crash_doc_values(a["crash"]),
        **router_values(a["router"]),
    }

    remove_starter_code(root, dry)
    if not dry:
        align_android_kotlin(root)
    write_shell(a, root, values, dry)
    write_locales(a, root, dry)
    write_home(a, root, values, dry)
    write_project_files(a, root, values, dry)
    write_assets(root, dry)
    if dry:
        return

    configure_dependencies(a, root)
    raise_android_min_sdk(root, CRASH_MIN_SDK[a["crash"]])
    for feature in a["features"]:
        add_feature.generate(root, feature, state=a["state"], router=a["router"])

    ai_values = setup_ai.build_values(
        root,
        state=a["state"],
        network=a["network"],
        router=a["router"],
        ci=a["ci"],
        app_name=a["app_name"],
        description=values["description"],
        application_id=ids["android_id"],
        flavors=a["flavors"],
        crash=a["crash"],
        uses_fvm=fl[0] == "fvm",
    )
    setup_ai.install(root, ai_values, state=a["state"], ci=a["ci"], agents=a["agents"], copy=a["copy_skills"])

    codegen_and_verify(a, root)
    summary(a, root, ids)


if __name__ == "__main__":
    main()
