# Container With Most Water

## Problem Statement
Given an integer array `height` of length `n`, find two lines such that the container they form with the x-axis holds the most water. Return the maximum amount of water the container can store. You cannot slant the container.

`water = min(height[left], height[right]) × (right - left)`

## Optimal Approach
**Two Pointers — Greedy Shrink** | Time: O(n) | Space: O(1)

Start with the widest possible container: `left = 0`, `right = n-1`. At each step, the water is `min(height[left], height[right]) × (right - left)`. Track `maxWater`.

**The greedy decision**: Move the pointer pointing to the **shorter** line inward. Why? The width decreases either way — so the only hope of finding more water is if we find a taller line. The taller side can never benefit from moving inward (it's already limited by the shorter side), so move the shorter one.

```java
// Java — Optimal
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1;
    int maxWater = 0;
    while (left < right) {
        int water = Math.min(height[left], height[right]) * (right - left);
        maxWater = Math.max(maxWater, water);
        if (height[left] <= height[right]) {
            left++;
        } else {
            right--;
        }
    }
    return maxWater;
}
```

```python
# Python — Optimal
def maxArea(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1
    return max_water
```

## Suboptimal Approaches
- **Brute Force O(n²)**: Check every pair `(i, j)`. Correct but too slow for large inputs.
- **Stack-based approach**: Overcomplicated for this problem. Stack is useful for Trapping Rain Water, not this one — a common confusion.

## Common Edge Cases
- **Two elements** (e.g., `[1, 1]`): Only one pair — answer is 1. Works correctly.
- **All same height** (e.g., `[4,4,4,4]`): Maximum container is the outermost pair. Two-pointer correctly starts there and finds it first.
- **Strictly increasing heights**: Answer is the last two elements. The pointer correctly moves left inward until it finds the best pair.
- **Very tall inner bars**: The two-pointer is greedy — it won't always find the inner tall bars if the outer bars are already optimal. This is fine because the problem asks for max, which the greedy provably finds.
- **Array of length 2**: Edge case — only one container possible. Works correctly.

## Key Concepts Tested
- Two-pointer technique on a problem that isn't immediately "sorted array"
- **Greedy proof**: Why move the shorter pointer? Because moving the taller one can only decrease or maintain water (width decreases, height is still limited by the shorter bar).
- Distinguishing this problem from **Trapping Rain Water** — different formula, different approach. This is about choosing two lines; Trapping Rain Water is about filling gaps between all lines.

## Verdict Guide
| Approach | Verdict |
|---|---|
| Two pointers O(n)/O(1) | **Optimal** |
| Brute force O(n²) | **Suboptimal** |
| Incorrect pointer movement (always move left, or always move right) | **Incorrect** |
