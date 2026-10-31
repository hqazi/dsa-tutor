# Can You Finish Every Course?

**Topic:** Graphs · **Difficulty:** Medium

There are `courses` courses numbered `0` to `courses - 1`. Each pair `[a, b]` in
`prereqs` means course `b` must be completed **before** course `a`.

Return `True` if some order lets you finish every course, i.e. the prerequisites
contain no cycle.

## Examples

**Example 1**

```text
Input:  courses = 2, prereqs = [[1, 0]]
Output: True
```

**Example 2**

```text
Input:  courses = 2, prereqs = [[1, 0], [0, 1]]
Output: False
```

Each course needs the other first, so neither can start.

## Constraints

- 1 <= courses <= 10^5
- 0 <= len(prereqs) <= 10^5
- 0 <= a, b < courses

## Signature

```python
def can_finish(courses: int, prereqs: list[list[int]]) -> bool:
```

## Your solution

Write it in `workspace/course-plan/solution.py`, then run the tests:

```bash
python scripts/run_tests.py course-plan
```
