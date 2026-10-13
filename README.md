# Flutter Kickstart

Turns "start a new Flutter app" into one short interview and a verified,
production-ready codebase. Works with **Claude Code, Cursor, Windsurf,
Antigravity, Codex, Gemini CLI and GitHub Copilot**.

The interview drives a deterministic generator (`scripts/scaffold.py`), so
every agent produces the same project. The result has to pass
`flutter analyze` and `flutter test` before the run reports success.

## What you get

| Area | Generated |
| --- | --- |
| Base | Very Good CLI app: native dev/staging/prod flavors, very_good_analysis, l10n |
| Architecture | `lib/core/` contracts + `lib/features/<name>/{domain,data,presentation}` |
| State | **Bloc/Cubit** (get_it + injectable) or **Riverpod** (riverpod_generator), asked every time |
| Network | `AppApiClient` contract on **viva_network_kit** or **plain Dio** (asked), sealed `AppFailure`, `Either` everywhere, auth + logging interceptors |
| Shell | go_router (`AppRoutes`), Material 3 light/dark theme + `AppColors`/`AppSpacing`/`AppRadius`, `AppLogger`, `CrashReporter` (console, Sentry or Crashlytics), per-flavor `AppConfig` with `--dart-define` overrides |
| Features | `home` + any starter features, each with all layers, DI, route, l10n and tests |
| Tests | Unit, bloc/controller and widget tests; `scripts/quality_gate.sh` |
| CI/CD | Optional (`--ci github\|none`): GitHub Actions `pr_checks` (coverage gate), `android` (sign, Firebase App Distribution, Play internal), `ios` (Fastlane, TestFlight/App Store), symbol upload, `docs/deployment-setup.md` |
| AI layer | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, 10 project skills, Cursor + Windsurf rules, Copilot instructions, Claude reviewer subagents, and `tool/kickstart/add_feature.py` so the app can grow without the plugin |

## Install

### Claude Code (plugin)

```text
/plugin marketplace add alamin-karno/flutter-kickstart
/plugin install flutter-kickstart@flutter-kickstart
```

### Every agent at once (skills)

```bash
git clone https://github.com/alamin-karno/flutter-kickstart.git ~/flutter-kickstart
~/flutter-kickstart/install.sh          # symlinks; `git pull` updates them
~/flutter-kickstart/install.sh --copy   # for agents that ignore symlinks
~/flutter-kickstart/install.sh --uninstall
```

On Windows: `powershell -ExecutionPolicy Bypass -File install.ps1`.

The installer links `skills/flutter-kickstart` and `skills/flutter-figma-to-flutter` into:

| Agent | Global skills folder |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/`, `~/.agents/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |
| Antigravity | `~/.gemini/config/skills/`, `~/.gemini/antigravity/skills/` |
| Codex | `~/.codex/skills/`, `~/.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/`, `~/.agents/skills/` |

Agents without skill support: tell the agent *"Read
`~/flutter-kickstart/skills/flutter-kickstart/SKILL.md` and follow
it."*

Start a **new** agent session after installing.

### Prerequisites

Flutter (or [fvm](https://fvm.app)), `python3` (3.8+), network access for
`pub get`. Very Good CLI is activated automatically if missing. For iOS:
macOS + Xcode.

## Use

Ask in plain words, for example:

- *"Create a new Flutter app called Acme Wallet for com.acme."*
- *"Add an orders feature that loads `/v1/orders`."* (inside a generated app)
- *"Implement this Figma frame: <link>"* (needs a Figma MCP server)

Or run the generator yourself:

```bash
python3 skills/flutter-kickstart/scripts/scaffold.py \
  --name acme_wallet --app-name "Acme Wallet" --org com.acme \
  --platforms android,ios --state bloc --network viva \
  --base-url development=https://dev.api.acme.com \
  --base-url staging=https://stg.api.acme.com \
  --base-url production=https://api.acme.com \
  --features auth,orders --locales en,bn --crash sentry --ci github --agents all
```

`--config answers.json` takes the same keys. `--dry-run` prints the plan.

Inside a generated app:

```bash
python3 tool/kickstart/add_feature.py --name orders [--entity order] [--endpoint /v1/orders]
./scripts/quality_gate.sh
```

## How the AI layer works in a generated app

```
AGENTS.md                      canonical rules (Cursor, Windsurf, Antigravity, Codex, Copilot read it natively)
CLAUDE.md, GEMINI.md           one line each: @AGENTS.md
.agents/skills/<skill>/        canonical project skills
.claude/skills  -> .agents/skills
.cursor/skills  -> .agents/skills
.windsurf/skills -> .agents/skills
.cursor/rules/flutter-architecture.mdc     glob rule for lib/**/*.dart
.windsurf/rules/flutter-architecture.md    glob rule for lib/**/*.dart
.github/copilot-instructions.md
.claude/agents/{architecture,test}-reviewer.md
```

Edit `.agents/skills/` and `AGENTS.md` only; every tool sees the change.
`--copy-skills` (or Windows) writes real copies instead of symlinks.
Refresh the layer later with `python3 skills/flutter-kickstart/scripts/setup_ai.py --root <app>`.

## Layout

```
.claude-plugin/{plugin,marketplace}.json   Claude Code plugin + marketplace
skills/
  flutter-kickstart/
    SKILL.md                               interview + how to run the generator
    scripts/scaffold.py                    full project generator
    scripts/add_feature.py                 feature generator (also vendored into apps)
    scripts/setup_ai.py                    cross-agent AI layer installer
    templates/lib, test                    core + app shell (Dart)
    templates/feature/{common,bloc,riverpod,home}
    templates/project                      CI/CD, Fastlane, scripts, docs
    templates/ai                           AGENTS.md, rules, project skills, subagents
  flutter-figma-to-flutter/SKILL.md        design-to-code
install.sh, install.ps1                    multi-agent installers
docs/                                      plan, comparison with app-team-agent-skills
```

## Changing the templates

1. Edit under `skills/flutter-kickstart/templates/` or `scripts/`.
2. Regenerate both variants and make sure they pass:
   ```bash
   cd /tmp && python3 <repo>/skills/flutter-kickstart/scripts/scaffold.py --name demo_bloc --org com.acme --state bloc --features orders --crash sentry
   cd /tmp && python3 <repo>/skills/flutter-kickstart/scripts/scaffold.py --name demo_rp --org com.acme --state riverpod --features orders --crash crashlytics
   ```
3. Bump `version` in `.claude-plugin/plugin.json` and run `claude plugin validate .`.

## License

[MIT](LICENSE) © Md. Al-Amin
