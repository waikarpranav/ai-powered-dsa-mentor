# Maximum Depth of Binary Tree

## Problem Statement
Given the `root` of a binary tree, return its maximum depth — the number of nodes along the longest path from the root down to the farthest leaf.

## Optimal Approach
**Recursive DFS (Post-order)** | Time: O(n) | Space: O(h)

The depth of a tree = `1 + max(depth of left subtree, depth of right subtree)`. This is naturally recursive.

```java
// Java — Recursive DFS (Optimal, clean)
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
```

```python
# Python — Recursive DFS
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

## Alternative Approach (Iterative BFS — Level Order)
**Time: O(n) | Space: O(w)** where w = max width of tree.

Count levels using a queue. Each level processed = +1 depth.

```java
// Java — BFS (Iterative)
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    int depth = 0;
    while (!queue.isEmpty()) {
        depth++;
        int levelSize = queue.size();
        for (int i = 0; i < levelSize; i++) {
            TreeNode node = queue.poll();
            if (node.left  != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
    }
    return depth;
}
```

## Alternative Approach (Iterative DFS with Stack)
**Time: O(n) | Space: O(h)**

```java
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    Deque<int[]> stack = new ArrayDeque<>();  // [node, depth]
    stack.push(new int[]{0, 1});              // Can't push TreeNode here, use pair
    // Simpler: use two stacks or a custom Pair class
    // BFS is cleaner for this — use BFS iterative instead
}
```

## Common Edge Cases
- **Empty tree** (`root == null`): Return 0. Base case handles it.
- **Single node**: Left and right are both null → `1 + max(0, 0) = 1`. Correct.
- **Left-skewed tree** (only left children): Recursion depth = n. Stack overflow risk for very large n in recursive approach. BFS avoids this.
- **Balanced tree**: Recursion depth = log n. Safe.
- **Root with only one child**: `max(depth, 0)` correctly ignores the missing side.

## Key Concepts Tested
- Post-order DFS: process children before parent
- Recognizing the recursive structure: tree depth = 1 + max(left depth, right depth)
- BFS for level-order problems — counting levels = counting depth
- Space complexity: recursive = O(h) call stack, BFS = O(w) queue where w is max width

## Verdict Guide
| Approach | Verdict |
|---|---|
| Recursive DFS O(n)/O(h) | **Optimal** |
| Iterative BFS O(n)/O(w) | **Optimal** |
| Iterative DFS with stack O(n)/O(h) | **Acceptable** |
| Returning `max(left, right)` without `+1` | **Incorrect** |
