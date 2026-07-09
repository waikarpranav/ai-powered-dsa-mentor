# Merge Two Sorted Lists

## Problem Statement
You are given the heads of two sorted linked lists `list1` and `list2`. Merge them into one sorted linked list by splicing together the nodes (not creating new ones). Return the head of the merged list.

## Optimal Approach
**Iterative with Dummy Node** | Time: O(m + n) | Space: O(1)

Use a `dummy` node as a fake head so you never need special-case logic for the first node. Maintain a `curr` pointer that builds the merged list.

At each step, pick the smaller of `list1.val` and `list2.val`, attach it to `curr.next`, and advance that list's pointer.

```java
// Java — Optimal (Iterative)
public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
    ListNode dummy = new ListNode(0);   // Fake head
    ListNode curr = dummy;
    while (list1 != null && list2 != null) {
        if (list1.val <= list2.val) {
            curr.next = list1;
            list1 = list1.next;
        } else {
            curr.next = list2;
            list2 = list2.next;
        }
        curr = curr.next;
    }
    // Attach the remaining non-null list
    curr.next = (list1 != null) ? list1 : list2;
    return dummy.next;
}
```

```python
# Python — Optimal (Iterative)
def mergeTwoLists(list1, list2):
    dummy = ListNode(0)
    curr = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next
    curr.next = list1 if list1 else list2
    return dummy.next
```

## Alternative Approach (Recursive)
**Time: O(m + n) | Space: O(m + n)** — elegant but uses call stack.

```java
// Java — Recursive (Acceptable)
public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
    if (list1 == null) return list2;
    if (list2 == null) return list1;
    if (list1.val <= list2.val) {
        list1.next = mergeTwoLists(list1.next, list2);
        return list1;
    } else {
        list2.next = mergeTwoLists(list1, list2.next);
        return list2;
    }
}
```

## Suboptimal Approaches
- **Collect all values, sort, rebuild**: O((m+n) log(m+n)) time, O(m+n) space — defeats the purpose of merging sorted lists.
- **Creating new nodes**: O(m+n) time and space — correct but wasteful. The problem says "splice together the nodes of the first two lists."

## Common Edge Cases
- **Both lists empty**: Returns `null`. `dummy.next` is null.
- **One list empty** (e.g., `list1 = null`): The while loop doesn't execute. `curr.next = list2`. Returns `list2` directly.
- **Lists of different lengths**: The `curr.next = list1 or list2` line handles the remaining tail without any loop — this is the key insight.
- **All elements of one list are smaller**: Works correctly — one list gets exhausted first, the other is attached as a tail.
- **Duplicate values across lists**: `<=` in the comparison ensures stable ordering (list1 elements come first on ties).

## Key Concepts Tested
- Dummy node pattern — eliminates edge cases for the head pointer
- In-place pointer splicing (no new nodes created)
- The tail-attachment trick: `curr.next = remaining` avoids an extra loop
- Recursive vs iterative tradeoff: both O(m+n) time, but recursive uses O(m+n) stack space

## Verdict Guide
| Approach | Verdict |
|---|---|
| Iterative with dummy node O(m+n)/O(1) | **Optimal** |
| Recursive O(m+n)/O(m+n) | **Acceptable** |
| Collect + sort + rebuild O((m+n)log(m+n)) | **Suboptimal** |
| Creating new nodes instead of splicing | **Suboptimal** |
