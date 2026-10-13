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
    variant: Optional[str] = None,
    variants: Iterable[str] = ("bloc", "riverpod"),
) -> List[Path]:
    """Copy every file under src_root into dest_root, rendering `{{key}}`
    placeholders. `.tmpl` is dropped from file names; `__token__` path parts
    are replaced from path_tokens. Files named `x.<variant>.ext.tmpl` are only
    copied for the matching variant (and lose the `.<variant>` part)."""
    written: List[Path] = []
    path_tokens = path_tokens or {}
    variants = tuple(variants)
    for src in sorted(src_root.rglob("*")):
        if src.is_dir() or src.name == ".DS_Store":
            continue
        rel = src.relative_to(src_root).as_posix()
        for token, value in path_tokens.items():
            rel = rel.replace(f"__{token}__", value)
        if rel.endswith(".tmpl"):
            rel = rel[: -len(".tmpl")]
        skip = False
        for v in variants:
            marker = f".{v}."
            if marker in Path(rel).name:
                if v != variant:
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


def add_arb_strings(arb: Path, strings: Dict[str, str], dry_run: bool = False) -> None:
    if not arb.exists():
        warn(f"{arb} not found; add these l10n keys by hand: {strings}")
        return
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


def detect_state_management(root: Path) -> str:
    text = (root / "pubspec.yaml").read_text(encoding="utf-8")
    if re.search(r"^\s+flutter_riverpod:", text, re.MULTILINE):
        return "riverpod"
    return "bloc"


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
