# Balanced Brackets

**Topic:** Stacks · **Difficulty:** Easy

`code` contains only the characters `()[]{}`. It is **balanced** if every opening
bracket is closed by the same kind of bracket, and brackets close in the reverse
order they were opened (so `([)]` is not balanced).

Return `True` if `code` is balanced. The empty string is balanced.

## Examples

**Example 1**

```text
Input:  code = "{[()]}()"
Output: True
```

**Example 2**

```text
Input:  code = "([)]"
Output: False
```

`[` is opened after `(`, so it must close first.

**Example 3**

```text
Input:  code = ""
Output: True
```

## Constraints

- 0 <= len(code) <= 10^5
- code contains only ()[]{}

## Signature

```python
def is_balanced(code: str) -> bool:
```

## Your solution

Write it in `workspace/balanced-brackets/solution.py`, then run the tests:

```bash
python scripts/run_tests.py balanced-brackets
```
