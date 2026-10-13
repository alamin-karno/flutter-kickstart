# Contributing to Flutter Kickstart

Thanks for helping! Bug reports, ideas, docs fixes and code are all welcome.
This guide explains how we work so your contribution can land quickly.

- [Ways to help](#ways-to-help)
- [Branches (Git Flow)](#branches-git-flow)
- [Your first pull request](#your-first-pull-request)
- [Checks before you open a PR](#checks-before-you-open-a-pr)
- [Pull request rules](#pull-request-rules)
- [Commit messages](#commit-messages)
- [Making a release (maintainers)](#making-a-release-maintainers)

## Ways to help

- **Report a bug**: [open a bug report](https://github.com/alamin-karno/flutter-kickstart/issues/new?template=bug_report.yml) with the command you ran and the output of `fks doctor`.
- **Suggest a feature**: [open a feature request](https://github.com/alamin-karno/flutter-kickstart/issues/new?template=feature_request.yml) and describe the problem it solves.
- **Improve the docs**: the site lives in [`website/`](website). Every page has an "Edit this page" link.
- **Write code**: pick an issue, or open one first for anything big so we can agree on the approach.

Security problems: please **don't** open a public issue. See [SECURITY.md](SECURITY.md).

## Branches (Git Flow)

```text
feature/*  ──PR──▶  dev  ──▶  release/x.y.z  ──PR──▶  main  ──tag──▶  vX.Y.Z
                     ▲                                  │
                     └────────── back-merge PR ─────────┘
```

| Branch | What it's for | Branch from | PR into |
| --- | --- | --- | --- |
| `dev` | **Default branch.** The next release takes shape here | — | — |
| `main` | Released code only. Installers and the plugin read from here | — | — |
| `feature/<short-name>` | New features and improvements | `dev` | `dev` |
| `fix/<short-name>` | Bug fixes for the next release | `dev` | `dev` |
| `docs/<short-name>` | Docs-only changes | `dev` | `dev` |
| `release/<x.y.z>` | Version bump and changelog for a release | `dev` | `main` |
| `hotfix/<x.y.z>` | Urgent fix to a released version | `main` | `main`, then back to `dev` |

`dev` and `main` are **protected**: no direct pushes, no force pushes, no
deleting. Every change goes through a pull request with passing CI.

## Your first pull request

1. **Fork** the repo and clone your fork.
2. **Create a branch from `dev`:**
   ```bash
   git checkout dev
   git pull upstream dev
   git checkout -b feature/riverpod-family-providers
   ```
3. **Install from your clone** so `fks` and the skills use your changes:
   ```bash
   ./install.sh
   ```
4. **Make one focused change.**
5. **Run the checks** below.
6. **Push and open a pull request into `dev`.** Fill in the template.

## Checks before you open a PR

| You changed | Run |
| --- | --- |
| Python (`bin/`, `skills/**/scripts/`) | `python3 -m py_compile bin/flutter-kickstart skills/flutter-kickstart/scripts/*.py` |
| Templates or generator | Generate **both sides of every choice** and make sure both pass (below) |
| Installers | `bash -n install.sh` |
| Plugin manifests | `claude plugin validate .` |
| Docs site | `cd website && npm ci && npm run build` (fails on dead links) |

Template changes compile and test real Flutter apps, so run both:

```bash
cd /tmp
python3 <repo>/skills/flutter-kickstart/scripts/scaffold.py --name demo_bloc --org com.acme \
  --state bloc --network viva --ci github --locales en,bn --features orders --crash sentry
python3 <repo>/skills/flutter-kickstart/scripts/scaffold.py --name demo_rp --org com.acme \
  --state riverpod --network dio --ci none --features orders --crash crashlytics
```

A template named `x.<choice>.dart.tmpl` is generated only for that choice
(`bloc`, `riverpod`, `viva`, `dio`). More detail:
[Changing the templates](https://alamin-karno.github.io/flutter-kickstart/contributing/templates).

## Pull request rules

- **Target `dev`.** PRs into `main` are only for `release/*` and `hotfix/*` branches.
- **One topic per PR.** Small PRs get reviewed faster.
- **CI must pass.** `CI / Scripts and manifests` and `CI / Docs build` are required.
- **Update the docs** in `website/` when behaviour, flags or output change.
- **Add a CHANGELOG entry** under `## [Unreleased]` for anything users will notice.
- **Don't bump the version.** That happens on the release branch.
- **Squash merge** feature PRs into `dev`. Release and back-merge PRs use a merge commit.

## Commit messages

Write the summary in the imperative mood, under about 70 characters, and
explain *why* in the body when it isn't obvious.

```text
Add Riverpod family providers to the feature template

Features that load one item by id needed a hand-written provider.
```

Good: `Fix iOS locale list for extra languages`. Not so good: `fixed stuff`.

## Making a release (maintainers)

1. `git checkout dev && git pull && git checkout -b release/1.2.0`
2. Bump `version` in `.claude-plugin/plugin.json`.
3. In `CHANGELOG.md`, rename `[Unreleased]` to `[1.2.0] - YYYY-MM-DD` and add a new empty `[Unreleased]`.
4. Open a PR from `release/1.2.0` into `main`; merge it with a **merge commit**.
5. Tag `main`: `git checkout main && git pull && git tag -a v1.2.0 -m "v1.2.0" && git push origin v1.2.0`
6. The **Release** workflow checks the tag and publishes the GitHub Release from the changelog.
7. Open a PR from `main` into `dev` to bring the release back.

We follow [Semantic Versioning](https://semver.org): breaking changes bump
the major, new features the minor, fixes the patch.

## Code of Conduct

By taking part you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
