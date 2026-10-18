"""Shared helpers for the flutter-kickstart scripts. Python 3.8+, stdlib only."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional

_HERE = Path(__file__).resolve().parent
# Plugin layout: <skill>/scripts/_common.py + <skill>/templates/.
# Vendored layout (inside a generated app): tool/kickstart/_common.py + tool/kickstart/templates/.
SKILL_DIR = _HERE if (_HERE / "templates").is_dir() else _HERE.parent
TEMPLATES = SKILL_DIR / "templates"

_PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")

# Setup-question choices that swap implementations. A template named
# `x.<choice>.ext.tmpl` is rendered only when <choice> is selected.
STATE_CHOICES = ("bloc", "riverpod")
NETWORK_CHOICES = ("viva", "dio")
DEFAULT_NETWORK = "viva"
NETWORK_LABELS = {"viva": "viva_network_kit (on Dio)", "dio": "plain Dio"}
# AppApiClient implementation per network choice: (file in lib/core/network/, class).
API_CLIENTS = {"viva": ("viva_api_client.dart", "VivaApiClient"), "dio": ("dio_api_client.dart", "DioApiClient")}
CI_CHOICES = ("github", "none")
ROUTER_CHOICES = ("go_router", "auto_route", "navigator")
DEFAULT_ROUTER = "go_router"
ROUTER_LABELS = {
    "go_router": "go_router (declarative, URL-based)",
    "auto_route": "auto_route (typed routes, code generation)",
    "navigator": "Navigator (Flutter's built-in named routes, no package)",
}
_VARIANT_MARKERS = STATE_CHOICES + NETWORK_CHOICES + ROUTER_CHOICES

# Image assets live in these folders and are only referenced through
# ImageResourceResolver in lib/core/asset_resolver/.
ASSET_DIRS = ("assets/images/", "assets/icons/")


def route_entry(router: str, route: str, screen: str) -> str:
    """The snippet registered at `// scaffold:routes` for one screen."""
    if router == "auto_route":
        return f"AutoRoute(page: {screen[: -len('Screen')]}Route.page, path: AppRoutes.{route}),"
    if router == "navigator":
        return f"AppRoutes.{route} => const {screen}(),"
    return (
        f"GoRoute(\n"
        f"  path: AppRoutes.{route},\n"
        f"  name: '{route}',\n"
        f"  builder: (context, state) => const {screen}(),\n"
        f"),"
    )


def navigate_example(router: str, route: str) -> str:
    """How code links to a route, for messages and docs."""
    if router == "auto_route":
        return f"context.router.push(const {pascal(route)}Route())"
    if router == "navigator":
        return f"Navigator.of(context).pushNamed(AppRoutes.{route})"
    return f"context.push(AppRoutes.{route})"


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #

def info(msg: str) -> None:
    print(f"  {msg}", flush=True)


def step(msg: str) -> None:
    print(f"\n==> {msg}", flush=True)


def warn(msg: str) -> None:
    print(f"  WARNING: {msg}", file=sys.stderr, flush=True)


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"\nERROR: {msg}", file=sys.stderr, flush=True)
    sys.exit(1)


# --------------------------------------------------------------------------- #
# Names
# --------------------------------------------------------------------------- #

def snake(value: str) -> str:
    value = re.sub(r"[\s\-]+", "_", value.strip())
    value = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", value)
    return re.sub(r"_+", "_", value).lower().strip("_")


def pascal(value: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in snake(value).split("_"))


def camel(value: str) -> str:
    p = pascal(value)
    return p[:1].lower() + p[1:]


def title(value: str) -> str:
    return " ".join(part.capitalize() for part in snake(value).split("_"))


def singular(value: str) -> str:
    """Naive English singular, good enough for a default entity name."""
    if value.endswith("ies") and len(value) > 3:
        return value[:-3] + "y"
    if value.endswith(("ses", "xes", "zes", "ches", "shes")):
        return value[:-2]
    if value.endswith("s") and not value.endswith("ss") and len(value) > 1:
        return value[:-1]
    return value


def valid_package_name(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z][a-z0-9_]*", value))


# --------------------------------------------------------------------------- #
# Templates
# --------------------------------------------------------------------------- #

def render(text: str, values: Dict[str, str], source: str = "") -> str:
    def sub(match: "re.Match[str]") -> str:
        key = match.group(1)
        if key not in values:
            # Leave GitHub Actions `${{ ... }}` expressions and unknown keys alone.
            return match.group(0)
        return values[key]

    return _PLACEHOLDER.sub(sub, text)


def render_tree(
    src_root: Path,
    dest_root: Path,
    values: Dict[str, str],
    *,
    path_tokens: Optional[Dict[str, str]] = None,
    overwrite: bool = True,
    dry_run: bool = False,
    selected: Iterable[str] = (),
) -> List[Path]:
    """Copy every file under src_root into dest_root, rendering `{{key}}`
    placeholders. `.tmpl` is dropped from file names; `__token__` path parts
    are replaced from path_tokens. Files named `x.<choice>.ext.tmpl` are only
    copied when <choice> is in `selected` (and lose the `.<choice>` part)."""
    written: List[Path] = []
    path_tokens = path_tokens or {}
    selected = set(selected)
    for src in sorted(src_root.rglob("*")):
        if src.is_dir() or src.name == ".DS_Store":
            continue
        rel = src.relative_to(src_root).as_posix()
        for token, value in path_tokens.items():
            rel = rel.replace(f"__{token}__", value)
        if rel.endswith(".tmpl"):
            rel = rel[: -len(".tmpl")]
        skip = False
        for choice in _VARIANT_MARKERS:
            marker = f".{choice}."
            if marker in Path(rel).name:
                if choice not in selected:
                    skip = True
                rel = rel.replace(marker, ".", 1)
        if skip:
            continue
        dest = dest_root / rel
        if dest.exists() and not overwrite:
            info(f"skip   {dest.relative_to(dest_root)} (exists)")
            continue
        content = render(src.read_text(encoding="utf-8"), values, str(src))
        if dry_run:
            info(f"would write {rel}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
            if dest.suffix == ".sh":
                dest.chmod(0o755)
        written.append(dest)
    return written


def insert_before_marker(
    path: Path, marker: str, snippet: str, *, dry_run: bool = False
) -> bool:
    """Insert snippet on the line(s) before `// <marker>`, keeping the marker's
    indentation. Idempotent: does nothing if the snippet is already present.
    Returns False if the marker is missing."""
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if snippet.strip() in text:
        return True
    pattern = re.compile(rf"^([ \t]*)// {re.escape(marker)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return False
    indent = match.group(1)
    block = "".join(
        (indent + line if line.strip() else line) + "\n"
        for line in snippet.strip("\n").splitlines()
    )
    text = text[: match.start()] + block + text[match.start():]
    if not dry_run:
        path.write_text(text, encoding="utf-8")
    return True


ARB_DIR = "lib/l10n/arb"
TEMPLATE_LOCALE = "en"


def add_arb_strings(root: Path, strings: Dict[str, str], dry_run: bool = False) -> None:
    """Add missing keys to every `app_<locale>.arb`. Non-template locales get
    the English text as a placeholder until someone translates it."""
    arbs = sorted((root / ARB_DIR).glob("app_*.arb"))
    if not arbs:
        warn(f"No {ARB_DIR}/app_*.arb found; add these l10n keys by hand: {strings}")
        return
    for arb in arbs:
        data = json.loads(arb.read_text(encoding="utf-8"))
        changed = False
        for key, value in strings.items():
            if key not in data:
                data[key] = value
                data[f"@{key}"] = {"description": f"{value} (generated by flutter-kickstart)"}
                changed = True
        if changed and not dry_run:
            arb.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Project inspection
# --------------------------------------------------------------------------- #

def read_package_name(root: Path) -> str:
    pubspec = root / "pubspec.yaml"
    if not pubspec.exists():
        fail(f"No pubspec.yaml in {root}. Is this a Flutter project?")
    match = re.search(r"^name:\s*([a-z0-9_]+)", pubspec.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        fail("Could not read `name:` from pubspec.yaml")
    return match.group(1)


def _has_dependency(root: Path, package: str) -> bool:
    text = (root / "pubspec.yaml").read_text(encoding="utf-8")
    return bool(re.search(rf"^\s+{re.escape(package)}:", text, re.MULTILINE))


def detect_state_management(root: Path) -> str:
    return "riverpod" if _has_dependency(root, "flutter_riverpod") else "bloc"


def detect_network(root: Path) -> str:
    return "viva" if _has_dependency(root, "viva_network_kit") else "dio"


def detect_router(root: Path) -> str:
    if _has_dependency(root, "auto_route"):
        return "auto_route"
    return "go_router" if _has_dependency(root, "go_router") else "navigator"


def router_values(router: str) -> Dict[str, str]:
    """Placeholders that differ per router in shell, feature and AI templates."""
    auto = router == "auto_route"
    return {
        "router": router,
        "router_label": ROUTER_LABELS[router],
        # auto_route needs @RoutePage() on every routed screen.
        "route_page_import": "import 'package:auto_route/auto_route.dart';\n" if auto else "",
        "route_page_annotation": "@RoutePage()\n" if auto else "",
    }


def flutter_cmd(root: Path) -> List[str]:
    """`fvm flutter` when the project (or a parent) pins a version with fvm."""
    for d in [root, *root.parents]:
        if (d / ".fvmrc").exists() or (d / ".fvm").is_dir():
            if shutil.which("fvm"):
                return ["fvm", "flutter"]
            warn("Project uses fvm but `fvm` is not on PATH; falling back to `flutter`.")
            break
    if not shutil.which("flutter"):
        fail("`flutter` not found on PATH. Install Flutter (or fvm) first.")
    return ["flutter"]


def dart_cmd(root: Path) -> List[str]:
    return [*flutter_cmd(root)[:-1], "dart"] if flutter_cmd(root)[0] == "fvm" else ["dart"]


# Lints whose fixes only change style, never behaviour. Applied after
# generation so the output matches whatever very_good_analysis version (and
# Dart language version) the project uses, e.g. Dart 3.13's primary-constructor
# style, without hard-coding new syntax that older SDKs can't parse.
SAFE_FIX_CODES = (
    "directives_ordering",
    "unnecessary_type_name_in_constructor",
    "empty_container_bodies",
    "prefer_const_constructors",
    "prefer_const_declarations",
    "prefer_const_literals_to_create_immutables",
    "unnecessary_const",
    "unnecessary_new",
    "unnecessary_import",
    "require_trailing_commas",
    "sort_child_properties_last",
    "omit_local_variable_types",
)


def safe_fix(root: Path) -> None:
    cmd = [*dart_cmd(root), "fix", "--apply"]
    for code in SAFE_FIX_CODES:
        cmd += ["--code", code]
    run(cmd, root, quiet=True, check=False)


def run(cmd: List[str], cwd: Path, *, check: bool = True, quiet: bool = False) -> int:
    info("$ " + " ".join(cmd))
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE if quiet else None,
        stderr=subprocess.STDOUT if quiet else None,
        text=True,
        env={**os.environ, "CI": os.environ.get("CI", "")},
    )
    if check and proc.returncode != 0:
        if quiet and proc.stdout:
            print(proc.stdout[-4000:])
        fail(f"Command failed ({proc.returncode}): {' '.join(cmd)}")
    return proc.returncode
