# Two Sum

## Problem Statement
Given an array of integers `nums` and an integer `target`, return indices of the two numbers that add up to `target`. Exactly one solution exists. You may not use the same element twice.

## Optimal Approach
**Hash Map — Single Pass** | Time: O(n) | Space: O(n)

For each element at index `i`, compute `complement = target - nums[i]`. Check if `complement` already exists in the hash map. If yes → return `[map[complement], i]`. If no → store `nums[i] → i` in the map and continue.

The key insight: we check *before* inserting, so an element never matches itself. The map stores values seen so far, so any match found is guaranteed to be a *different* index.

```java
// Java — Optimal
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{};
}
```

```python
# Python — Optimal
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

## Suboptimal Approaches
- **Brute Force (nested loops)**: O(n²) time, O(1) space. Check every pair `(i, j)`. Correct but unacceptable for large inputs.
- **Sort + Two Pointers**: O(n log n) time — loses original indices unless you track them with a wrapper object. More complex than hash map with no benefit.

## Common Edge Cases
- `target` equals twice a single element (e.g., `nums=[3,3], target=6`) → must use two *different* indices. The "check before insert" pattern handles this correctly — both 3s are at different indices and one will be in the map when the other is processed.
- Array with exactly 2 elements → answer is always `[0, 1]`.
- Negative numbers → hash map handles naturally.
- Duplicate values in array (e.g., `[1,2,3,2], target=4`) → second occurrence finds the first in the map correctly.

## Key Concepts Tested
- Hash map O(1) lookup vs. linear search O(n)
- Complement pattern: `x + y = target → y = target - x`
- Critical detail: check-before-insert avoids same-index reuse

## Verdict Guide
| Approach | Verdict |
|---|---|
| Hash map single pass O(n)/O(n) | **Optimal** |
| Sort + two pointers with index tracking | **Acceptable** |
| Brute force nested loops O(n²)/O(1) | **Suboptimal** |
| Using a set instead of map (loses index) | **Incorrect** |
