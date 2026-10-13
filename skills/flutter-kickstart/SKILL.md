---
name: flutter-kickstart
description: Creates a new production-ready Flutter app from a short interview. The app gets Very Good CLI flavors (dev/staging/prod), feature-first clean architecture, Bloc or Riverpod, a viva_network_kit network layer with typed AppFailure errors, go_router, theming, l10n, crash reporting (Sentry/Crashlytics), tests, GitHub Actions + Fastlane CI/CD, and an AI-agent layer (AGENTS.md + skills) that works in Claude Code, Cursor, Windsurf, Antigravity, Codex, Gemini CLI and Copilot. Also adds features to apps it created, and makes an existing scaffolded app AI-ready. Use whenever someone wants to start, create, bootstrap or set up a new Flutter app or project, add a feature/screen with all its layers to a scaffolded app, or set up AI rules/skills for one, even if they don't say "scaffold".
---

# Flutter Kickstart

Turns "start a new Flutter app" into one interview and one deterministic
script run. Don't hand-write the shell: `scripts/scaffold.py` generates
everything from templates and verifies it compiles and passes its tests.

All paths below are relative to this skill's directory (the folder that
contains this `SKILL.md`). The scripts need `python3`, Flutter (or `fvm`),
and Very Good CLI (the script activates it if missing).

## Which path?

| Situation | Do |
| --- | --- |
| New app | Interview (step 1), then run `scaffold.py` (step 2) |
| Add a feature to an app this skill created | `python3 tool/kickstart/add_feature.py --name <feature>` inside the app (also at `scripts/add_feature.py --root <app>`) |
| App was scaffolded before, AI files missing/outdated | `python3 scripts/setup_ai.py --root <app>` |
| Existing app not created by this skill | Don't run the scaffold over it. Follow its own conventions, or offer `setup_ai.py` only if the user wants this skill's AI layer |

## 1. Interview

Ask one question at a time, in this order. Skip a question when an earlier
answer makes it moot. Offer the default in brackets.

| # | Question | Flag |
| - | --- | --- |
| 1 | App display name and one-line description | `--app-name`, `--description` |
| 2 | Package name [snake_case of the display name] | `--name` |
| 3 | Organization / reverse domain, e.g. `com.vivasoftltd` | `--org` |
| 4 | Platforms [android,ios] | `--platforms` |
| 5 | State management: **Bloc or Riverpod**. Always ask; never default it. Client needs vary. | `--state bloc\|riverpod` |
| 6 | API base URL per flavor (development, staging, production). Placeholders are fine if unknown. | `--base-url development=https://...` (repeat) |
| 7 | Starter features beyond home (e.g. auth, orders) | `--features auth,orders` |
| 8 | Crash reporting: none, Sentry or Crashlytics [none] | `--crash` |
| 9 | Figma file link, optional | `--figma-url` |
| 10 | Which AI tools the team uses [all] | `--agents all` or e.g. `claude,cursor,windsurf,antigravity` |

Flavors default to development/staging/production. Those three are fully
wired natively. Custom flavors (`--flavors`) only get Dart entrypoints, and
the script warns about the native parts left to do. Mention this before
accepting custom flavors.

Then read every answer back in one short summary and get a yes before
generating.

## 2. Generate

```bash
python3 scripts/scaffold.py \
  --name acme_wallet --app-name "Acme Wallet" --description "..." \
  --org com.vivasoftltd --platforms android,ios --state bloc \
  --base-url development=https://dev.api.acme.com \
  --base-url staging=https://stg.api.acme.com \
  --base-url production=https://api.acme.com \
  --features auth,orders --crash sentry --agents all \
  --output-dir <parent folder>
```

Add `--dry-run` first if the user wants to see the plan. The script:

1. Creates the Very Good CLI base (native flavors, lints, l10n) and removes
   the counter demo.
2. Writes `lib/core/` (config, network on `viva_network_kit`, `AppFailure`,
   logging, crash reporting, go_router, theme tokens, DI for the chosen
   state management) plus the app shell, flavor entrypoints and tests.
3. Generates `home` and each starter feature with all layers and tests.
4. Adds the dependencies, CI/CD (`pr_checks`, `android`, `ios`), Fastlane,
   scripts and `docs/deployment-setup.md`.
5. Installs the AI layer: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, skills in
   `.agents/skills/` linked into `.claude/`, `.cursor/` and `.windsurf/`,
   Cursor and Windsurf rules, Copilot instructions, Claude reviewer
   subagents, and `tool/kickstart/add_feature.py`.
6. Runs codegen, format, `flutter analyze` and `flutter test`. It stops on
   the first failure.

If a step fails, read the error, fix the cause (often a missing tool or no
network for `pub get`), and re-run with `--skip-create` to reuse the
created project.

## 3. Report

Relay the script's closing summary. State plainly what still needs a human:

- GitHub secrets, the Android keystore and the iOS team/certificates
  (`docs/deployment-setup.md`). The build-and-deploy workflows fail until
  these exist; `pr_checks` works immediately.
- Real API URLs, if placeholders were used.
- The Sentry DSN, or `flutterfire configure` per flavor for Crashlytics.
- The Figma link in `figma-token-map.md`, app icons and the splash screen.

Don't imply the app can ship today because the workflow files exist.

## Conventions the generated app enforces

The generated `AGENTS.md` and `.agents/skills/` are the source of truth.
In short: `presentation -> domain <- data`. Network only through
`AppApiClient`. Repositories return `Either<AppFailure, T>`. State uses
sealed classes. Navigation uses `context.push(AppRoutes.x)`. Styling uses
theme tokens, text uses `context.l10n`, logging uses `AppLogger`. Tests
ship with every change, and `./scripts/quality_gate.sh` must pass.
