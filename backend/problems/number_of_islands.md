# Number of Islands

## Problem Statement
Given an `m x n` 2D binary grid where `'1'` = land and `'0'` = water, return the number of islands. An island is surrounded by water and formed by connecting adjacent land cells horizontally or vertically.

## Optimal Approach
**DFS Flood Fill** | Time: O(m × n) | Space: O(m × n) worst case call stack

Scan the grid. When you find a `'1'` (unvisited land), increment the island count and run DFS to sink the entire connected island (mark all its cells as `'0'` or visited so they're not counted again).

```java
// Java — DFS (Optimal)
public int numIslands(char[][] grid) {
    int count = 0;
    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == '1') {
                count++;
                dfs(grid, i, j);
            }
        }
    }
    return count;
}
private void dfs(char[][] grid, int i, int j) {
    if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] != '1') return;
    grid[i][j] = '0';       // Sink this land cell (mark visited)
    dfs(grid, i + 1, j);
    dfs(grid, i - 1, j);
    dfs(grid, i, j + 1);
    dfs(grid, i, j - 1);
}
```

```python
# Python — DFS
def numIslands(grid):
    if not grid:
        return 0
    count = 0
    def dfs(i, j):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] != '1':
            return
        grid[i][j] = '0'
        dfs(i+1, j); dfs(i-1, j); dfs(i, j+1); dfs(i, j-1)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    return count
```

## Alternative Approach (BFS)
**Time: O(m × n) | Space: O(min(m, n))** — iterative, avoids deep recursion stack.

```java
public int numIslands(char[][] grid) {
    int count = 0;
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == '1') {
                count++;
                Queue<int[]> queue = new LinkedList<>();
                queue.offer(new int[]{i, j});
                grid[i][j] = '0';
                while (!queue.isEmpty()) {
                    int[] cell = queue.poll();
                    for (int[] d : dirs) {
                        int ni = cell[0] + d[0], nj = cell[1] + d[1];
                        if (ni >= 0 && ni < grid.length && nj >= 0 && nj < grid[0].length && grid[ni][nj] == '1') {
                            grid[ni][nj] = '0';
                            queue.offer(new int[]{ni, nj});
                        }
                    }
                }
            }
        }
    }
    return count;
}
```

## Common Edge Cases
- **Empty grid**: Return 0. Check `if (grid == null || grid.length == 0)`.
- **All water**: Count stays 0.
- **All land** (one big island): DFS from first cell sinks everything — count = 1.
- **Single cell grid**: Works correctly.
- **Diagonal adjacency doesn't count**: The problem says horizontal/vertical only — 4-directional DFS is correct, NOT 8-directional.
- **Modifying input**: The DFS approach modifies the grid (sinks cells). If input modification is not allowed, use a separate `visited` boolean array instead.

## Key Concepts Tested
- Graph traversal (DFS/BFS) on a 2D grid — the most common graph problem format
- Flood fill pattern — mark visited nodes to avoid reprocessing
- 4-directional movement (up, down, left, right)
- Boundary checking before recursive calls
- This is the foundation for: surrounded regions, max area of island, pacific atlantic water flow

## Verdict Guide
| Approach | Verdict |
|---|---|
| DFS flood fill O(mn)/O(mn) | **Optimal** |
| BFS flood fill O(mn)/O(min(m,n)) | **Optimal** |
| Union-Find O(mn)/O(mn) | **Acceptable** (advanced) |
| 8-directional DFS (includes diagonals) | **Incorrect** |
| Not marking visited cells (infinite recursion) | **Incorrect** |
