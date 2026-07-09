# Linked List Cycle (Detect Cycle)

## Problem Statement
Given the `head` of a linked list, determine if it has a cycle. A cycle exists if some node's `next` pointer points back to a previous node. Return `true` if a cycle exists, `false` otherwise.

## Optimal Approach
**Floyd's Cycle Detection — Slow & Fast Pointers** | Time: O(n) | Space: O(1)

Use two pointers: `slow` moves 1 step at a time, `fast` moves 2 steps. If there's a cycle, `fast` will eventually lap `slow` and they'll meet. If `fast` reaches null, there's no cycle.

**Intuition**: Think of a circular track. A faster runner will always lap a slower runner.

```java
// Java — Optimal (Floyd's)
public boolean hasCycle(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;   // Pointers met — cycle exists
    }
    return false;
}
```

```python
# Python — Optimal (Floyd's)
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

## Suboptimal Approach
**HashSet — Visited Nodes** | Time: O(n) | Space: O(n)

Store each visited node. If you see a node again, there's a cycle.

```java
// Java — HashSet (Acceptable but O(n) space)
public boolean hasCycle(ListNode head) {
    Set<ListNode> visited = new HashSet<>();
    while (head != null) {
        if (visited.contains(head)) return true;
        visited.add(head);
        head = head.next;
    }
    return false;
}
```

## Common Edge Cases
- **Empty list** (`head == null`): `fast == null` → loop doesn't run → return `false`. ✓
- **Single node, no cycle** (`head.next == null`): `fast.next == null` → loop doesn't run → return `false`. ✓
- **Single node pointing to itself** (cycle of length 1): `fast = head.next.next = head`. `slow = head.next = head`. They meet on first iteration → return `true`. ✓
- **Cycle at the tail**: The most common case — last node points to some earlier node.
- **No cycle, long list**: `fast` reaches null naturally.

## Critical Bug Patterns
- Checking `fast.next != null` BEFORE `fast.next.next`: If you do `fast = fast.next.next` without first checking `fast.next != null`, you'll get a NullPointerException when `fast` is at the second-to-last node.
- Using `slow == fast` before moving pointers: Both start at `head`, so checking equality before the first move would always return `true`.
- Comparing values (`slow.val == fast.val`) instead of references (`slow == fast`): Different nodes can have the same value — you must compare node identity.

## Key Concepts Tested
- Floyd's Cycle Detection Algorithm (also called the "tortoise and hare" algorithm)
- Two-pointer technique for cycle problems
- O(1) space vs O(n) space tradeoff
- Node identity comparison (`==`) vs value comparison (`.val ==`)

## Verdict Guide
| Approach | Verdict |
|---|---|
| Floyd's slow/fast pointers O(n)/O(1) | **Optimal** |
| HashSet of visited nodes O(n)/O(n) | **Acceptable** |
| Marking nodes as visited by mutating values | **Incorrect** (modifies input) |
| Comparing `.val` instead of node reference | **Incorrect** |
