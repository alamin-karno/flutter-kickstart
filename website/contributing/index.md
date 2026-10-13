---
title: How to contribute
description: How to report bugs, suggest features and open pull requests for Flutter Kickstart, with the branch, commit and review rules.
---

# How to contribute

Thanks for helping. Bug reports, ideas, docs fixes and code are all welcome.

## Report a bug or suggest a feature

[Open an issue](https://github.com/alamin-karno/flutter-kickstart/issues/new/choose)
and pick a template. For bugs, include:

- the command you ran (or what you asked your agent),
- the output of `fks doctor`,
- what you expected and what happened.

## Your first pull request

1. **Fork** the repo and clone your fork.
2. **Branch from `dev`** (never from `main`):
   ```bash
   git checkout dev
   git pull
   git checkout -b feature/short-description
   ```
3. **Make the change.** Keep it focused on one thing.
4. **Check it** (see below).
5. **Open a pull request into `dev`** and fill in the template.

See [Branches and releases](/contributing/git-flow) for branch names and how
releases work.

## Checks before you open a PR

| You changed | Run |
| --- | --- |
| Python scripts | `python3 -m py_compile bin/flutter-kickstart skills/flutter-kickstart/scripts/*.py` |
| Templates | Generate both sides of every choice (see [Changing the templates](/contributing/templates)) |
| Installers | `bash -n install.sh` |
| Plugin manifests | `claude plugin validate .` |
| Docs site | `cd website && npm ci && npm run build` |

CI runs the fast checks on every pull request. Template changes also need the
generation runs, because they compile and test real Flutter apps.

## Rules

- **Pull requests only.** Nobody pushes straight to `dev` or `main`; both branches are protected.
- **One topic per PR.** Smaller PRs get reviewed faster.
- **Keep CI green.** A PR can't merge until its checks pass.
- **Update the docs** in `website/` when you change behaviour, flags or output.
- **Add a CHANGELOG line** under `Unreleased` for anything users will notice.
- **Write clear commits** in the imperative mood: `Add Riverpod family providers`, not `added stuff`.
- **Be kind.** We follow the [Code of Conduct](https://github.com/alamin-karno/flutter-kickstart/blob/dev/CODE_OF_CONDUCT.md).

## Security issues

Please don't open a public issue. See the
[security policy](https://github.com/alamin-karno/flutter-kickstart/blob/dev/SECURITY.md).
