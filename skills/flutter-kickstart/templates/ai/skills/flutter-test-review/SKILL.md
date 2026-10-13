---
name: flutter-test-review
description: Checks that new or changed code in {{app_name}} has the tests the flutter-testing skill requires, then runs them. Use after generating or changing code and before calling it done, or when asked whether a change is adequately tested.
---

# Test review

Read `.agents/skills/flutter-testing/SKILL.md` for the requirements, then
for each changed file in `lib/`:

1. Repository / use case -> a unit test with its dependency mocked
   (`mocktail`).
2. {{test_review_state_check}}
3. Screen or shared widget -> a widget test using `pumpApp`.
4. New critical flow -> an `integration_test/` smoke test.

Then run `./scripts/quality_gate.sh` and read the result: files existing is
not enough, they must pass and coverage must not drop.

Report what is missing per file, not a generic "add more tests". If every
required test exists and passes, say so plainly.
