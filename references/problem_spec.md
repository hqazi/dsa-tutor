# Problem spec (for generating problems)

Generate a problem when the user asks for a new one, or when `state.py next`
returns `"action": "generate"`. Write a spec JSON file, then:

```bash
python scripts/new_problem.py create problems/generated/_drafts/<slug>.json
```

(`_drafts/` is git-ignored.) The script validates the spec, fills in expected
outputs from your brute force, and runs the **self-check**: the reference solution
must pass every test within the 2-second limit. Nothing is written unless it
passes. On `"ok": false`, read `problems` / `failures`, fix the spec (usually a
wrong hand-written expected value or a buggy reference) and run `create` again.
Never show the problem to the user before `create` succeeds. On success it also
scaffolds `workspace/<slug>/solution.py`; then call `state.py start SLUG`.

## Fields

```json
{
  "slug": "busiest-hour-window",
  "title": "Busiest Hour",
  "topic": "sliding-window",
  "difficulty": "medium",
  "statement": "Markdown. What to compute, in plain words, with a small story if it helps.",
  "constraints": ["1 <= len(visits) <= 10^5", "0 <= visits[i] <= 10^4"],
  "notes": "Optional Markdown shown after the constraints (e.g. a follow-up).",
  "signature": {
    "function": "busiest_window",
    "params": [{"name": "visits", "type": "list[int]"}, {"name": "k", "type": "int"}],
    "returns": "int"
  },
  "compare": {"mode": "exact"},
  "expected_complexity": {"time": "O(n)", "space": "O(1)"},
  "tests": [
    {"visibility": "visible", "input": {"visits": [1, 3, 2], "k": 2}, "expected": 5,
     "explanation": "Optional, shown under the example."},
    {"visibility": "visible", "input": {"visits": [4], "k": 1}},
    {"visibility": "hidden", "category": "all zeros", "input": {"visits": [0, 0, 0], "k": 2}},
    {"visibility": "hidden", "category": "large input", "input": {"visits": [...], "k": 5000},
     "expected_by": "reference"}
  ],
  "reference_solution": "def busiest_window(visits, k):\n    ...\n",
  "brute_force": "def busiest_window(visits, k):\n    return max(sum(visits[i:i+k]) for i in range(len(visits)-k+1))\n"
}
```

| Field | Rules |
|---|---|
| `slug` | lowercase words joined by hyphens; must not exist yet (`--force` replaces). |
| `topic` | an id from `topics.md`. |
| `difficulty` | `easy`, `medium` (or `hard` if the user asks). Match `topics.md`. |
| `signature.params[].type` | Python type hints. Use `ListNode \| None` / `TreeNode \| None` for linked lists and trees; the harness builds them from JSON lists (trees in level order with `null`). |
| `compare.mode` | `exact` (default), `unordered` (list order ignored), `unordered_deep` (order ignored at every level, e.g. groups of items), `float` (+ `tolerance`, default 1e-6 relative). |
| `tests[].visibility` | at least **2 visible** (shown as examples) and **3 hidden** tests. |
| `tests[].category` | required for hidden tests; it is all the user sees when one fails, so make it meaningful: `empty input`, `single element`, `duplicates`, `negative numbers`, `large input`... |
| `tests[].expected` | optional when `brute_force` is given; the brute force then computes it. |
| `tests[].expected_by` | `"reference"` only for large performance tests the brute force is too slow for. Needs `brute_force` in the spec (the reference must first agree with it on every other test). |
| `reference_solution` | the optimal solution; must run each test within 2 s. |
| `brute_force` | strongly recommended: a simple, obviously-correct solution, written differently from the reference. It makes expected values trustworthy. |

## Writing a good problem

- **Original wording.** Do not copy well-known problem statements; give it its own
  framing and names. Classic patterns are fine.
- **One clear answer.** If several answers could be valid, define a tie-break
  ("smallest index first") or use an `unordered` compare mode.
- **No hint in the statement** about the technique beyond what an interviewer
  would say. Expected complexity lives in `meta.json`, not in `problem.md`, unless
  the brute force is plausible and you want to rule it out ("aim for O(n)").
- **Function-based.** One function that returns a value (no in-place-only
  mutation, no classes to implement, no printing).
- **Inputs are JSON**: numbers, strings, booleans, lists, objects, `null`.
- **Visible tests small** (they are printed in `problem.md`); hidden tests cover
  edge cases: empty, single, duplicates, negatives, extremes, plus 1–3 random,
  and for medium problems one `large input` test sized so the expected complexity
  passes easily and a naive approach times out (roughly n = 10^4 to 2·10^4).
- Keep `tests.json` under ~300 KB.
