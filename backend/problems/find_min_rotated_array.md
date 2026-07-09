# Find Minimum in Rotated Sorted Array

## Problem Statement
Given a sorted array that has been rotated between 1 and n times, find the minimum element. All values are unique. Must run in O(log n).

**Example**: `[3,4,5,1,2]` → `1`. `[4,5,6,7,0,1,2]` → `0`.

## Optimal Approach
**Binary Search on the Pivot** | Time: O(log n) | Space: O(1)

The minimum element is at the **rotation pivot** — the only place where `nums[i] < nums[i-1]`.

**Key observation**: If `nums[mid] > nums[right]`, the minimum is in the right half (including `mid+1`). Otherwise the minimum is in the left half (including `mid`).

```java
// Java — Optimal
public int findMin(int[] nums) {
    int left = 0, right = nums.length - 1;
    while (left < right) {           // Note: strict < not <=
        int mid = left + (right - left) / 2;
        if (nums[mid] > nums[right]) {
            left = mid + 1;          // Min is in right half
        } else {
            right = mid;             // Mid could be the min — don't exclude it
        }
    }
    return nums[left];               // left == right == min index
}
```

```python
# Python — Optimal
def findMin(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]
```

**Why compare with `nums[right]` and not `nums[left]`?**
Comparing with `nums[right]` is cleaner because:
- If `nums[mid] > nums[right]` → we crossed the pivot going left-to-mid, so min is to the right.
- If `nums[mid] <= nums[right]` → the right side including mid is sorted, min could be at mid or to its left.

## Suboptimal Approaches
- **Linear scan O(n)**: Just find the minimum. Correct but ignores the sorted structure — doesn't meet O(log n) requirement.
- **Find pivot then return nums[pivot]**: Also O(log n) but split into two steps — more code than needed.

## Common Edge Cases
- **Not rotated at all** (e.g., `[1,2,3,4,5]`): `nums[mid]` is always ≤ `nums[right]`, so `right` keeps shrinking to 0. Returns `nums[0]` correctly.
- **Rotated by 1** (e.g., `[2,1]`): `left=0, right=1, mid=0`. `nums[0]=2 > nums[1]=1` → `left=1`. Loop ends, return `nums[1]=1`. Correct.
- **Single element**: Returns it immediately.
- **Two elements**: Handled correctly by the `left < right` loop condition.
- **`while left <= right` bug**: Using `<=` with `right = mid` causes an infinite loop when `left == right == mid`. Always use strict `<` when `right = mid` (not `mid - 1`).

## Key Concepts Tested
- Binary search variant — search for a property (the pivot point), not a value
- Why `right = mid` instead of `mid - 1`: we don't exclude `mid` because it could itself be the minimum
- Why `left < right` instead of `left <= right`: the loop terminates when they meet, which is the answer
- Compare `nums[mid]` vs `nums[right]` — this is simpler than comparing with `nums[left]`

## Verdict Guide
| Approach | Verdict |
|---|---|
| Binary search O(log n)/O(1) | **Optimal** |
| Linear scan O(n) | **Suboptimal** |
| Binary search with `while left <= right` and `right = mid` → infinite loop | **Incorrect** |
