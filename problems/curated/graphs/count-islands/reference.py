def count_islands(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    seen = [[False] * cols for _ in range(rows)]
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not seen[r][c]:
                islands += 1
                seen[r][c] = True
                stack = [(r, c)]
                while stack:
                    y, x = stack.pop()
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 1 and not seen[ny][nx]:
                            seen[ny][nx] = True
                            stack.append((ny, nx))
    return islands
