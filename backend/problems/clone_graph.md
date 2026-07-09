# Clone Graph

## Problem Statement
Given a reference to a node in a **connected undirected graph**, return a **deep copy** of the graph. Each node has a `val` and a list of `neighbors`. All values are unique.

## Optimal Approach
**BFS / DFS + HashMap (visited clone map)** | Time: O(V + E) | Space: O(V)

Use a `HashMap<Node, Node>` that maps each **original node** to its **cloned node**. This serves two purposes:
1. Tracks which nodes have been visited (prevents infinite loops in cycles).
2. Gives instant access to the cloned node for building neighbor lists.

```java
// Java — BFS (Optimal)
public Node cloneGraph(Node node) {
    if (node == null) return null;
    Map<Node, Node> cloned = new HashMap<>();
    Queue<Node> queue = new LinkedList<>();
    cloned.put(node, new Node(node.val));
    queue.offer(node);
    while (!queue.isEmpty()) {
        Node curr = queue.poll();
        for (Node neighbor : curr.neighbors) {
            if (!cloned.containsKey(neighbor)) {
                cloned.put(neighbor, new Node(neighbor.val));
                queue.offer(neighbor);
            }
            cloned.get(curr).neighbors.add(cloned.get(neighbor));
        }
    }
    return cloned.get(node);
}
```

```java
// Java — DFS Recursive (Also Optimal)
public Node cloneGraph(Node node) {
    if (node == null) return null;
    return dfs(node, new HashMap<>());
}
private Node dfs(Node node, Map<Node, Node> cloned) {
    if (cloned.containsKey(node)) return cloned.get(node);
    Node clone = new Node(node.val);
    cloned.put(node, clone);                   // Store BEFORE visiting neighbors (handles cycles)
    for (Node neighbor : node.neighbors) {
        clone.neighbors.add(dfs(neighbor, cloned));
    }
    return clone;
}
```

```python
# Python — DFS
def cloneGraph(node):
    if not node:
        return None
    cloned = {}
    def dfs(n):
        if n in cloned:
            return cloned[n]
        clone = Node(n.val)
        cloned[n] = clone             # Store before recursing (handles cycles)
        for neighbor in n.neighbors:
            clone.neighbors.append(dfs(neighbor))
        return clone
    return dfs(node)
```

## Common Edge Cases
- **Null input**: Return null immediately.
- **Single node with no neighbors**: Clone it and return — no neighbors to process.
- **Single node with self-loop** (node is its own neighbor): The `cloned.containsKey` check prevents infinite recursion. The clone's neighbor list will contain the clone itself.
- **Graph with cycles**: The visited map is the key — without it, a cycle causes infinite recursion.
- **Disconnected graph**: The problem guarantees a connected graph, so this won't occur here.

## Critical Pattern
**Always insert the clone into the map BEFORE visiting its neighbors.** If you visit neighbors first, a cycle will cause infinite recursion because the current node isn't yet "seen."

```java
// CORRECT order:
Node clone = new Node(node.val);
cloned.put(node, clone);      // ← Register first
for (Node n : node.neighbors) dfs(n, cloned);  // ← Then visit

// WRONG order:
Node clone = new Node(node.val);
for (Node n : node.neighbors) dfs(n, cloned);  // ← Infinite loop on cycles
cloned.put(node, clone);
```

## Key Concepts Tested
- Graph traversal (BFS or DFS)
- HashMap to track visited nodes AND serve as the clone registry
- Handling cycles in graph traversal
- Deep copy semantics: new node objects with the same structure, no shared references

## Verdict Guide
| Approach | Verdict |
|---|---|
| BFS/DFS + HashMap O(V+E)/O(V) | **Optimal** |
| DFS with clone registered after neighbors (infinite loop on cycles) | **Incorrect** |
| Shallow copy (same node references in neighbor lists) | **Incorrect** |
