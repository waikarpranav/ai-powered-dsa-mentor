# House Robber

## Problem Statement
You are a robber planning to rob houses along a street. You cannot rob two **adjacent** houses (alarm triggers). Given an integer array `nums` where `nums[i]` is the money in house `i`, return the maximum amount you can rob tonight.

## Optimal Approach
**Space-Optimized DP** | Time: O(n) | Space: O(1)

`dp[i]` = maximum money robbed from houses `0..i`.

**Recurrence**: At each house `i`, you either:
- **Skip it**: `dp[i] = dp[i-1]`
- **Rob it**: `dp[i] = dp[i-2] + nums[i]`

`dp[i] = max(dp[i-1], dp[i-2] + nums[i])`

Since you only need the previous two values, reduce to two variables:

```java
// Java — Optimal O(n)/O(1)
public int rob(int[] nums) {
    if (nums.length == 1) return nums[0];
    int prev2 = nums[0];
    int prev1 = Math.max(nums[0], nums[1]);
    for (int i = 2; i < nums.length; i++) {
        int curr = Math.max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

```python
# Python — Optimal O(n)/O(1)
def rob(nums):
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
    return prev1
```

**Trace through `[2, 7, 9, 3, 1]`**:
- prev2=2, prev1=max(2,7)=7
- i=2: curr=max(7, 2+9)=11, prev2=7, prev1=11
- i=3: curr=max(11, 7+3)=11, prev2=11, prev1=11
- i=4: curr=max(11, 11+1)=12, prev2=11, prev1=12
- Answer: 12 (rob houses 0,2,4: 2+9+1=12 ✓)

## Common Edge Cases
- **Single house**: Return `nums[0]`. Handle before the loop.
- **Two houses**: Return `max(nums[0], nums[1])`. The initialization `prev1 = max(nums[0], nums[1])` handles this — loop starts at `i=2` and never runs.
- **All same values**: Returns `ceil(n/2) * value` — robs every other house.
- **Decreasing array**: Might just rob the first house. Handled correctly.

## Common Bug
Initializing `prev1 = nums[1]` instead of `prev1 = max(nums[0], nums[1])`. For `[3, 1, 3]`, this gives wrong answer of 4 instead of 6.

## Key Concepts Tested
- DP with optimal substructure: current decision depends on previous 2 states
- Space optimization: 1D array → 2 variables
- The "skip or take" recurrence — appears in many DP problems (Coin Change, LCS, etc.)
- House Robber II (circular array) extends this with two passes (rob 0..n-2 OR 1..n-1)

## Verdict Guide
| Approach | Verdict |
|---|---|
| Space-optimized DP O(n)/O(1) | **Optimal** |
| DP with O(n) array | **Acceptable** |
| Memoized recursion O(n)/O(n) | **Acceptable** |
| Greedy (just take every other house) | **Incorrect** (e.g., [2,1,1,2] → greedy gives 2 but answer is 4) |
