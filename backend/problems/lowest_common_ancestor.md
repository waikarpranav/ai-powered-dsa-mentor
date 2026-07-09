# Lowest Common Ancestor of a BST

## Problem Statement
Given a BST and two nodes `p` and `q`, find their Lowest Common Ancestor (LCA). The LCA is the deepest node that is an ancestor of both `p` and `q`. A node is a descendant of itself.

## Optimal Approach
**BST Property — Single Pass** | Time: O(h) | Space: O(1) iterative / O(h) recursive

Use the BST property: if both `p` and `q` are less than the current node, go left. If both are greater, go right. Otherwise (one is smaller, one is larger — or one equals the current node), the current node IS the LCA.

```java
// Java — Iterative (Optimal, O(1) space)
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    while (root != null) {
        if (p.val < root.val && q.val < root.val) {
            root = root.left;       // Both in left subtree
        } else if (p.val > root.val && q.val > root.val) {
            root = root.right;      // Both in right subtree
        } else {
            return root;            // Split point — this is the LCA
        }
    }
    return null;
}
```

```java
// Java — Recursive (Also Optimal, cleaner)
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (p.val < root.val && q.val < root.val) return lowestCommonAncestor(root.left, p, q);
    if (p.val > root.val && q.val > root.val) return lowestCommonAncestor(root.right, p, q);
    return root;
}
```

```python
# Python — Iterative
def lowestCommonAncestor(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None
```

## Important Distinction — LCA of a Regular Binary Tree
For a **plain binary tree** (not a BST), you CANNOT use the BST property. Instead use:

```java
// For plain binary tree — O(n) time
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left  = lowestCommonAncestor(root.left,  p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if (left != null && right != null) return root;   // p and q on different sides
    return left != null ? left : right;               // Both on same side
}
```

The problem here is specifically a **BST**, so always use the BST property approach.

## Common Edge Cases
- **One node is the ancestor of the other**: e.g., `p = root`. The `return root` condition (when `p.val == root.val`) correctly returns `root` as the LCA.
- **Both nodes are the same**: Returns that node. Works correctly since neither `<` condition fires.
- **Nodes are on opposite sides of root**: The first comparison returns root immediately.
- **Problem guarantees p and q exist in the BST**: No need to handle "not found."

## Key Concepts Tested
- Exploiting BST structure to get O(h) instead of O(n)
- Understanding "split point" = LCA in a BST
- Knowing the difference between LCA in a BST vs LCA in a general binary tree
- O(1) space with the iterative approach vs O(h) with recursion

## Verdict Guide
| Approach | Verdict |
|---|---|
| BST property iterative O(h)/O(1) | **Optimal** |
| BST property recursive O(h)/O(h) | **Optimal** |
| General binary tree LCA O(n)/O(h) used on BST | **Acceptable** (correct but ignores BST property) |
| Brute force (find paths from root to each node, find divergence) | **Acceptable** but verbose |
