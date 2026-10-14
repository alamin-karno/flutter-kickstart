# Changelog

All notable changes to Flutter Kickstart are listed here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-10-15

First public release.

### Added
- A generator driven by a few setup questions, on Very Good CLI: development, staging and production flavors, feature-first clean architecture, Bloc or Riverpod, an `AppApiClient` network layer on viva_network_kit or plain Dio, go_router, theming, l10n with optional extra locales, crash reporting and tests. Generated apps pass `flutter analyze` and `flutter test` and start at about 95% line coverage.
- Optional CI/CD: GitHub Actions workflows and Fastlane lanes.
- Cross-agent AI layer in every generated app: `AGENTS.md`, project skills, Cursor and Windsurf rules, Copilot instructions and reviewer subagents, plus the `flutter-figma-to-flutter` skill.
- The `fks` command (alias `flutter-kickstart`): `create`, `run`, `add-feature`, `doctor`, `update`, `uninstall`.
- One-line installers for macOS/Linux (`install.sh`) and Windows (`install.ps1`) that set up the command and link the skills for every agent. Set `FLUTTER_KICKSTART_BRANCH` to a tag such as `v1.0.0` to install that exact release.
- Claude Code plugin and marketplace manifests.
- Documentation site at https://alamin-karno.github.io/flutter-kickstart/ with guides, generated-app docs, CLI and flag reference, troubleshooting, FAQ and contributing docs.
- CI for scripts, manifests, a generator dry-run for every state/network pair and the docs build; automatic docs deployment; tag-driven GitHub Releases.
- Contributing guide, Code of Conduct, security policy, issue and pull request templates.

[Unreleased]: https://github.com/alamin-karno/flutter-kickstart/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/alamin-karno/flutter-kickstart/releases/tag/v1.0.0
