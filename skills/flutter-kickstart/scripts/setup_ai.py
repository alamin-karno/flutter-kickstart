#!/usr/bin/env python3
"""Install the AI-agent layer into a Flutter project created by flutter-kickstart.

One source of truth, read by every supported agent:

    AGENTS.md                      Cursor, Windsurf/Devin, Antigravity, Codex, Copilot, Gemini CLI
    CLAUDE.md -> @AGENTS.md        Claude Code
    GEMINI.md -> @AGENTS.md        Gemini CLI (and Antigravity's GEMINI.md lookup)
    .agents/skills/<skill>/        canonical skills (Antigravity, Codex, Cursor, Gemini CLI, Devin)
    .claude/skills   -> .agents/skills   (Claude Code)
    .cursor/skills   -> .agents/skills   (Cursor)
    .windsurf/skills -> .agents/skills   (Windsurf)
    .claude/agents/                Claude Code reviewer subagents
    .cursor/rules/*.mdc            Cursor glob rule for Dart files
    .windsurf/rules/*.md           Windsurf glob rule for Dart files
    .github/copilot-instructions.md
    tool/kickstart/                 add_feature.py + feature templates (no plugin needed later)

    python3 setup_ai.py --root . [--agents all|claude,cursor,...] [--copy]
        [--router go_router|auto_route|navigator]

Re-running refreshes everything this script owns and leaves other files alone.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Iterable, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    API_CLIENTS,
    CI_CHOICES,
    NETWORK_CHOICES,
    NETWORK_LABELS,
    ROUTER_CHOICES,
    SKILL_DIR,
    STATE_CHOICES,
    TEMPLATES,
    detect_network,
    detect_router,
    detect_state_management,
    fail,
    info,
    read_package_name,
    render,
    render_tree,
    router_values,
    step,
    title,
    warn,
)

AGENTS = ("claude", "cursor", "windsurf", "antigravity", "codex", "gemini", "copilot")
# Agents that need a mirror of .agents/skills in their own folder.
MIRRORS = {"claude": ".claude/skills", "cursor": ".cursor/skills", "windsurf": ".windsurf/skills"}
CRASH_LABELS = {"none": "console only (no backend yet)", "sentry": "Sentry", "crashlytics": "Firebase Crashlytics"}
# Skills that only make sense when CI/CD was generated.
CI_ONLY_SKILLS = {"flutter-deployment"}
# Skills shipped in one variant per setup answer: `<prefix><choice>` is
# installed as `<prefix without the trailing dash>`.
VARIANT_SKILLS = ("flutter-state-management-", "flutter-navigation-")


def network_values(network: str) -> Dict[str, str]:
    packages = "`dio` or `viva_network_kit`" if network == "viva" else "`dio`"
    return {
        "network_label": NETWORK_LABELS[network],
        "network_packages": packages,
        "api_client_class": API_CLIENTS[network][1],
    }


def ci_values(ci: str) -> Dict[str, str]:
    if ci == "none":
        return {
            "deployment_skill_row": "",
            "coverage_enforcement": "No CI was generated; enforce the coverage floor in your CI.",
        }
    return {
        "deployment_skill_row": "| `flutter-deployment` | CI workflows, signing, Fastlane, releases |\n",
        "coverage_enforcement": "The coverage floor is enforced in `.github/workflows/pr_checks.yml`.",
    }


def state_values(state: str) -> Dict[str, str]:
    if state == "riverpod":
        return {
            "state_label": "Riverpod (flutter_riverpod + riverpod_generator)",
            "codegen_note": "@riverpod controllers",
            "di_summary": "providers.dart: the provider graph is the DI graph",
            "presentation_state": "@riverpod controllers",
            "feature_di_file": "providers",
            "presentation_dirs": "controllers/<feature>_controller.dart   @riverpod AsyncNotifier + sealed state",
            "state_rule": (
                "State lives in `@riverpod` controllers returning a sealed state; "
                "expected failures are a state value, not a thrown error. No `setState` "
                "for feature state, no Bloc, no `get_it`."
            ),
            "state_test_row": (
                "Riverpod controller | `ProviderContainer` test overriding the use-case "
                "provider: loading, success, one `AppFailure` path per method"
            ),
            "review_state_check": (
                "controllers are `@riverpod` classes with a sealed state; no `ref.watch` "
                "inside callbacks; no `setState` for feature state; implementations are "
                "only named in `*_providers.dart`."
            ),
            "test_review_state_check": (
                "Riverpod controller -> a `ProviderContainer` test covering loading, "
                "success and one `AppFailure` path per public method."
            ),
        }
    return {
        "state_label": "Bloc / Cubit (flutter_bloc, get_it + injectable)",
        "codegen_note": "injectable modules",
        "di_summary": "injector.dart (get_it + injectable), register_module.dart",
        "presentation_state": "Cubits",
        "feature_di_file": "module",
        "presentation_dirs": "cubit/<feature>_cubit.dart + <feature>_state.dart   sealed states",
        "state_rule": (
            "State lives in Cubits (or Blocs) with sealed state classes; error states "
            "carry the `AppFailure`. No `setState` for feature state, no Riverpod."
        ),
        "state_test_row": (
            "Cubit / Bloc | `bloc_test`: initial state, success, one `AppFailure` path "
            "per method or event"
        ),
        "review_state_check": (
            "Cubits/Blocs use sealed states, take use cases via the constructor, are "
            "registered in the feature's `*_module.dart`, and are created only in "
            "screen-level `BlocProvider`; no `setState` for feature state."
        ),
        "test_review_state_check": (
            "Cubit/Bloc -> a `bloc_test` suite covering the initial state, success "
            "and one `AppFailure` path per public method or event."
        ),
    }


def navigation_values(router: str) -> Dict[str, str]:
    values = router_values(router)
    if router == "auto_route":
        values.update({
            "app_widget": "MaterialApp.router",
            "routing_summary": "AppRoutes + AppRouter (auto_route; app_router.gr.dart is generated)",
            "navigation_rule": (
                "Navigation: the generated typed route, `context.router.push(const OrdersRoute())`.\n"
                "   Screens carry `@RoutePage()`. Never `Navigator.push` or a raw path string."
            ),
            "navigation_rule_short": "Navigate with typed routes, `context.router.push(const XRoute())`; never `Navigator.push`.",
        })
    elif router == "navigator":
        values.update({
            "app_widget": "MaterialApp",
            "routing_summary": "AppRoutes + onGenerateAppRoute (Flutter Navigator, named routes)",
            "navigation_rule": (
                "Navigation: `Navigator.of(context).pushNamed(AppRoutes.x)` with a constant\n"
                "   from `AppRoutes`. Never a raw route string or a `MaterialPageRoute` built in a widget."
            ),
            "navigation_rule_short": "Navigate with `Navigator.of(context).pushNamed(AppRoutes.x)`; never build routes in widgets.",
        })
    else:
        values.update({
            "app_widget": "MaterialApp.router",
            "routing_summary": "AppRoutes + buildAppRouter (go_router)",
            "navigation_rule": (
                "Navigation: `context.push(AppRoutes.x)` / `context.go(...)` with a\n"
                "   constant from `AppRoutes`. Never `Navigator.push` or a raw path string."
            ),
            "navigation_rule_short": "Navigate with `context.push(AppRoutes.x)`; never `Navigator.push`.",
        })
    return values


def build_values(root: Path, *, state: str, network: str, router: str, ci: str, app_name: str, description: str,
                 application_id: str, flavors: Iterable[str], crash: str, uses_fvm: bool) -> Dict[str, str]:
    values = {
        "package": read_package_name(root),
        "app_name": app_name,
        "description": description,
        "application_id": application_id,
        "crash_label": CRASH_LABELS.get(crash, crash),
        "flavor_list": ", ".join(f"`{f}`" for f in flavors),
        "flutter": "fvm flutter" if uses_fvm else "flutter",
        "dart": "fvm dart" if uses_fvm else "dart",
    }
    values.update(state_values(state))
    values.update(network_values(network))
    values.update(navigation_values(router))
    values.update(ci_values(ci))
    return values


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    info(f"write  {path}")


def render_file(src: Path, dest: Path, values: Dict[str, str]) -> None:
    write(dest, render(src.read_text(encoding="utf-8"), values))


def install_skills(root: Path, values: Dict[str, str], state: str, ci: str) -> List[str]:
    """Render project skills into .agents/skills (canonical)."""
    canonical = root / ".agents/skills"
    names: List[str] = []
    for skill_dir in sorted((TEMPLATES / "ai/skills").iterdir()):
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name
        if ci == "none" and name in CI_ONLY_SKILLS:
            shutil.rmtree(canonical / name, ignore_errors=True)
            continue
        prefix = next((p for p in VARIANT_SKILLS if name.startswith(p)), None)
        if prefix:
            if name[len(prefix):] not in (state, values["router"]):
                continue
            name = prefix.rstrip("-")
        dest = canonical / name
        if dest.exists():
            shutil.rmtree(dest)
        render_tree(skill_dir, dest, values)
        names.append(name)
    # The design-to-code skill ships with the plugin; vendor it so every agent has it.
    figma = SKILL_DIR.parent / "flutter-figma-to-flutter"
    if figma.is_dir():
        dest = canonical / "flutter-figma-to-flutter"
        if dest.exists():
            shutil.rmtree(dest)
        render_tree(figma, dest, values)
        names.append("flutter-figma-to-flutter")
    info(f"skills {', '.join(names)} -> .agents/skills/")
    return names


def mirror_skills(root: Path, rel: str, names: List[str], copy: bool) -> None:
    target = root / rel
    source = root / ".agents/skills"
    if target.is_symlink():
        target.unlink()
    if not copy and not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(os.path.relpath(source, target.parent), target_is_directory=True)
        info(f"link   {rel} -> .agents/skills")
        return
    # Real folder (copy mode, or the team already keeps other skills there):
    # refresh only the skills this script owns.
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        dest = target / name
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        elif dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(source / name, dest)
    info(f"copy   {len(names)} skills -> {rel}/")


def vendor_feature_generator(root: Path) -> None:
    """Copy add_feature.py and its templates into tool/kickstart/ so the project
    can generate features without the plugin installed."""
    dest = root / "tool/kickstart"
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "templates").mkdir(parents=True)
    for script in ("_common.py", "add_feature.py"):
        shutil.copy2(SKILL_DIR / "scripts" / script, dest / script)
    shutil.copytree(TEMPLATES / "feature", dest / "templates/feature")
    (dest / "add_feature.py").chmod(0o755)
    info("vendor tool/kickstart/add_feature.py (+ templates/feature)")


def install(root: Path, values: Dict[str, str], *, state: str, ci: str, agents: Iterable[str], copy: bool) -> None:
    agents = set(agents)
    ai = TEMPLATES / "ai"
    step(f"AI agent layer for: {', '.join(sorted(agents))}")

    render_file(ai / "AGENTS.md.tmpl", root / "AGENTS.md", values)
    names = install_skills(root, values, state, ci)
    vendor_feature_generator(root)

    for agent, rel in MIRRORS.items():
        if agent in agents:
            mirror_skills(root, rel, names, copy)
    if "claude" in agents:
        render_file(ai / "CLAUDE.md.tmpl", root / "CLAUDE.md", values)
        for agent_file in sorted((ai / "agents").glob("*.md")):
            render_file(agent_file, root / ".claude/agents" / agent_file.name, values)
    if "gemini" in agents:
        render_file(ai / "GEMINI.md.tmpl", root / "GEMINI.md", values)
    if "cursor" in agents:
        render_file(ai / "rules/cursor.mdc.tmpl", root / ".cursor/rules/flutter-architecture.mdc", values)
    if "windsurf" in agents:
        render_file(ai / "rules/windsurf.md.tmpl", root / ".windsurf/rules/flutter-architecture.md", values)
    if "copilot" in agents:
        render_file(ai / "rules/copilot-instructions.md.tmpl", root / ".github/copilot-instructions.md", values)


def parse_agents(value: str) -> List[str]:
    if value.strip().lower() == "all":
        return list(AGENTS)
    chosen = [a.strip().lower() for a in value.split(",") if a.strip()]
    unknown = [a for a in chosen if a not in AGENTS]
    if unknown:
        fail(f"Unknown agent(s) {unknown}. Choose from: {', '.join(AGENTS)} or 'all'.")
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".")
    parser.add_argument("--agents", default="all", help=f"'all' or comma list of: {', '.join(AGENTS)}")
    parser.add_argument("--copy", action="store_true", help="Copy skills into each agent folder instead of symlinking (default on Windows)")
    parser.add_argument("--app-name", help="Display name (default: from package name)")
    parser.add_argument("--description", default="")
    parser.add_argument("--application-id", default="")
    parser.add_argument("--state", choices=STATE_CHOICES, help="Default: detected from pubspec.yaml")
    parser.add_argument("--network", choices=NETWORK_CHOICES, help="Default: detected from pubspec.yaml")
    parser.add_argument("--router", choices=ROUTER_CHOICES, help="Default: detected from pubspec.yaml")
    parser.add_argument("--ci", choices=CI_CHOICES, help="Default: github if .github/workflows/pr_checks.yml exists")
    parser.add_argument("--crash", default="none", choices=sorted(CRASH_LABELS))
    parser.add_argument("--flavors", default="development,staging,production")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    package = read_package_name(root)
    state = args.state or detect_state_management(root)
    ci = args.ci or ("github" if (root / ".github/workflows/pr_checks.yml").exists() else "none")
    values = build_values(
        root,
        state=state,
        network=args.network or detect_network(root),
        router=args.router or detect_router(root),
        ci=ci,
        app_name=args.app_name or title(package),
        description=args.description,
        application_id=args.application_id or package,
        flavors=[f.strip() for f in args.flavors.split(",") if f.strip()],
        crash=args.crash,
        uses_fvm=(root / ".fvmrc").exists(),
    )
    install(root, values, state=state, ci=ci, agents=parse_agents(args.agents), copy=args.copy or os.name == "nt")
    if not (root / "lib/core/routing/app_router.dart").exists():
        warn("This project was not created by flutter-kickstart; add_feature.py expects its lib/core layout.")
    print("\nAI layer installed. Start a new agent session so it picks up the skills.")


if __name__ == "__main__":
    main()
