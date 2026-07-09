# Reverse Linked List

## Problem Statement
Given the head of a singly linked list, reverse the list in-place and return the new head.

## Optimal Approach
**Iterative — Three Pointers** | Time: O(n) | Space: O(1)

Use three pointers: `prev = null`, `curr = head`, `next = null`. In each iteration:
1. Save `next = curr.next` (before breaking the link)
2. Reverse the link: `curr.next = prev`
3. Advance both pointers: `prev = curr`, `curr = next`

At the end, `curr == null` and `prev` is the new head.

```java
// Java — Optimal (Iterative)
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    while (curr != null) {
        ListNode next = curr.next;   // Save before breaking link
        curr.next = prev;            // Reverse the link
        prev = curr;                 // Move prev forward
        curr = next;                 // Move curr forward
    }
    return prev;                     // prev is now the new head
}
```

```python
# Python — Optimal (Iterative)
def reverseList(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

## Alternative Approach (Recursive)
**Time: O(n) | Space: O(n)** — recursion stack depth equals list length.

```java
// Java — Recursive (Acceptable, O(n) stack space)
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode newHead = reverseList(head.next);
    head.next.next = head;   // Point next node back to current
    head.next = null;        // Break forward link (make current the new tail)
    return newHead;
}
```

The recursive approach is elegant but uses O(n) stack space — risky for very large lists (stack overflow). In interviews, mention both but prefer iterative if not told otherwise.

## Suboptimal Approaches
- **Collect values into array, rebuild list**: O(n) time, O(n) space. Technically works but defeats the purpose of "in-place" reversal. In an interview, this signals you don't understand pointer manipulation.
- **Using a stack**: O(n) time, O(n) space. Same issue — extra data structure where O(1) is achievable.

## Common Edge Cases
- **Empty list** (`head == null`) → return null. Both iterative and recursive handle this.
- **Single node** → return head unchanged. `prev` remains the same as `head` after one iteration.
- **Two-node list** (`1 → 2 → null`) → verify manually: `prev=null, curr=1`; step1: next=2, 1.next=null, prev=1, curr=2; step2: next=null, 2.next=1, prev=2, curr=null. Return 2 → correct.
- **Forgetting to set `head.next = null`** in recursive approach → the original head still points forward → creates a cycle.
- **Forgetting `if head.next == null`** base case in recursive → `head.next.next` throws NullPointerException.

## Key Concepts Tested
- In-place pointer manipulation (no extra data structure)
- Iterative vs. recursive tradeoff (time same, space O(1) vs O(n))
- Order of pointer operations: save next BEFORE breaking the link
- Understanding that `prev = null` is correct — the original head becomes the new tail, so its `next` must be `null`

## Verdict Guide
| Approach | Verdict |
|---|---|
| Iterative three-pointer O(n)/O(1) | **Optimal** |
| Recursive O(n)/O(n) | **Acceptable** |
| Collect into array and rebuild O(n)/O(n) | **Suboptimal** |
| Stack-based O(n)/O(n) | **Suboptimal** |
| Incorrect pointer order (loses nodes) | **Incorrect** |
