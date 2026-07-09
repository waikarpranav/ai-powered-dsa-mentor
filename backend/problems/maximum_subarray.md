# Maximum Subarray (Kadane's Algorithm)

## Problem Statement
Given an integer array `nums`, find the subarray with the largest sum and return its sum. The subarray must contain at least one element.

## Optimal Approach
**Kadane's Algorithm** | Time: O(n) | Space: O(1)

Maintain two variables: `currentSum` (best sum ending at current position) and `maxSum` (global best). For each element:

`currentSum = max(nums[i], currentSum + nums[i])`

The decision at each step: should I extend the current subarray, or start fresh from here? If `currentSum` is negative, it only drags future sums down — so restart from `nums[i]`.

`maxSum = max(maxSum, currentSum)`

```java
// Java — Optimal (Kadane's)
public int maxSubArray(int[] nums) {
    int maxSum = nums[0];      // Initialize to nums[0], NOT 0
    int currentSum = nums[0];
    for (int i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    return maxSum;
}
```

```python
# Python — Optimal (Kadane's)
def maxSubArray(nums):
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum
```

## Suboptimal Approaches
- **Brute Force O(n²)**: Check all subarrays with two nested loops. Unacceptable.
- **Brute Force O(n³)**: Triple nested loop summing each subarray. Very unacceptable.
- **Divide and Conquer O(n log n)**: Correct but unnecessarily complex. Split array, find max crossing subarray. Valid in interviews only if specifically asked.
- **DP with O(n) array**: `dp[i] = max(nums[i], dp[i-1] + nums[i])`. Correct, O(n) space — can be reduced to O(1) (Kadane's).

## Common Edge Cases
- **All negative numbers** (e.g., `[-3, -1, -2]`) → answer is `-1` (the largest single element). This is the most common bug: initializing `maxSum = 0` returns 0, which is wrong. Must initialize to `nums[0]`.
- **Single element** → return `nums[0]`.
- **Mixed positive and negative** → Kadane's handles correctly.
- **Array of all same value** → returns that value × length.
- Starting loop from index 0 without separate initialization → off-by-one or incorrect result.

## Key Concepts Tested
- Kadane's algorithm — knowing it by name and explaining it
- Greedy insight: when to "abandon" the current subarray (when it goes negative)
- Correct initialization: `nums[0]`, not 0 or `Integer.MIN_VALUE`
- Distinguishing "maximum subarray sum" from "maximum subarray product" (different problem)

## Verdict Guide
| Approach | Verdict |
|---|---|
| Kadane's O(n)/O(1) with correct initialization | **Optimal** |
| DP with O(n) array | **Acceptable** |
| Divide and Conquer O(n log n) | **Acceptable** (but overengineered) |
| Brute force O(n²) | **Suboptimal** |
| Kadane's with maxSum = 0 initialization (fails all-negative) | **Incorrect** |
