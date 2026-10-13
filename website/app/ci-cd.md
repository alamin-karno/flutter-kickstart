---
title: CI/CD and releases
description: The GitHub Actions workflows, Fastlane lanes, branch-to-flavor mapping and secrets a Flutter Kickstart app gets with --ci github.
---

# CI/CD and releases

Choose `--ci github` (the default) to get GitHub Actions workflows, Fastlane
and a setup guide. Choose `--ci none` to skip all of it. You still get
`scripts/quality_gate.sh`.

## Workflows

| Workflow | Runs on | Does |
| --- | --- | --- |
| `pr_checks.yml` | Pull requests to `develop`, `staging`, `main` | Quality gate + coverage floor |
| `android.yml` | Pushes to `develop`, `staging`, `main` | Builds and signs an App Bundle, uploads symbols, then Firebase App Distribution or the Play internal track |
| `ios.yml` | Pushes to `develop`, `staging`, `main` | Builds and signs with Fastlane, uploads symbols, ships to TestFlight / App Store |

## Branch to flavor

| Branch | Flavor | Android goes to | iOS goes to |
| --- | --- | --- | --- |
| `develop` | development | Firebase App Distribution | TestFlight |
| `staging` | staging | Firebase App Distribution | TestFlight |
| `main` | production | Play Store (internal track) | App Store Connect |

## What works right away

`pr_checks` works as soon as you push. The build-and-deploy workflows fail
until you add signing keys and secrets. That is expected: nobody can ship an
app without them.

## Secrets you need to add

The full list, with how to create each one, is in your app's
`docs/deployment-setup.md`. In short:

| Secret | For |
| --- | --- |
| `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_ALIAS`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEYSTORE_PRIVATE_KEY_PASSWORD` | Android signing |
| `PLAY_STORE_SERVICE_ACCOUNT_JSON` | Play Console upload |
| `FIREBASE_APP_ID_ANDROID`, `FIREBASE_SERVICE_ACCOUNT` | Firebase App Distribution |
| `APP_STORE_CONNECT_API_KEY_ID`, `APP_STORE_CONNECT_API_ISSUER_ID`, `APP_STORE_CONNECT_API_KEY_CONTENT` | Fastlane and App Store Connect |
| `IOS_CERTIFICATE_BASE64`, `IOS_CERTIFICATE_PASSWORD`, `IOS_PROVISIONING_PROFILE_BASE64`, `KEYCHAIN_PASSWORD` | iOS signing |
| `API_BASE_URL` | Optional base-URL override (use GitHub environments for one per flavor) |

Crash reporting adds its own rows (for example `SENTRY_DSN`).
