---
title: Generator flags
description: Every scaffold.py and fks create flag, its default, and a JSON config example for generating Flutter apps without questions.
---

# Generator flags

`fks create` and `scaffold.py` take the same flags. Pass them to skip the
interview, for example in scripts or CI.

```bash
python3 ~/.flutter-kickstart/skills/flutter-kickstart/scripts/scaffold.py --name acme_wallet --org com.acme --state bloc
```

## Project

| Flag | Default | Description |
| --- | --- | --- |
| `--name` | required | Package name, snake_case (e.g. `acme_wallet`) |
| `--app-name` | from `--name` | Display name |
| `--description` | empty | One-line description |
| `--org` | required | Organization / reverse domain, e.g. `com.acme` |
| `--platforms` | `android,ios` | Comma list: `android`, `ios`, `web`, `macos`, `windows` |
| `--flavors` | `development,staging,production` | Custom flavors only get Dart entrypoints |
| `--output-dir` | `.` | Parent folder for the new project |

## Stack

| Flag | Default | Description |
| --- | --- | --- |
| `--state` | required | `bloc` or `riverpod` |
| `--network` | `viva` | `viva` (viva_network_kit) or `dio` (plain Dio) |
| `--base-url` | `https://<flavor>.api.example.com` | `FLAVOR=URL`, repeatable. A bare URL applies to every flavor |
| `--features` | none | Starter features beyond home, e.g. `auth,orders` |
| `--locales` | `en` | Comma list; `en` is always included |
| `--crash` | `none` | `none`, `sentry` or `crashlytics` |

## Delivery and AI

| Flag | Default | Description |
| --- | --- | --- |
| `--ci` | `github` | `github` (Actions + Fastlane) or `none` |
| `--coverage-floor` | `80` | Minimum line coverage CI enforces |
| `--figma-url` | empty | Saved into `figma-token-map.md` |
| `--agents` | `all` | `all` or a comma list of `claude`, `cursor`, `windsurf`, `antigravity`, `codex`, `gemini`, `copilot` |
| `--copy-skills` | off | Copy skills per agent instead of symlinking |

## Run control

| Flag | Description |
| --- | --- |
| `--config answers.json` | Read answers from a JSON file (keys match flags, dashes become underscores) |
| `--dry-run` | Print the plan, write nothing |
| `--skip-create` | Reuse an existing Very Good CLI project at `<output-dir>/<name>` (handy after a failed run) |
| `--skip-verify` | Skip analyze and test at the end |

## Config file example

```json
{
  "name": "acme_wallet",
  "app_name": "Acme Wallet",
  "org": "com.acme",
  "state": "riverpod",
  "network": "dio",
  "base_url": ["development=https://dev.api.acme.com", "production=https://api.acme.com"],
  "features": "auth,orders",
  "locales": "en,bn",
  "crash": "sentry",
  "ci": "github",
  "coverage_floor": 85
}
```

```bash
fks create --config answers.json
```
