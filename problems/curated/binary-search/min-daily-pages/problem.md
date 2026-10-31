# Pages Per Day

**Topic:** Binary search · **Difficulty:** Medium

You will read a book's chapters **in order**; `chapters[i]` is the number of pages
in chapter `i`. Each day you read some whole chapters (never splitting one across
days), and you must finish within `days` days.

Return the smallest daily page limit that makes this possible.

## Examples

**Example 1**

```text
Input:  chapters = [3, 2, 2, 4, 1, 4], days = 3
Output: 6
```

Read `[3, 2]`, `[2, 4]`, `[1, 4]`: the busiest day is 6 pages.

**Example 2**

```text
Input:  chapters = [1, 2, 3, 1, 1], days = 4
Output: 3
```

## Constraints

- 1 <= days <= len(chapters) <= 10^5
- 1 <= chapters[i] <= 10^4

## Signature

```python
def min_daily_pages(chapters: list[int], days: int) -> int:
```

## Your solution

Write it in `workspace/min-daily-pages/solution.py`, then run the tests:

```bash
python scripts/run_tests.py min-daily-pages
```
