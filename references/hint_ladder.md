# Hint ladder

Each hint request climbs **one** level. Always call `state.py hint SLUG` first: it
records the hint and returns the level to give (`level` 1 to 4, or `null` when all
four are used). Never skip levels, and never give more than the level returned.

| Level | Give | Do not give |
|---|---|---|
| 1. Pattern family | The family of technique: "this is a sliding-window problem", "think about what a hash map could remember for you". | Which variable to track, any code. |
| 2. Key insight | The one observation that unlocks it: "if the window sum is already too big, growing it can never help, so shrink from the left". | The full sequence of steps. |
| 3. Approach outline | 3 to 5 plain-language steps of the algorithm, plus the target complexity. | Code or pseudocode. |
| 4. Pseudocode | Language-neutral pseudocode of the whole approach. | Python. They still write the solution. |

After level 4, offer the full explanation (`render_explanation.py`), which the
user can ask for at any time anyway.

## Looking at the user's code

Read `workspace/<slug>/solution.py` before giving a hint. Fit the hint to it:

- If they are on a workable path, hint **along their path** ("your two-loop version
  is correct; what work does the inner loop repeat?") instead of steering them to
  the reference approach.
- If they have a bug rather than a wrong idea, the hint can be about the bug, but
  at the same level of detail: level 1 points at the area ("look at what happens
  when the list is empty"), higher levels get more specific.

## Style

- One or two sentences for levels 1 and 2. Ask a question when it can do the work:
  "what would you need to know about the numbers you've already seen?"
- Never paste the reference solution or reveal hidden test data.
- Hints count: any hint makes the eventual solve "with hints". Do not tell the user
  this to discourage asking; struggling for a long time teaches less than a good hint.
