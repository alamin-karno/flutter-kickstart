# Changelog

All notable changes to Flutter Kickstart are listed here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Documentation site at https://alamin-karno.github.io/flutter-kickstart/ with a landing page, guides, generated-app docs, CLI and flag reference, troubleshooting, FAQ and contributing docs.
- CI for scripts, manifests, a generator dry-run for every state/network pair and the docs build.
- Automatic docs deployment from `dev`, and tag-driven GitHub Releases.
- Contributing guide, Code of Conduct, security policy, issue and pull request templates.

### Changed
- Git Flow: `dev` is the default branch; `main` holds released versions only.
- The installers and the Claude Code marketplace entry install from `main`, so users only get released versions. Set `FLUTTER_KICKSTART_BRANCH` to try another branch.
- New README with a banner, quick start and links to the docs.

## [1.1.0] - 2026-10-13

### Added
- The `fks` command (alias `flutter-kickstart`): `create`, `run`, `add-feature`, `doctor`, `update`, `uninstall`.
- One-line installers for macOS/Linux (`install.sh`) and Windows (`install.ps1`) that set up the command and the skills for every agent.
- Interview choices for the network client (viva_network_kit or plain Dio), CI/CD (GitHub Actions or none) and extra locales.

### Changed
- Generated apps start at about 95% line coverage.

### Fixed
- `unnecessary_ignore` lint warning on newer Flutter versions.

## [1.0.0] - 2026-10-13

### Added
- First version: interview-driven generator (`scaffold.py`) on Very Good CLI with flavors, clean architecture, Bloc or Riverpod, `AppApiClient` networking, go_router, theming, l10n, crash reporting, tests and GitHub Actions + Fastlane CI/CD.
- Cross-agent AI layer (`AGENTS.md`, project skills, Cursor/Windsurf rules, Copilot instructions, reviewer subagents) and the `flutter-figma-to-flutter` skill.
- Claude Code plugin and marketplace manifests.

[Unreleased]: https://github.com/alamin-karno/flutter-kickstart/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/alamin-karno/flutter-kickstart/releases/tag/v1.1.0
[1.0.0]: https://github.com/alamin-karno/flutter-kickstart/commit/9f2408e
