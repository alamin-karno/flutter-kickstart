# Flutter Kickstart

Turns "start a new Flutter app" into one short interview and a verified,
production-ready codebase. Works with **Claude Code, Cursor, Windsurf,
Antigravity, Codex, Gemini CLI and GitHub Copilot**.

The interview drives a deterministic generator (`scripts/scaffold.py`), so
every agent produces the same project. The result has to pass
`flutter analyze` and `flutter test` before the run reports success.

## Quick start

```bash
# 1. Install (once)
curl -fsSL https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/main/install.sh | bash

# 2. Create an app (answer a few questions; Enter accepts the default)
fks create

# 3. Run it
cd my_app && fks run
```

Windows (PowerShell): `irm https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/main/install.ps1 | iex`

`fks` is short for **f**lutter **k**ick**s**tart, the way `fvm` is short for
Flutter Version Manager. `flutter-kickstart` works too.

| Command | What it does |
| --- | --- |
| `fks create` | Asks the interview questions, generates the app, checks it with `flutter analyze` + `flutter test` |
| `fks create --yes` | Asks only name, org and state management; uses defaults for everything else |
| `fks create --name x --org com.acme --state bloc ...` | No questions; takes the same flags as `scaffold.py` |
| `fks run [flavor]` | `flutter run --flavor <flavor> -t lib/main_<flavor>.dart` (default `development`, uses fvm if pinned) |
| `fks add-feature orders` | Adds a feature with all layers, DI, route, l10n and tests to the app in `.` |
| `fks doctor` | Checks Python, Flutter, git and Very Good CLI |
| `fks update` | Pulls the latest templates and skills |
| `fks uninstall` | Removes the command and the agent skills |

The installer also puts the skills in every AI agent's global folder, so you can
skip the CLI and just ask your agent: *"Create a new Flutter app called Acme
Wallet for com.acme."*

## What you get

| Area | Generated |
| --- | --- |
| Base | Very Good CLI app: native dev/staging/prod flavors, very_good_analysis, l10n in English plus any extra locales you pick |
| Architecture | `lib/core/` contracts + `lib/features/<name>/{domain,data,presentation}` |
| State | **Bloc/Cubit** (get_it + injectable) or **Riverpod** (riverpod_generator), asked every time |
| Network | `AppApiClient` contract backed by **viva_network_kit** (`VivaApiClient`) or **plain Dio** (`DioApiClient`), asked every time; sealed `AppFailure`, `Either` everywhere, auth + logging interceptors |
| Shell | go_router (`AppRoutes`), Material 3 light/dark theme + `AppColors`/`AppSpacing`/`AppRadius`, `AppLogger`, `CrashReporter` (console, Sentry or Crashlytics), per-flavor `AppConfig` with `--dart-define` overrides |
| Features | `home` + any starter features, each with all layers, DI, route, l10n and tests |
| Tests | Unit, DI, bloc/controller and widget tests (~95% line coverage), `AppApiClient` contract tests that run against either client, `scripts/quality_gate.sh` |
| CI/CD | Optional (`--ci github\|none`): GitHub Actions `pr_checks` (coverage gate), `android` (sign, Firebase App Distribution, Play internal), `ios` (Fastlane, TestFlight/App Store), symbol upload, `docs/deployment-setup.md` |
| AI layer | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, 10 project skills, Cursor + Windsurf rules, Copilot instructions, Claude reviewer subagents, and `tool/kickstart/add_feature.py` so the app can grow without the plugin |

## The interview

The skill asks these one at a time, then reads the answers back before
generating. Each answer maps to a `scaffold.py` flag.

| # | Question | Flag | Default |
| - | --- | --- | --- |
| 1 | App display name and description | `--app-name`, `--description` | from `--name` |
| 2 | Package name | `--name` | snake_case of the display name |
| 3 | Organization / reverse domain | `--org` | required |
| 4 | Platforms | `--platforms` | `android,ios` |
| 5 | State management: Bloc or Riverpod | `--state bloc\|riverpod` | none, always asked |
| 6 | Network client: viva_network_kit or plain Dio | `--network viva\|dio` | `viva`, always asked |
| 7 | API base URL per flavor | `--base-url flavor=url` (repeat) | `https://<flavor>.api.example.com` |
| 8 | Starter features beyond home | `--features auth,orders` | none |
| 9 | Languages besides English | `--locales en,bn` | `en` |
| 10 | Crash reporting: none, Sentry or Crashlytics | `--crash` | `none` |
| 11 | CI/CD: GitHub Actions + Fastlane, or none | `--ci github\|none` | `github` |
| 12 | Minimum test coverage, in percent | `--coverage-floor` | `80` |
| 13 | Figma file link | `--figma-url` | none |
| 14 | AI tools the team uses | `--agents` | `all` |

What the choices change:

- **Network.** Feature code only depends on the `AppApiClient` contract, so
  this swaps one class in `lib/core/network/`. Both clients share
  `dio_factory.dart`, `AppFailureConverter` and the `JsonSerializer` API
  (`serializer.addParser<XModel>(XModel.fromJson)`), so features,
  repositories and `add_feature.py` are identical either way.
  viva_network_kit also checks connectivity before each call; plain Dio
  doesn't add the package at all.
- **Locales.** Each extra locale gets `lib/l10n/arb/app_<locale>.arb`,
  seeded with the English strings until it's translated, and the iOS
  locale list is updated. `add_feature.py` adds new strings to every ARB.
- **CI/CD.** `github` generates the workflows, Fastlane and
  `docs/deployment-setup.md`. `none` generates no workflows (Very Good CLI's
  included) and leaves the deployment skill out of the AI layer;
  `scripts/quality_gate.sh` is always generated.
- **Coverage floor.** CI enforces it, and the generator itself fails if a
  freshly generated app falls below it.

## Install

### One line (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/main/install.sh | bash
```

This clones the repo into `~/.flutter-kickstart`, links `fks` and
`flutter-kickstart` into `~/.local/bin` (it tells you if that isn't on your
`PATH`), and links the skills for every agent. `fks update` pulls new
versions. Override locations with `FLUTTER_KICKSTART_HOME` and
`FLUTTER_KICKSTART_BIN`.

On Windows: `irm https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/main/install.ps1 | iex`
(copies the skills and adds `fks` to your user `PATH`).

### Claude Code (plugin)

```text
/plugin marketplace add alamin-karno/flutter-kickstart
/plugin install flutter-kickstart@flutter-kickstart
```

### From a clone

```bash
git clone https://github.com/alamin-karno/flutter-kickstart.git ~/flutter-kickstart
~/flutter-kickstart/install.sh               # symlinks; `fks update` updates them
~/flutter-kickstart/install.sh --copy        # for agents that ignore symlinks
~/flutter-kickstart/install.sh --skills-only # skills only, no `fks` command
~/flutter-kickstart/install.sh --uninstall
```

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
`~/.flutter-kickstart/skills/flutter-kickstart/SKILL.md` and follow
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

Or run the generator yourself (`fks create` takes the same flags):

```bash
fks create \
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
fks run staging                                     # or: fks run (development)
fks add-feature orders --endpoint /v1/orders        # or: python3 tool/kickstart/add_feature.py --name orders
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
    templates/project                      always generated: quality gate, Figma token map
    templates/ci/github                    GitHub Actions, Fastlane, deployment docs (--ci github)
    templates/ai                           AGENTS.md, rules, project skills, subagents
  flutter-figma-to-flutter/SKILL.md        design-to-code
bin/flutter-kickstart                      the `fks` CLI (create, run, add-feature, doctor, update)
install.sh, install.ps1                    one-line installers: CLI + skills for every agent
docs/                                      plan, comparison with app-team-agent-skills
```

## Changing the templates

1. Edit under `skills/flutter-kickstart/templates/` or `scripts/`.
   A template named `x.<choice>.dart.tmpl` is only generated for that
   choice (`bloc`, `riverpod`, `viva`, `dio`) and loses the `.<choice>`
   part, e.g. `dio_api_client.dio.dart.tmpl` -> `dio_api_client.dart`.
2. Regenerate both sides of every choice and make sure they pass (the
   generator runs analyze, tests and the coverage floor):
   ```bash
   cd /tmp && python3 <repo>/skills/flutter-kickstart/scripts/scaffold.py --name demo_bloc --org com.acme --state bloc --network viva --ci github --locales en,bn --features orders --crash sentry
   cd /tmp && python3 <repo>/skills/flutter-kickstart/scripts/scaffold.py --name demo_rp --org com.acme --state riverpod --network dio --ci none --features orders --crash crashlytics
   ```
3. Bump `version` in `.claude-plugin/plugin.json` and run `claude plugin validate .`.

## License

[MIT](LICENSE) © Md. Al-Amin
