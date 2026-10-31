# Topics

The scripts parse the table below. Each row needs an `id`, a `group`, and the
ids of its prerequisites (`-` for none). Topics are listed in teaching order;
when several topics are equally weak, the one listed first wins.

| id | name | group | prerequisites | key patterns |
|---|---|---|---|---|
| arrays-strings | Arrays & strings | basics | - | indexing, in-place updates, building results |
| hashing | Hash maps & sets | basics | arrays-strings | counting, seen-set, complement lookup |
| two-pointers | Two pointers | basics | arrays-strings | converging ends, fast/slow, merging |
| sliding-window | Sliding window | basics | two-pointers, hashing | fixed window, grow/shrink window |
| prefix-sums | Prefix sums | basics | arrays-strings | running totals, range sums, sum-to-count maps |
| stack | Stacks | linear | arrays-strings | matching pairs, monotonic stack, expression evaluation |
| linked-list | Linked lists | linear | arrays-strings | pointer rewiring, dummy head, fast/slow pointers |
| binary-search | Binary search | search-sort | arrays-strings | lower bound, search on the answer, rotated arrays |
| sorting | Sorting & intervals | search-sort | arrays-strings | custom keys, interval merging, sweep line |
| recursion-backtracking | Recursion & backtracking | recursion-dp | arrays-strings | choose/explore/undo, pruning |
| trees | Binary trees | trees-graphs | recursion-backtracking | DFS, BFS by level, BST invariants |
| heaps | Heaps | trees-graphs | sorting | top-k, k-way merge, running min/max |
| graphs | Graphs | trees-graphs | trees, hashing | grid BFS/DFS, connected components, topological order |
| greedy | Greedy | recursion-dp | sorting | exchange argument, earliest finish, reach |
| dynamic-programming | Dynamic programming | recursion-dp | recursion-backtracking | 1-D/2-D tables, choose-or-skip, unbounded choices |

## Groups

Onboarding asks for comfort (`none` / `some` / `solid`) per group, not per topic.

| group | covers |
|---|---|
| basics | arrays & strings, hashing, two pointers, sliding window, prefix sums |
| linear | stacks, linked lists |
| search-sort | binary search, sorting & intervals |
| trees-graphs | binary trees, heaps, graphs |
| recursion-dp | recursion & backtracking, greedy, dynamic programming |

A group rated `solid` counts as meeting the prerequisite for topics that depend
on it, so confident learners are not forced through the basics first.

## Difficulty

- **easy**: one standard pattern applied directly; small edge-case surface.
- **medium**: a pattern plus one twist (a second data structure, search on the
  answer, a non-obvious invariant), or a careful edge-case surface.
- **hard**: allowed for generated problems on request; never recommended automatically in v1.
