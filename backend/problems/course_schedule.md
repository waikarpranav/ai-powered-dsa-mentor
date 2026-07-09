# Course Schedule

## Problem Statement
There are `numCourses` courses labeled `0` to `numCourses-1`. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` means you must take course `b` before course `a`. Return `true` if you can finish all courses, `false` otherwise.

This is a **cycle detection problem on a directed graph**. If a cycle exists in the prerequisite graph → impossible to finish all courses.

## Optimal Approach
**DFS Cycle Detection with 3-State Coloring** | Time: O(V + E) | Space: O(V + E)

Assign each node one of 3 states:
- `0` = unvisited
- `1` = visiting (currently in DFS stack — on the current path)
- `2` = visited (fully processed — safe)

A cycle exists if DFS reaches a node with state `1` (already on the current path).

```java
// Java — DFS with 3-state coloring (Optimal)
public boolean canFinish(int numCourses, int[][] prerequisites) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
    for (int[] pre : prerequisites) adj.get(pre[0]).add(pre[1]);

    int[] state = new int[numCourses]; // 0=unvisited, 1=visiting, 2=visited

    for (int i = 0; i < numCourses; i++) {
        if (state[i] == 0 && hasCycle(adj, state, i)) return false;
    }
    return true;
}
private boolean hasCycle(List<List<Integer>> adj, int[] state, int node) {
    state[node] = 1;   // Mark as visiting
    for (int neighbor : adj.get(node)) {
        if (state[neighbor] == 1) return true;   // Back edge = cycle
        if (state[neighbor] == 0 && hasCycle(adj, state, neighbor)) return true;
    }
    state[node] = 2;   // Mark as fully visited
    return false;
}
```

```python
# Python — DFS with 3-state coloring
def canFinish(numCourses, prerequisites):
    adj = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        adj[a].append(b)
    state = [0] * numCourses  # 0=unvisited, 1=visiting, 2=done

    def has_cycle(node):
        if state[node] == 1: return True
        if state[node] == 2: return False
        state[node] = 1
        for neighbor in adj[node]:
            if has_cycle(neighbor):
                return True
        state[node] = 2
        return False

    return all(not has_cycle(i) for i in range(numCourses) if state[i] == 0)
```

## Alternative Approach (Topological Sort — BFS/Kahn's Algorithm)
**Time: O(V + E) | Space: O(V + E)**

If a valid topological ordering exists, there's no cycle. Use BFS with in-degree counts.

```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    int[] inDegree = new int[numCourses];
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
    for (int[] pre : prerequisites) {
        adj.get(pre[1]).add(pre[0]);
        inDegree[pre[0]]++;
    }
    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < numCourses; i++) if (inDegree[i] == 0) queue.offer(i);
    int processed = 0;
    while (!queue.isEmpty()) {
        int node = queue.poll();
        processed++;
        for (int neighbor : adj.get(node)) {
            if (--inDegree[neighbor] == 0) queue.offer(neighbor);
        }
    }
    return processed == numCourses;  // All courses processed = no cycle
}
```

## Common Edge Cases
- **No prerequisites**: Return `true` — no graph edges, no cycle.
- **Self-loop** (e.g., `[0, 0]`): Course 0 requires itself — cycle → `false`.
- **Disconnected graph**: Outer loop iterates all nodes, so disconnected components are checked.
- **Cycle of length 2** (e.g., `[0,1], [1,0]`): A↔B — detected by the `state == 1` check.
- **numCourses = 1, no prerequisites**: Return `true`.

## Key Concepts Tested
- Directed graph cycle detection
- 3-state DFS coloring (vs 2-state which works only for undirected graphs)
- Building an adjacency list from an edge list
- Topological sort as an alternative cycle detection method
- Why 2-state (visited/unvisited) fails for directed graphs: a node can be visited via multiple paths without a cycle

## Verdict Guide
| Approach | Verdict |
|---|---|
| DFS 3-state coloring O(V+E)/O(V+E) | **Optimal** |
| BFS Kahn's topological sort O(V+E)/O(V+E) | **Optimal** |
| DFS with only 2 states (visited/unvisited) on directed graph | **Incorrect** (false positives) |
| Checking only immediate prerequisites (not full graph) | **Incorrect** |
