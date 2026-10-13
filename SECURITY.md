# Security Policy

## Supported versions

Only the latest release gets security fixes. `fks update` (or re-running the
installer) always moves you to it.

| Version | Supported |
| --- | --- |
| Latest release | ✅ |
| Older releases | ❌ |

## Reporting a vulnerability

Please **don't** open a public issue for security problems.

Report it privately through
[GitHub private vulnerability reporting](https://github.com/alamin-karno/flutter-kickstart/security/advisories/new).
Include:

- what is affected (installer, `fks` CLI, generator, a template, the docs site),
- steps to reproduce it,
- the impact you expect.

You'll get a reply within a few days. Once a fix is released, we'll credit you
in the release notes unless you'd rather stay anonymous.

## Scope notes

Flutter Kickstart runs on your machine and writes a Flutter project from its
templates. Of special interest:

- the one-line installers (`install.sh`, `install.ps1`),
- anything that could make a generated app leak secrets (keys, DSNs, signing material),
- generated CI workflows that could expose repository secrets.
