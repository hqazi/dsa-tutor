# Onboarding questionnaire

Use this when `state.py status` reports `"onboarded": false`, or when the user says
"update my profile". Ask the questions **before anything else**, one message with
all five is fine. Accept short answers. If the user says "skip" (to everything or
to one question), use the default.

| # | Question | Saved as | Values | Default |
|---|---|---|---|---|
| 1 | What is your goal: preparing for interviews (and if so, roughly when), or general practice? | `goal`, `interview_date` | `interview` / `general`; date `YYYY-MM-DD` or `null` | `general` |
| 2 | How much DSA experience do you have? | `experience` | `beginner` / `intermediate` / `advanced` | `beginner` |
| 3 | How comfortable are you with each area? (none / some / solid) basics (arrays, hashing, two pointers, sliding window, prefix sums) · linear (stacks, linked lists) · search & sort · trees & graphs (incl. heaps) · recursion & DP (incl. greedy) | `comfort.<group>` | `none` / `some` / `solid` per group: `basics`, `linear`, `search-sort`, `trees-graphs`, `recursion-dp` | all `none` |
| 4 | When you are stuck, do you want a nudge early, or would you rather struggle first? | `hint_preference` | `early` / `struggle` | `early` |
| 5 | Is there a topic you want to focus on right now? | `focus_topic` | a topic id from `topics.md`, or `null` to let the tutor choose | `null` |

## Saving

Save everything in one call:

```bash
python scripts/state.py profile set goal=interview interview_date=2026-12-15 experience=intermediate \
  comfort.basics=solid comfort.linear=some comfort.search-sort=some comfort.trees-graphs=none \
  comfort.recursion-dp=none hint_preference=struggle focus_topic=sliding-window
```

- "skip" for everything: `python scripts/state.py profile defaults`.
- `comfort.all=some` sets every group at once.
- Map loose answers sensibly ("pretty good at arrays" means `comfort.basics=some`
  or `solid`; "trees" as a focus means `focus_topic=trees`). If an answer is truly
  unclear, use the default and say so.
- Unknown interview date: `goal=interview` with no date is fine.

## How the answers are used

- `comfort` = `solid` for a group counts as meeting the prerequisites for topics
  that depend on it, and pushes that group later in recommendations.
- `focus_topic` is served until it reaches *comfortable* (3 unaided solves).
- `hint_preference` = `early`: when the user seems stuck (long silence, the same
  failing test twice), offer a level-1 hint. `struggle`: only give hints when asked.
- `goal` and `interview_date`: mention the time left when it helps, and favour
  timing yourself on medium problems as the date approaches.

## Updating later

"Update my profile" re-asks the questions (show current values as defaults) and
saves the changes with `profile set`. Changing only the focus: `state.py focus TOPIC`.
