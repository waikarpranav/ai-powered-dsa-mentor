# Coin Change

## Problem Statement
Given an array `coins` of denominations and an integer `amount`, return the **fewest number of coins** needed to make up the amount. If it's not possible, return `-1`. You have infinite coins of each denomination.

## Optimal Approach
**Bottom-Up DP** | Time: O(amount × n) | Space: O(amount)

`dp[i]` = minimum coins needed to make amount `i`.

**Initialization**: `dp[0] = 0` (0 coins to make amount 0). All others = `∞` (impossible until proven otherwise).

**Recurrence**: For each amount `i` from 1 to `amount`, try every coin `c`:
`dp[i] = min(dp[i], dp[i - c] + 1)` if `i >= c` and `dp[i - c] != ∞`

```java
// Java — Bottom-Up DP (Optimal)
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);   // Fill with "infinity" (amount+1 is impossible max)
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

```python
# Python — Bottom-Up DP
def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Trace through `coins=[1,2,5], amount=11`**:
- dp[0]=0, dp[1]=1, dp[2]=1, dp[3]=2, dp[4]=2, dp[5]=1, dp[6]=2, ..., dp[11]=3
- Answer: 3 (5+5+1)

## Alternative Approach (Top-Down with Memoization)
```java
public int coinChange(int[] coins, int amount) {
    int[] memo = new int[amount + 1];
    Arrays.fill(memo, -1);
    int result = dfs(coins, amount, memo);
    return result == Integer.MAX_VALUE ? -1 : result;
}
private int dfs(int[] coins, int rem, int[] memo) {
    if (rem < 0) return Integer.MAX_VALUE;
    if (rem == 0) return 0;
    if (memo[rem] != -1) return memo[rem];
    int min = Integer.MAX_VALUE;
    for (int coin : coins) {
        int sub = dfs(coins, rem - coin, memo);
        if (sub != Integer.MAX_VALUE) min = Math.min(min, sub + 1);
    }
    return memo[rem] = min;
}
```

## Suboptimal Approaches
- **Greedy (largest coin first)**: Works for standard coin systems (US quarters, dimes, etc.) but FAILS for general coin sets. E.g., `coins=[1,3,4], amount=6`: greedy gives 4+1+1=3 coins but DP finds 3+3=2 coins.
- **Plain recursion without memo**: O(amount^n) — exponential, completely unacceptable.

## Common Edge Cases
- **amount = 0**: Return 0. `dp[0] = 0` handles this.
- **No combination possible** (e.g., `coins=[2], amount=3`): `dp[3]` stays at `amount+1` → return -1.
- **Single coin equal to amount**: Return 1.
- **Coin larger than amount**: The `coin <= i` check skips it correctly.
- **Using `Integer.MAX_VALUE` as infinity**: Adding 1 to `Integer.MAX_VALUE` overflows. Use `amount + 1` as infinity instead (safe since the answer can never exceed `amount` coins of denomination 1).

## Key Concepts Tested
- Unbounded knapsack DP pattern (infinite supply of each item)
- Bottom-up DP iteration order: outer loop is `amount`, inner is `coins`
- Why greedy fails for general coin sets
- "Infinity" initialization trick: use `amount + 1` not `Integer.MAX_VALUE`

## Verdict Guide
| Approach | Verdict |
|---|---|
| Bottom-up DP O(amount × n)/O(amount) | **Optimal** |
| Top-down with memoization O(amount × n)/O(amount) | **Acceptable** |
| Greedy (largest coin first) | **Incorrect** for general coin sets |
| Plain recursion without memo | **Suboptimal** |
