# flutter-kickstart vs app-team-agent-skills

Compared on 2026-10-13 against
[ArafatRohan93/app-team-agent-skills](https://github.com/ArafatRohan93/app-team-agent-skills)
(`flutter-team` plugin v1.3.0: `flutter-app-structure` and
`flutter-design-system-theme`).

## Where they overlap

Both turn an empty project into a team-standard Flutter shell with flavors,
clean architecture, DI, a network layer with typed errors, go_router,
theme tokens, l10n, logging and crash-reporting contracts, tests, and a
feature generator. Both ship as skills that several agents can load.

## Differences

| Topic | flutter-kickstart (this repo) | app-team-agent-skills |
| --- | --- | --- |
| Entry | Interview, then `scaffold.py` | `flutter create`, then `bootstrap_app.py` |
| Base | Very Good CLI (flavors, lints, l10n built in) | Plain `flutter create`; Android + iOS flavors added by script (Ruby `xcodeproj`) |
| State management | Bloc/Cubit **or** Riverpod, asked per project | Cubit only |
| DI | get_it + injectable modules, or the Riverpod provider graph | get_it with hand-written modules |
| Errors | dartz `Either`, sealed `AppFailure` from one `AppFailureConverter` | fpdart `Either`, `NetworkException` -> `Failure` with localized messages |
| Network | `AppApiClient` on `viva_network_kit` (company package) or plain Dio, asked in the interview | Own Dio client + interceptors |
| Navigation | go_router + `AppRoutes` path constants | go_router behind an `AppNavigator`, typed route classes with `fromParams` |
| Extra abstractions | - | Key-value/secure storage, image resolver (SVG/PNG) |
| Crash reporting | Console, Sentry or Crashlytics adapter generated | Contract + console implementation; backend documented |
| CI/CD | GitHub Actions (PR gate, Android, iOS), Fastlane, store upload, symbol upload, setup doc | `local_ci.sh` (format, analyze, tests, Android + iOS flavor builds) |
| Design | Figma MCP -> widgets (`flutter-figma-to-flutter`) | Design hand-off -> Material 3 theme from Stitch, DTCG/Figma tokens, CSS/Tailwind, HTML, PDF and screenshots, with contrast tests and a designer mapping report |
| AI layer in the generated app | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, 10 project skills for all agents, Cursor/Windsurf rules, Copilot instructions, Claude reviewer subagents, vendored feature generator | None; relies on the skill being installed globally |
| Existing apps | Feature generator and AI layer for scaffolded apps | Per-area reference docs that guide work in any app following its conventions |
| Install | Claude plugin marketplace, `install.sh`/`install.ps1` for 8 agent folders | `npx skills`, `install.sh` (3 folders), manual links |

## Takeaways

- **Complementary, not duplicates.** This repo covers project setup to
  store release and keeps every agent on the conventions inside the
  generated repo. The other repo is stronger on design-system theming and
  on guiding work in existing apps.
- **Both trigger on "new Flutter app".** With both installed globally, an
  agent may pick either skill. Install one per machine, or merge them into
  one team repo.
- **Conventions differ** (dartz vs fpdart, injectable vs manual modules,
  `viva_network_kit` vs own Dio client, path constants vs typed routes).
  Pick one team standard before a wide rollout.
- **Not ported here** (candidates if the team wants parity): storage and
  image-resolver abstractions, typed routes with `fromParams`, localized
  failure messages, native flavor builds in a local CI script, and the
  design-token theme pipeline. `flutter-design-system-theme` expects
  `flutter-app-structure`'s theme files, so it would need porting to this
  plugin's `lib/core/theming/` before it can theme apps generated here.
