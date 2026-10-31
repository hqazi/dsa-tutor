# Collapse Matching Neighbours

**Topic:** Stacks · **Difficulty:** Easy

Repeatedly delete two **adjacent equal letters** from `s` until no such pair is
left. Removing a pair can bring two new letters next to each other, and they may
then be removed too. Return the final string (the result does not depend on the
order of removals).

## Examples

**Example 1**

```text
Input:  s = "abbaca"
Output: "ca"
```

Remove `bb` to get `aaca`, then `aa` to get `ca`.

**Example 2**

```text
Input:  s = "azxxzy"
Output: "ay"
```

## Constraints

- 0 <= len(s) <= 10^5
- s contains only lowercase English letters

## Signature

```python
def collapse_pairs(s: str) -> str:
```

## Your solution

Write it in `workspace/collapse-pairs/solution.py`, then run the tests:

```bash
python scripts/run_tests.py collapse-pairs
```
