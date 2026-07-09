# Validate Binary Search Tree

## Problem Statement
Given the `root` of a binary tree, determine if it is a valid BST. A valid BST requires:
- Every node in the **left subtree** has a value **strictly less than** the current node.
- Every node in the **right subtree** has a value **strictly greater than** the current node.
- Both subtrees must also be valid BSTs.

## Optimal Approach
**Recursive with Min/Max Bounds** | Time: O(n) | Space: O(h)

Pass down a `(min, max)` range for each node. A node is valid if `min < node.val < max`.

- Root: range is `(-∞, +∞)`
- Going **left**: upper bound becomes `node.val`
- Going **right**: lower bound becomes `node.val`

```java
// Java — Optimal
public boolean isValidBST(TreeNode root) {
    return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
}
private boolean validate(TreeNode node, long min, long max) {
    if (node == null) return true;
    if (node.val <= min || node.val >= max) return false;
    return validate(node.left,  min,       node.val) &&
           validate(node.right, node.val,  max);
}
```

```python
# Python — Optimal
def isValidBST(root):
    def validate(node, min_val, max_val):
        if not node:
            return True
        if node.val <= min_val or node.val >= max_val:
            return False
        return validate(node.left, min_val, node.val) and \
               validate(node.right, node.val, max_val)
    return validate(root, float('-inf'), float('inf'))
```

**Why `Long.MIN_VALUE`/`Long.MAX_VALUE` instead of `Integer`?** Because node values can equal `Integer.MIN_VALUE` or `Integer.MAX_VALUE`. Using Integer bounds would incorrectly reject valid trees with extreme values.

## Alternative Approach (Inorder Traversal)
A valid BST's inorder traversal produces strictly increasing values.

```java
// Java — Inorder check
private Integer prev = null;
public boolean isValidBST(TreeNode root) {
    if (root == null) return true;
    if (!isValidBST(root.left)) return false;
    if (prev != null && root.val <= prev) return false;
    prev = root.val;
    return isValidBST(root.right);
}
```

## The Classic Wrong Approach
❌ **Only checking immediate children**:
```java
// WRONG — this is NOT sufficient
if (root.left != null && root.left.val >= root.val) return false;
if (root.right != null && root.right.val <= root.val) return false;
```
This fails for trees like:
```
    5
   / \
  1   4
     / \
    3   6
```
Node 3 is in the right subtree of 5, so it must be > 5. But the local check only verifies 3 < 4 (its parent). The min/max bounds approach catches this.

## Common Edge Cases
- **Single node**: Always valid. `validate(node, -∞, +∞)` → no violation possible.
- **Duplicate values**: BST requires **strictly** less/greater. Duplicates make it invalid. The `<=` and `>=` checks catch this.
- **Node value equals `Integer.MIN_VALUE`**: Use `Long` bounds or `null` sentinels instead of Integer bounds.
- **Left-skewed or right-skewed valid BSTs**: Work correctly.
- **Tree with values that look locally valid but violate the global BST property**: The min/max bounds approach is specifically designed to catch this (see the classic wrong approach above).

## Key Concepts Tested
- BST property applies globally (all nodes in subtree), not just locally (parent-child pair)
- Passing validity bounds down the recursion — a fundamental tree recursion pattern
- Why inorder traversal of a BST is sorted — used here as an alternative check
- Using `Long` instead of `Integer` to avoid boundary value bugs

## Verdict Guide
| Approach | Verdict |
|---|---|
| Min/max bounds recursion O(n)/O(h) | **Optimal** |
| Inorder traversal check O(n)/O(h) | **Optimal** |
| Only checking immediate children (local check) | **Incorrect** |
| Using Integer.MIN/MAX_VALUE bounds | **Incorrect** for edge cases |
