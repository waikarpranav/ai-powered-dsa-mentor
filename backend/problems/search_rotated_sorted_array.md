# Search in Rotated Sorted Array

## Problem Statement
A sorted array has been rotated at some unknown pivot. Given the rotated array `nums` (all unique values) and a `target`, return its index or `-1` if not found. Must run in O(log n).

**Example**: `[4,5,6,7,0,1,2]` rotated at index 3. Search for `0` → return `4`.

## Optimal Approach
**Modified Binary Search** | Time: O(log n) | Space: O(1)

A rotated sorted array has a key property: **at least one half is always sorted**. Use this to decide which half to search.

At each step with `left`, `mid`, `right`:
1. Check if `nums[left..mid]` is sorted: `nums[left] <= nums[mid]`
   - If target is in this range `[nums[left], nums[mid])` → search left half
   - Else → search right half
2. Otherwise `nums[mid..right]` is sorted:
   - If target is in this range `(nums[mid], nums[right]]` → search right half
   - Else → search left half

```java
// Java — Optimal
public int search(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;

        // Left half is sorted
        if (nums[left] <= nums[mid]) {
            if (target >= nums[left] && target < nums[mid]) {
                right = mid - 1;   // Target in left half
            } else {
                left = mid + 1;    // Target in right half
            }
        }
        // Right half is sorted
        else {
            if (target > nums[mid] && target <= nums[right]) {
                left = mid + 1;    // Target in right half
            } else {
                right = mid - 1;   // Target in left half
            }
        }
    }
    return -1;
}
```

```python
# Python — Optimal
def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:           # Left half sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:                                  # Right half sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

## Suboptimal Approaches
- **Linear search O(n)**: Ignores the sorted structure. Doesn't meet the O(log n) requirement.
- **Find pivot first, then binary search**: Two-pass O(log n) — correct but unnecessarily complex. The one-pass approach is cleaner.

## Common Edge Cases
- **Not rotated** (e.g., `[1,2,3,4,5]`): The pivot is at index 0. `nums[left] <= nums[mid]` will always be true, degenerating into a normal binary search. Works correctly.
- **Rotated by 1** (e.g., `[2,3,4,5,1]`): Works correctly.
- **Single element**: `left == right == mid`. Checks `nums[mid] == target` immediately.
- **Target not in array**: Returns -1. Loop exits when `left > right`.
- **Duplicate values**: This problem guarantees unique values. If duplicates are allowed (variant problem), the `nums[left] <= nums[mid]` check becomes ambiguous and requires O(n) worst case.

## Key Concepts Tested
- Modified binary search — knowing that binary search works on any property that creates a monotone decision
- Recognizing that one half is ALWAYS sorted in a rotated array
- Careful boundary conditions: `>=` vs `>`, `left` vs `mid`
- `mid = left + (right - left) / 2` avoids integer overflow vs `(left + right) / 2`

## Verdict Guide
| Approach | Verdict |
|---|---|
| Modified binary search O(log n)/O(1) | **Optimal** |
| Two-pass (find pivot + binary search) O(log n)/O(1) | **Acceptable** |
| Linear search O(n) | **Suboptimal** |
| Incorrect boundary conditions (off-by-one) | **Incorrect** |
