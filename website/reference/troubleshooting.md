---
title: Troubleshooting
description: Fixes for common Flutter Kickstart problems, such as fks not found, agents not seeing the skills, failed generation and CI build failures.
---

# Troubleshooting

## `fks: command not found`

The installer puts `fks` in `~/.local/bin`. Add it to your `PATH`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # or ~/.bashrc
source ~/.zshrc
```

On Windows, open a new terminal. The installer added `fks` to your user `PATH`.

## My agent doesn't know the skill

- Start a **new** agent session. Skills load when a session starts.
- Check the skill is linked: `ls ~/.claude/skills/flutter-kickstart` (or your agent's folder from [Installation](/guide/installation#where-the-skills-go)).
- If your agent ignores symlinks, reinstall with copies: `~/.flutter-kickstart/install.sh --copy`.

## Generation stopped with an error

The generator stops at the first failing step and prints why. Common causes:

| Symptom | Fix |
| --- | --- |
| `pub get` fails | Check your network or proxy, then re-run |
| `very_good` not found | Run `dart pub global activate very_good_cli`, and make sure `~/.pub-cache/bin` is on your `PATH` |
| Wrong Flutter version | Pin one with fvm, or upgrade Flutter |

After fixing the cause, reuse the project that was already created:

```bash
fks create <same flags> --skip-create
```

## `fks run` says there's no `lib/main_<flavor>.dart`

Run it from the app's root folder. The error lists the flavors that exist.

## Android/iOS workflows fail in CI

That is expected until you add signing keys and secrets. `pr_checks` works
right away. Follow `docs/deployment-setup.md` in your app, or see
[CI/CD and releases](/app/ci-cd).

## Coverage check fails on a pull request

Add tests for the code you changed, then run `./scripts/quality_gate.sh`
locally. Generated files (`*.g.dart`, l10n output, flavor entrypoints) don't
count toward coverage.

## Still stuck?

[Open an issue](https://github.com/alamin-karno/flutter-kickstart/issues/new/choose)
with the output of `fks doctor` and the command you ran.
