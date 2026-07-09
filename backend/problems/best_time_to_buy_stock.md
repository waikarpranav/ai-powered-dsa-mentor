# Best Time to Buy and Sell Stock

## Problem Statement
Given an array `prices` where `prices[i]` is the price on day `i`, find the maximum profit achievable from a single buy-sell transaction. Must buy before selling. If no profit is possible, return 0.

## Optimal Approach
**Single Pass — Track Running Minimum** | Time: O(n) | Space: O(1)

Maintain two variables: `minPrice` (lowest price seen so far) and `maxProfit`. For each price:
1. Update `maxProfit = max(maxProfit, price - minPrice)`
2. Update `minPrice = min(minPrice, price)`

The order matters: check profit first, then update minPrice. This ensures we never "buy and sell on the same day" in a way that matters (profit would just be 0 or negative).

```java
// Java — Optimal
public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE;
    int maxProfit = 0;
    for (int price : prices) {
        maxProfit = Math.max(maxProfit, price - minPrice);
        minPrice = Math.min(minPrice, price);
    }
    return maxProfit;
}
```

```python
# Python — Optimal
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        max_profit = max(max_profit, price - min_price)
        min_price = min(min_price, price)
    return max_profit
```

## Suboptimal Approaches
- **Brute Force**: O(n²) — try every pair (buy_day, sell_day) where buy_day < sell_day. Correct but unacceptable.
- **DP with full dp array**: O(n) time, O(n) space — stores min-so-far in an array. Correct but wastes space; reducible to O(1).
- **Sorting**: Incorrect — sorting destroys the temporal ordering (must buy before sell).

## Common Edge Cases
- Prices strictly decreasing (e.g., `[5,4,3,2,1]`) → no profitable transaction possible → return 0. The `maxProfit = 0` initialization handles this since `price - minPrice` will always be ≤ 0.
- Single element array (`[7]`) → no transaction possible → return 0.
- All prices equal (e.g., `[3,3,3]`) → return 0.
- Maximum is at the very start and minimum at the end → returns 0 correctly (can't sell before buying).
- Initializing `maxProfit = Integer.MIN_VALUE` instead of 0 is a bug — the problem guarantees we can return 0 if no profit is achievable.

## Key Concepts Tested
- Greedy: maintain running minimum
- Recognizing that O(1) extra space is achievable (no need for DP array)
- Distinguishing from "Best Time to Buy and Sell Stock II" (unlimited transactions — that's a greedy problem, not this one)

## Verdict Guide
| Approach | Verdict |
|---|---|
| Single pass O(n)/O(1) | **Optimal** |
| DP with O(n) dp array | **Acceptable** |
| Brute force O(n²)/O(1) | **Suboptimal** |
| Any approach that ignores time ordering | **Incorrect** |
