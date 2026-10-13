---
title: fks CLI
description: Every fks command (create, run, add-feature, doctor, update, uninstall) with examples.
---

# fks CLI

`fks` is short for **f**lutter **k**ick**s**tart, the way `fvm` is short for
Flutter Version Manager. The long name, `flutter-kickstart`, works too.

| Command | What it does |
| --- | --- |
| `fks create` | Asks the interview questions, generates the app, checks it with `flutter analyze` + `flutter test` |
| `fks create --yes` | Asks only name, org and state management; uses defaults for everything else |
| `fks create --name x --org com.acme --state bloc ...` | No questions; takes the same [flags](/reference/flags) as the generator |
| `fks run [flavor]` | Runs a flavor (default `development`); uses fvm if the project pins a version |
| `fks add-feature <name>` | Adds a feature with all layers, DI, route, l10n and tests to the app in `.` |
| `fks doctor` | Checks Python, Flutter, git and Very Good CLI |
| `fks update` | Pulls the latest release of the templates and skills |
| `fks uninstall` | Removes the commands and the agent skills |

## fks create

```bash
fks create                     # interactive
fks create "Acme Wallet"       # interactive, with the name already filled in
fks create --yes               # quick: name, org and state only
```

Any `--flag` other than `--yes` switches to non-interactive mode and passes
everything straight to the generator:

```bash
fks create \
  --name acme_wallet --app-name "Acme Wallet" --org com.acme \
  --platforms android,ios --state bloc --network viva \
  --base-url development=https://dev.api.acme.com \
  --base-url staging=https://stg.api.acme.com \
  --base-url production=https://api.acme.com \
  --features auth,orders --locales en,bn --crash sentry --ci github --agents all
```

If you say no at the confirmation step, `fks` prints the full command so you
can re-run the same choices later.

## fks run

```bash
fks run                       # flutter run --flavor development -t lib/main_development.dart
fks run staging
fks run production --release  # extra arguments go to flutter run
```

## fks add-feature

```bash
fks add-feature orders
fks add-feature orders --endpoint /v1/orders --entity order
```

Uses the app's own `tool/kickstart/add_feature.py` when it exists. See
[Adding features](/guide/adding-features) for every option.

## fks doctor

```text
fks doctor
  ✓ python3          3.12.4
  ✓ flutter          Flutter 3.35.0 • channel stable
  ✓ git              /usr/bin/git
  • very_good        not found (activated automatically on first create)
  • templates        /Users/you/.flutter-kickstart
```

Exits with a non-zero code if a required tool is missing.
