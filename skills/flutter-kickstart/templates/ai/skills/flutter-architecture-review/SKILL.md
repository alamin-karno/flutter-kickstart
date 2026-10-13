---
name: flutter-architecture-review
description: Reviews a diff or set of files in {{app_name}} against its architecture, state-management, error-handling, theming, navigation, l10n and network rules. Use after generating or changing feature code and before calling it done, or when asked to review a branch, PR or file for architecture or convention problems.
---

# Architecture review

Review with fresh eyes. Read `AGENTS.md` and the skills it lists for the
areas the diff touches, then check each changed file:

1. **Layering**: does `domain/` import `data/`, `presentation/` or
   Flutter? Does `presentation/` import a `data/` implementation instead of
   going through the feature's DI file? Does a feature import another
   feature?
2. **Errors**: does a data source or repository throw, or return anything
   other than `Either<AppFailure, T>`? Is an exception converted outside
   `core/network/` or a data source?
3. **State**: {{review_state_check}}
4. **Theming**: any `Color(0x...)`, `Colors.*`, bare padding/size numbers
   or inline `TextStyle` that should be a token?
5. **Navigation**: any `Navigator.*`, raw path string, or required data
   passed through `extra`?
6. **Network**: any {{network_packages}} import outside
   `lib/core/network/`? Any model decoded without an
   `addParser` registration?
7. **Text and logging**: user-visible strings not from `context.l10n`? Any
   `print`, or tokens/personal data in logs?

Report each finding as `file:line`, what is wrong, and the fix. If the
diff is clean on all seven checks, say so plainly; don't invent nitpicks.
