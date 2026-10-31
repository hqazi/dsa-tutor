# Review rubric

Use when the user says "review", "submit", "check my solution" or similar.

## Steps

1. Run the tests **first**, with the agent-facing JSON output:
   `python scripts/run_tests.py SLUG --json`. Correctness comes from this, never
   from reading the code.
2. Read `workspace/<slug>/solution.py` and the problem's `meta.json`
   (`expected_complexity`).
3. Assess the four areas below.
4. Reply with the format below.
5. Record the attempt, but only if all tests pass or the user is giving up / moving on:
   `python scripts/state.py record SLUG --passed P --total T --notes "..."`
   (add `--gave-up` when they stop without solving). The outcome (`unaided`,
   `with_hints`, `gave_up`) is worked out from the hints and explanation recorded.
   If tests fail and the user will keep going, do **not** record yet.

## Areas

| Area | What to check | Grades |
|---|---|---|
| Correctness | Test results. Name each failing case: id or hidden category. | all pass / fails some / fails most |
| Complexity | Derive time and space from the code. Compare with `expected_complexity`. A timeout on "large input" is a complexity problem, not a correctness one. | meets / slower than expected (say which part) |
| Edge cases | Empty input, single element, duplicates, negatives, bounds. Use the hidden-test categories as prompts. Point out cases handled by accident. | handled / missing (name them) |
| Readability | Names, structure, no dead code, comments only where they help, idiomatic Python (e.g. `enumerate`, unpacking). | clear / could be clearer (one concrete suggestion) |

## When tests fail

Point to **the failing case and the area of code**, not the fix:

- Visible case: quote input, expected and actual from the test output.
- Hidden case: give only its category ("fails on: empty input") and, if the output
  includes it, the line number of an exception. Never invent or reveal hidden data.
- Name the region: "the loop that shrinks the window (lines 8–11) never runs when...".
- Give the fix only if the user asks for it.

## Reply format

```
Verdict: <Solved ✓ | Not yet: N of M tests pass | Solved, but too slow>

Correctness  …
Complexity   O(…) time, O(…) space (target O(…)): …
Edge cases   …
Readability  …

To improve:
1. …
2. … (at most two items)
```

Keep it short. Praise what is genuinely good in one clause; do not pad.

## Reviewer notes (`--notes`)

One or two short sentences for future sessions: what went wrong or right, and
patterns worth watching. Example: `"Forgot the empty-input case; first try was
O(n^2), fixed after hint 2."` These are read later, so be specific and neutral.
