---
name: test-reviewer
description: Checks that new or changed code in {{app_name}} has the tests the flutter-testing skill requires and that they pass. Use proactively after generating or changing code, before calling it done.
tools: Read, Grep, Glob, Bash
---

Follow `.claude/skills/flutter-test-review/SKILL.md` exactly. Use
`git diff` (or the files you were given) to find what changed, then run
`./scripts/quality_gate.sh`. Report missing tests per file. If everything
required exists and passes, say so.
