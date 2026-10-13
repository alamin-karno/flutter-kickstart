---
name: flutter-deployment
description: CI/CD, configuration, signing and release conventions for {{app_name}}. Use when changing a GitHub Actions workflow, Fastlane lane, flavor, --dart-define config, anything in scripts/, signing, or when preparing a release.
---

# Deployment

Pipelines: `.github/workflows/` (`pr_checks`, `android`, `ios`) and
`ios/fastlane/`. One-time secrets and signing are documented in
`docs/deployment-setup.md`; read it before assuming a pipeline is broken.

## Configuration

- Per-flavor defaults live in `lib/main_<flavor>.dart` (`AppConfig`).
- Override at build time with `--dart-define=API_BASE_URL=...` and
  `--dart-define=SENTRY_DSN=...`. CI passes these from GitHub secrets.
- Never commit secrets, keystores, `.p12` files or DSNs.

## Branch -> flavor stays 1:1

`develop` -> `development`, `staging` -> `staging`, `main` -> `production`
across `android.yml`, `ios.yml` and the Fastlane lanes. Change all of them
together or none.

## Quality gate

`scripts/quality_gate.sh` is what `pr_checks.yml` runs. Never add a
shortcut that skips it.

## Production builds are obfuscated

`--obfuscate --split-debug-info=build/symbols`, paired with
`scripts/upload_symbols.sh` for {{crash_label}}. Never ship one without
the other.

## Changing a workflow

Treat workflow and Fastlane files as reviewed code. Test changes on a PR
before they reach `develop`, `staging` or `main`.
