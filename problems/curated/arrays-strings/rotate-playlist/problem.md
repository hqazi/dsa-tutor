# Rotate the Playlist

**Topic:** Arrays & strings · **Difficulty:** Easy

A music app shows a playlist as a list of track ids. Each press of the **shift**
button moves the last track to the front of the playlist.

Given `tracks` and the number of presses `k`, return the playlist after all `k`
presses as a new list. `k` can be much larger than the number of tracks.

## Examples

**Example 1**

```text
Input:  tracks = [1, 2, 3, 4, 5], k = 2
Output: [4, 5, 1, 2, 3]
```

After one press: `[5, 1, 2, 3, 4]`; after two: `[4, 5, 1, 2, 3]`.

**Example 2**

```text
Input:  tracks = [7, 8], k = 5
Output: [8, 7]
```

Five presses on two tracks is the same as one press.

## Constraints

- 0 <= len(tracks) <= 10^5
- 0 <= k <= 10^9
- track ids are integers

## Signature

```python
def shift_playlist(tracks: list[int], k: int) -> list[int]:
```

## Your solution

Write it in `workspace/rotate-playlist/solution.py`, then run the tests:

```bash
python scripts/run_tests.py rotate-playlist
```
