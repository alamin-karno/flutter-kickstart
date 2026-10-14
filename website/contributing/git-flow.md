---
title: Branches and releases
description: The Git Flow model Flutter Kickstart uses, covering the dev, main, feature, release and hotfix branches, version tags and automatic docs publishing.
---

# Branches and releases

Flutter Kickstart uses **Git Flow**. Work happens on `dev`. `main` only ever
holds released versions, and every release has a tag.

```text
feature/*  ──PR──▶  dev  ──▶  release/x.y.z  ──PR──▶  main  ──tag──▶  vX.Y.Z
                     ▲                                  │
                     └────────── back-merge PR ─────────┘
```

## Branches

| Branch | Purpose | Created from | Merges into |
| --- | --- | --- | --- |
| `dev` | Default branch; the next release takes shape here | — | — |
| `main` | Released code only; installers and the plugin read from here | — | — |
| `feature/<name>` | A new feature or improvement | `dev` | `dev` (PR, squash) |
| `fix/<name>` | A bug fix for the next release | `dev` | `dev` (PR, squash) |
| `docs/<name>` | Docs-only change | `dev` | `dev` (PR, squash) |
| `release/<x.y.z>` | Freeze, version bump, changelog | `dev` | `main` (PR, merge commit) |
| `hotfix/<x.y.z>` | Urgent fix to a released version | `main` | `main` (PR), then back to `dev` |

`dev` and `main` are protected. They can't be deleted or force-pushed, and
every change arrives through a pull request with passing checks.

## Making a release

1. **Cut the branch** from an up-to-date `dev`:
   ```bash
   git checkout dev && git pull
   git checkout -b release/1.2.0
   ```
2. **Bump the version** in `.claude-plugin/plugin.json`.
3. **Update `CHANGELOG.md`**: rename `Unreleased` to `1.2.0 - YYYY-MM-DD` and add a fresh `Unreleased` section.
4. **Open a PR from `release/1.2.0` into `main`.** Only fixes go on this branch now.
5. **Merge with a merge commit** (not squash), so `main` and `dev` share history.
6. **Tag `main`**:
   ```bash
   git checkout main && git pull
   git tag -a v1.2.0 -m "v1.2.0"
   git push origin v1.2.0
   ```
   The **Release** workflow checks the tag matches `plugin.json` and publishes a GitHub Release with that version's changelog notes.
7. **Back-merge** with a PR from `main` into `dev`, so `dev` has the version bump.

## Versioning

We use [Semantic Versioning](https://semver.org):

- **Major** (`2.0.0`): generated apps or flags change in a way that breaks existing usage.
- **Minor** (`1.2.0`): new options, features or templates; existing usage keeps working.
- **Patch** (`1.1.1`): bug fixes only.

## The docs site

This site is built from `website/` with VitePress. A push to `dev` that
touches `website/` rebuilds and publishes it to GitHub Pages automatically.
Pull requests build the site too, so broken links are caught before merging.
