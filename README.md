# DSA Tutor

A personal data-structures-and-algorithms tutor that runs inside the coding agent
you already use. Fork this repo and it becomes **your** tutor: it asks a few
questions once, recommends problems, runs your code against real tests, gives
hints one level at a time, reviews your solutions, and writes explanations, while
your progress is committed right here in your fork.

- **Any agent.** The instructions are plain Markdown (`SKILL.md`), and
  everything deterministic is a small Python script. No agent-specific features.
- **Honest feedback.** Pass/fail comes from running tests, not from the model's opinion.
- **Teaches, doesn't tell.** Hints on request, full explanations whenever you want them.
- **Python only** for now, standard library only, Python 3.10+. No services, no containers.

## Setup

1. **Fork** this repo on GitHub, then clone your fork.
2. Point your agent at the skill:

   | Agent | How |
   |---|---|
   | Claude Code | Open the repo folder. `CLAUDE.md` points the agent at `SKILL.md`. To use it from anywhere, link the repo as a skill: `ln -s "$PWD" ~/.claude/skills/dsa-tutor`. |
   | Codex, Cursor, Copilot, Gemini CLI, others | Open the repo folder; `AGENTS.md` points the agent at `SKILL.md`. If your agent ignores it, say: *"Read SKILL.md and follow it."* |

3. Say **"Let's practise"**. The first session starts with five quick questions
   (say "skip" to use defaults).
4. Commit and push now and then: `state/`, `workspace/` and `explanations/` are
   your record.

## How a session goes

```
you    what next?
agent  Two Receipts (hashing, easy): staying on your focus topic until it's
       comfortable (1/3 unaided solves). Write your code in
       workspace/pair-with-target/solution.py
you    hint
agent  (level 1) Which earlier number would complete a pair with the current one?
you    review
agent  Verdict: Solved ✓ · O(n) time, O(n) space (target O(n)) · ...
```

Things you can say: *what next?*, *give me a medium graph problem*, *a new
problem on heaps*, *hint*, *run the tests*, *review*, *explain it*, *I give up*,
*how am I doing?*, *update my profile*.

Run the tests yourself at any time:

```bash
python scripts/run_tests.py pair-with-target
```

## How it decides what is next

- Each topic has a level: **new**, **learning** (something attempted), or
  **comfortable** (3 different problems solved without hints).
- You stay on your focus topic until it is comfortable, then move to the weakest
  topic whose prerequisites are comfortable (see `references/topics.md`).
- Problems are **easy** until you have 2 unaided solves in the topic, then **medium**.
- Unattempted curated problems come first; when a topic runs out, the agent
  generates a new problem and checks its reference solution against every test
  before showing it to you.

## What's inside

```
SKILL.md                    instructions for the agent (router: intent → script/reference)
scripts/                    state.py · new_problem.py · run_tests.py · render_explanation.py
references/                 topics, questionnaire, problem spec, review rubric, hint ladder
runners/python/harness.py   runs a solution on JSON test cases
problems/curated/           50 original problems across 15 topics
problems/generated/         problems made for you on demand
workspace/<slug>/           your solutions
state/                      your profile, progress and attempt log
explanations/<slug>.html    explanation pages (self-contained, light and dark)
```

| Topic | Easy | Medium |
|---|---|---|
| Arrays & strings | 2 | 1 |
| Hash maps & sets | 2 | 2 |
| Two pointers | 2 | 1 |
| Sliding window | 2 | 2 |
| Prefix sums | 2 | 1 |
| Stacks | 2 | 1 |
| Linked lists | 2 | 1 |
| Binary search | 2 | 1 |
| Sorting & intervals | 2 | 1 |
| Recursion & backtracking | 2 | 1 |
| Binary trees | 2 | 2 |
| Heaps | 2 | 1 |
| Graphs | 2 | 2 |
| Greedy | 2 | 1 |
| Dynamic programming | 2 | 2 |

## Notes

- **Your code runs locally, unsandboxed**, in a Python subprocess with a 2-second
  limit per test. It is your own code, so that is fine; just don't run solutions you
  don't trust.
- **Getting upstream updates** (new problems, fixes): add this repo as `upstream`
  and merge. Upstream never touches `state/`, `workspace/` or `explanations/`, so
  merges don't conflict with your progress.
- **More languages later:** tests are language-neutral JSON and each language is a
  folder under `runners/`, so adding one means a new runner plus a signature in
  `meta.json`.

## Development

```bash
python -m unittest discover -s tests          # script tests
python scripts/new_problem.py validate --all  # every reference passes its tests
```

Licensed under Apache 2.0.
