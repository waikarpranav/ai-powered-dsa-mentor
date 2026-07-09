# Climbing Stairs

## Problem Statement
You are climbing a staircase with `n` steps. Each time you can climb 1 or 2 steps. How many distinct ways can you climb to the top?

**Example**: n=4 → 5 ways (1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2)

## Optimal Approach
**Space-Optimized DP (Fibonacci)** | Time: O(n) | Space: O(1)

Let `dp[i]` = number of ways to reach step `i`.
- `dp[1] = 1` (only one way: take 1 step)
- `dp[2] = 2` (two ways: 1+1 or 2)
- `dp[i] = dp[i-1] + dp[i-2]` — you either came from step `i-1` (took 1 step) or from step `i-2` (took 2 steps)

This is exactly the Fibonacci sequence. You only need the last two values, so reduce to O(1) space.

```java
// Java — Optimal O(n)/O(1)
public int climbStairs(int n) {
    if (n <= 2) return n;
    int prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

```python
# Python — Optimal O(n)/O(1)
def climbStairs(n):
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1
```

## Alternative Approaches

**DP with O(n) array** — Acceptable:
```java
public int climbStairs(int n) {
    if (n <= 2) return n;
    int[] dp = new int[n + 1];
    dp[1] = 1; dp[2] = 2;
    for (int i = 3; i <= n; i++) dp[i] = dp[i-1] + dp[i-2];
    return dp[n];
}
```

**Recursion without memoization** — Suboptimal (O(2^n)):
```java
// DO NOT do this — exponential time
public int climbStairs(int n) {
    if (n <= 2) return n;
    return climbStairs(n-1) + climbStairs(n-2);
}
```

## Common Edge Cases
- **n = 1**: 1 way. Return 1.
- **n = 2**: 2 ways (1+1 or 2). Return 2.
- **n = 0**: Technically 1 way (do nothing). The problem guarantees n ≥ 1.
- **Large n**: O(1) space solution handles this without array allocation overhead.

## Key Concepts Tested
- Recognizing the Fibonacci pattern in DP problems
- Space optimization: 1D DP → two variables
- Why naive recursion is O(2^n): subproblems are recomputed exponentially
- This is the "Hello World" of DP — interviewers use it to check if you know top-down vs bottom-up and space optimization

## The DP Framework Applied Here
1. **Define state**: `dp[i]` = ways to reach step `i`
2. **Recurrence**: `dp[i] = dp[i-1] + dp[i-2]`
3. **Base cases**: `dp[1] = 1, dp[2] = 2`
4. **Order**: bottom-up (i = 3 to n)
5. **Optimize space**: keep only last 2 values

## Verdict Guide
| Approach | Verdict |
|---|---|
| Space-optimized DP O(n)/O(1) | **Optimal** |
| DP with O(n) array | **Acceptable** |
| Memoized recursion (top-down) O(n)/O(n) | **Acceptable** |
| Plain recursion without memo O(2^n) | **Suboptimal** |
