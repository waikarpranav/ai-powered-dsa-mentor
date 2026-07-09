# Binary Tree Inorder Traversal

## Problem Statement
Given the `root` of a binary tree, return the **inorder traversal** of its nodes' values.
Inorder = Left → Root → Right.

## Optimal Approach
**Iterative with Stack** | Time: O(n) | Space: O(h) where h = tree height

Simulate the recursion manually using a stack. Push all left nodes onto the stack, then process the top, then move to the right subtree.

```java
// Java — Iterative (Optimal / Preferred in interviews)
public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        // Go as far left as possible
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        // Process the node
        curr = stack.pop();
        result.add(curr.val);
        // Move to right subtree
        curr = curr.right;
    }
    return result;
}
```

```python
# Python — Iterative
def inorderTraversal(root):
    result, stack = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result
```

## Alternative Approach (Recursive)
**Time: O(n) | Space: O(h)** — simpler code, same complexity.

```java
// Java — Recursive
public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    inorder(root, result);
    return result;
}
private void inorder(TreeNode node, List<Integer> result) {
    if (node == null) return;
    inorder(node.left, result);
    result.add(node.val);
    inorder(node.right, result);
}
```

**Note**: Recursive is simpler to write but iterative demonstrates deeper understanding of how the call stack works — preferred in senior-level interviews.

## Suboptimal Approaches
- **Morris Traversal**: O(n) time, O(1) space — modifies tree pointers temporarily. Impressive if known, but very hard to implement correctly under pressure.

## Common Edge Cases
- **Empty tree** (`root == null`): Returns empty list. Both approaches handle this — the while loop condition handles null root.
- **Single node**: Returns `[root.val]`. No left or right children.
- **Left-skewed tree** (e.g., only left children): Stack grows to O(n). Still works correctly.
- **Right-skewed tree**: Each node has only a right child. Stack stays size 1 throughout.
- **BST**: Inorder traversal of a BST produces values in sorted order — a key property often tested.

## Key Concepts Tested
- Inorder = Left, Root, Right (memorize: Pre = Root first, In = Root middle, Post = Root last)
- Iterative simulation of recursion using an explicit stack
- For a BST: inorder gives sorted output — this is tested in Validate BST and other problems
- Space complexity: O(h) where h is height. O(log n) for balanced, O(n) for skewed.

## Verdict Guide
| Approach | Verdict |
|---|---|
| Iterative with explicit stack O(n)/O(h) | **Optimal** |
| Recursive O(n)/O(h) | **Acceptable** |
| Morris Traversal O(n)/O(1) | **Optimal** (bonus — rarely expected) |
| Wrong traversal order (e.g., preorder instead) | **Incorrect** |
